from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping_models import CriticReview, FinalMappingReview, MappingLink, MetricRowAssessment, RequirementDestination
from app.mandate_risk_v2.mapping_prompts import (
    CRITIC_SYSTEM_PROMPT,
    DESTINATION_SYSTEM_PROMPT,
    MAPPING_SYSTEM_PROMPT,
    batch_prompt,
    critic_prompt,
    destinations_prompt,
)
from app.mandate_risk_v2.mapping_validator import validate_batch, validate_critic, validate_dispositions
from app.mandate_risk_v2.models import RequirementIR
from app.mandate_risk_v2.pipeline import RequirementExtractionPipeline


@dataclass
class MappingResult:
    links: list[MappingLink]
    dispositions: FinalMappingReview
    critic: CriticReview
    usage: dict[str, Any]
    row_assessments: list[MetricRowAssessment] = field(default_factory=list)

    @property
    def screening_links(self) -> list[MappingLink]:
        rejected = {(item.requirement_id, item.raw_row_id) for item in self.critic.rejected_candidates}
        return [link for link in self.links if link.level in {"DIRECT", "REVIEW"}
                and (link.requirement_id, link.raw_row_id) not in rejected]

    @property
    def direct_links(self) -> list[MappingLink]:
        selected = {
            (item.requirement_id, row_id)
            for item in self.dispositions.dispositions
            for destination in item.destinations
            if destination.destination == "MAIN_TABLE"
            for row_id in destination.raw_row_ids
        }
        rejected = {(item.requirement_id, item.raw_row_id) for item in self.critic.rejected_candidates}
        return [
            link for link in self.links
            if link.level == "DIRECT" and (link.requirement_id, link.raw_row_id) in selected - rejected
        ]

    @property
    def candidate_links(self) -> list[MappingLink]:
        formal = {(link.requirement_id, link.raw_row_id) for link in self.direct_links}
        rejected = {(item.requirement_id, item.raw_row_id) for item in self.critic.rejected_candidates}
        return [link for link in self.links
                if link.level in {"DIRECT", "REVIEW"}
                and (link.requirement_id, link.raw_row_id) not in formal | rejected]


def _apply_unconfirmed_critic_verdicts(
    dispositions: FinalMappingReview,
    critic: CriticReview,
) -> FinalMappingReview:
    """Keep mapper proposals immutable and downgrade only final destinations."""

    result = dispositions.model_copy(deep=True)
    verdicts = {
        (item.requirement_id, item.destination, item.raw_row_id, item.aspect): item
        for item in critic.verdicts
    }
    rejected = {(item.requirement_id, item.raw_row_id): item for item in critic.rejected_candidates}

    for item in result.dispositions:
        rewritten = []
        for destination in item.destinations:
            removed = [rejected[(item.requirement_id, row_id)] for row_id in destination.raw_row_ids
                       if (item.requirement_id, row_id) in rejected]
            if removed:
                destination.raw_row_ids = [row_id for row_id in destination.raw_row_ids
                                          if (item.requirement_id, row_id) not in rejected]
                destination.reason += "; Critic 排除：" + "; ".join(entry.reason for entry in removed)
                if destination.destination == "MAIN_TABLE" and not destination.raw_row_ids:
                    destination.destination = "PENDING_REVIEW"
            if destination.destination == "MAIN_TABLE":
                confirmed_rows: list[int] = []
                objections = []
                for row_id in destination.raw_row_ids:
                    verdict = verdicts.get(
                        (item.requirement_id, "MAIN_TABLE", row_id, destination.aspect)
                    )
                    if verdict is not None and verdict.verdict != "CONFIRM":
                        objections.append(verdict)
                    else:
                        confirmed_rows.append(row_id)

                if confirmed_rows:
                    confirmed = destination.model_copy(deep=True)
                    confirmed.raw_row_ids = confirmed_rows
                    rewritten.append(confirmed)

                if objections:
                    pending = destination.model_copy(deep=True)
                    pending.destination = "PENDING_REVIEW"
                    pending.raw_row_ids = [
                        verdict.raw_row_id
                        for verdict in objections
                        if verdict.raw_row_id is not None
                    ]
                    if confirmed_rows:
                        pending.aspect = f"{destination.aspect} / Critic待确认"
                    details = "; ".join(
                        f"row {verdict.raw_row_id} {verdict.verdict}: {verdict.reason}"
                        for verdict in objections
                    )
                    pending.reason = f"Critic {details}; 原提案：{destination.reason}"
                    rewritten.append(pending)
                continue

            if destination.destination in {"LIBRARY_GAP", "NON_METRIC"}:
                verdict = verdicts.get(
                    (item.requirement_id, destination.destination, None, destination.aspect)
                )
                if verdict is not None and verdict.verdict != "CONFIRM":
                    pending = destination.model_copy(deep=True)
                    pending.destination = "PENDING_REVIEW"
                    pending.raw_row_ids = []
                    pending.reason = (
                        f"Critic {verdict.verdict}: {verdict.reason}; "
                        f"原提案：{destination.reason}"
                    )
                    rewritten.append(pending)
                else:
                    rewritten.append(destination)
                continue

            rewritten.append(destination)
        item.destinations = rewritten
    by_requirement = {item.requirement_id: item for item in result.dispositions}
    for missing in critic.missing_aspects:
        by_requirement[missing.requirement_id].destinations.append(RequirementDestination(
            destination="PENDING_REVIEW", raw_row_ids=[],
            evidence_clause_ids=missing.evidence_clause_ids,
            aspect=missing.aspect, reason=f"Critic 发现去向遗漏：{missing.reason}",
        ))
    return result


class MappingPipeline:
    def __init__(self, *, batch_size: int = 8, max_critic_repairs: int = 0,
                 concurrency: int = 2, critic_timeout_seconds: float = 240) -> None:
        if batch_size < 1 or max_critic_repairs < 0 or concurrency < 1:
            raise ValueError("invalid mapping batch or repair limit")
        if critic_timeout_seconds <= 0:
            raise ValueError("critic timeout must be positive")
        self.batch_size = batch_size
        self.max_critic_repairs = max_critic_repairs
        self.concurrency = concurrency
        self.critic_timeout_seconds = critic_timeout_seconds
        self._model = RequirementExtractionPipeline()

    async def run(
        self,
        *,
        ir: RequirementIR,
        clauses: Sequence[DocumentClause],
        registry: RawRiskMetricRegistry,
        provider: Any,
        signal: Any = None,
    ) -> MappingResult:
        rows = registry.all()
        if not rows:
            raise ValueError("MANDATE_RISK_METRIC_LIBRARY_INVALID: empty")
        usage_reports: list[dict[str, int] | None] = []
        validation_errors: list[dict[str, str]] = []

        async def call(stage: str, system: str, prompt: str):
            payload, usage = await self._model._call_model(
                provider=provider,
                system_prompt=system,
                user_prompt=prompt,
                signal=signal,
                stage=stage,
                timeout_seconds=self.critic_timeout_seconds if stage == "critic" else None,
            )
            usage_reports.append(usage)
            return payload

        critic_feedback: str | None = None
        for repair in range(self.max_critic_repairs + 1):
            links: list[MappingLink] = []
            row_assessments: list[MetricRowAssessment] = []
            semaphore = asyncio.Semaphore(self.concurrency)

            async def map_batch(batch_rows):
                feedback: str | None = critic_feedback
                async with semaphore:
                    for validation_attempt in range(2):
                        try:
                            payload = await call(
                                "mapping_batch",
                                MAPPING_SYSTEM_PROMPT,
                                batch_prompt(ir, clauses, batch_rows, feedback),
                            )
                            return validate_batch(
                                payload, ir=ir, registry=registry,
                                batch_row_ids={x.row_id for x in batch_rows},
                                require_scores=True,
                            )
                        except (ValueError, TypeError) as exc:
                            if validation_attempt:
                                raise ValueError(f"MANDATE_MAPPING_BATCH_INVALID: {exc}") from exc
                            feedback = str(exc)[:2000]
                            validation_errors.append({"stage": "mapping", "error": feedback})

            batches = await asyncio.gather(
                *(map_batch(rows[offset:offset + self.batch_size])
                  for offset in range(0, len(rows), self.batch_size)),
                return_exceptions=True,
            )
            for batch in batches:
                if isinstance(batch, BaseException):
                    raise batch
                links.extend(batch.links)
                row_assessments.extend(batch.row_assessments)

            for validation_attempt in range(2):
                try:
                    payload = await call(
                        "destinations",
                        DESTINATION_SYSTEM_PROMPT,
                        destinations_prompt(ir, clauses, rows, links, critic_feedback),
                    )
                    dispositions = validate_dispositions(
                        payload, ir=ir, registry=registry, links=links
                    )
                    break
                except (ValueError, TypeError) as exc:
                    if validation_attempt:
                        raise ValueError(f"MANDATE_MAPPING_DESTINATIONS_INVALID: {exc}") from exc
                    critic_feedback = str(exc)[:2000]
                    validation_errors.append({"stage": "destinations", "error": critic_feedback})

            critic_validation_feedback: str | None = None
            for validation_attempt in range(2):
                try:
                    payload = await call(
                        "critic",
                        CRITIC_SYSTEM_PROMPT,
                        critic_prompt(
                            ir,
                            clauses,
                            rows,
                            links,
                            dispositions,
                            critic_validation_feedback,
                            row_assessments=row_assessments,
                        )
                    )
                    critic = validate_critic(payload, ir=ir, dispositions=dispositions,
                                             registry=registry, links=links, require_scores=True)
                    break
                except (ValueError, TypeError) as exc:
                    if validation_attempt:
                        raise ValueError(f"MANDATE_MAPPING_CRITIC_INVALID: {exc}") from exc
                    critic_validation_feedback = str(exc)[:2000]
                    validation_errors.append({"stage": "critic", "error": critic_validation_feedback})

            objections = [item for item in critic.verdicts if item.verdict != "CONFIRM"]
            if not objections or repair >= self.max_critic_repairs:
                if objections or critic.rejected_candidates or critic.missing_aspects:
                    dispositions = _apply_unconfirmed_critic_verdicts(dispositions, critic)
                recalled_ids = {(link.requirement_id, link.raw_row_id) for link in critic.recalled_links}
                links = [link for link in links if (link.requirement_id, link.raw_row_id) not in recalled_ids]
                links.extend(critic.recalled_links)
                adjustments = {(item.requirement_id, item.raw_row_id): item
                               for item in critic.score_adjustments}
                links = [link.model_copy(update={
                    "match_score": adjustments[(link.requirement_id, link.raw_row_id)].match_score,
                    "score_reason": "Critic：" + adjustments[(link.requirement_id, link.raw_row_id)].score_reason,
                }) if (link.requirement_id, link.raw_row_id) in adjustments else link for link in links]
                complete = all(
                    report is not None and "total_tokens" in report
                    for report in usage_reports
                )
                usage: dict[str, Any] = {
                    "complete": complete,
                    "expected_calls": len(usage_reports),
                    "reported_calls": sum(report is not None for report in usage_reports),
                    "validation_errors": validation_errors,
                }
                if complete:
                    usage["total_tokens"] = sum(
                        report["total_tokens"] for report in usage_reports if report
                    )
                return MappingResult(
                    links=links,
                    dispositions=dispositions,
                    critic=critic,
                    usage=usage,
                    row_assessments=row_assessments,
                )

            critic_feedback = "; ".join(
                f"{item.requirement_id}/{item.destination}/{item.aspect}/{item.raw_row_id}: {item.reason}"
                for item in objections
            )[:4000]

        raise RuntimeError("mapping repair loop exhausted")
