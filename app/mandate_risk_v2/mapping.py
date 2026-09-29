from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping_models import CriticReview, FinalMappingReview, MappingLink
from app.mandate_risk_v2.mapping_prompts import (
    CRITIC_SYSTEM_PROMPT, DESTINATION_SYSTEM_PROMPT, MAPPING_SYSTEM_PROMPT,
    batch_prompt, critic_prompt, destinations_prompt,
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

    @property
    def direct_links(self) -> list[MappingLink]:
        selected = {
            (item.requirement_id, row_id)
            for item in self.dispositions.dispositions
            for destination in item.destinations
            if destination.destination == "MAIN_TABLE"
            for row_id in destination.raw_row_ids
        }
        return [link for link in self.links if link.level == "DIRECT" and
                (link.requirement_id, link.raw_row_id) in selected]


def _apply_unconfirmed_critic_verdicts(
    dispositions: FinalMappingReview,
    critic: CriticReview,
) -> FinalMappingReview:
    """Downgrade only the exact row/aspect challenged by the independent Critic.

    MAIN_TABLE destinations can contain more than one metric row.  A challenge
    to one row must not demote its confirmed siblings.  LIBRARY_GAP has no row
    id, so it is keyed by Requirement + aspect.
    """

    result = dispositions.model_copy(deep=True)
    verdicts = {
        (item.requirement_id, item.destination, item.raw_row_id, item.aspect): item
        for item in critic.verdicts
    }

    for item in result.dispositions:
        rewritten = []
        for destination in item.destinations:
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

            if destination.destination == "LIBRARY_GAP":
                verdict = verdicts.get(
                    (item.requirement_id, "LIBRARY_GAP", None, destination.aspect)
                )
                if verdict is not None and verdict.verdict != "CONFIRM":
                    pending = destination.model_copy(deep=True)
                    pending.destination = "PENDING_REVIEW"
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
    return result


class MappingPipeline:
    def __init__(self, *, batch_size: int = 8, max_critic_repairs: int = 1) -> None:
        if batch_size < 1 or max_critic_repairs < 0:
            raise ValueError("invalid mapping batch or repair limit")
        self.batch_size = batch_size
        self.max_critic_repairs = max_critic_repairs
        self._model = RequirementExtractionPipeline()

    async def run(self, *, ir: RequirementIR, clauses: Sequence[DocumentClause],
                  registry: RawRiskMetricRegistry, provider: Any, signal: Any = None) -> MappingResult:
        rows = registry.all()
        if not rows:
            raise ValueError("MANDATE_RISK_METRIC_LIBRARY_INVALID: empty")
        usage_reports: list[dict[str, int] | None] = []

        async def call(system: str, prompt: str):
            payload, usage = await self._model._call_model(
                provider=provider, system_prompt=system, user_prompt=prompt, signal=signal,
            )
            usage_reports.append(usage)
            return payload

        critic_feedback: str | None = None
        for repair in range(self.max_critic_repairs + 1):
            links: list[MappingLink] = []
            for offset in range(0, len(rows), self.batch_size):
                batch_rows = rows[offset:offset + self.batch_size]
                feedback: str | None = critic_feedback
                for validation_attempt in range(2):
                    payload = await call(MAPPING_SYSTEM_PROMPT,
                                         batch_prompt(ir, clauses, batch_rows, feedback))
                    try:
                        batch = validate_batch(payload, ir=ir, registry=registry,
                                               batch_row_ids={x.row_id for x in batch_rows})
                        links.extend(batch.links)
                        break
                    except (ValueError, TypeError) as exc:
                        if validation_attempt:
                            raise ValueError(f"MANDATE_MAPPING_BATCH_INVALID: {exc}") from exc
                        feedback = str(exc)
            for validation_attempt in range(2):
                payload = await call(DESTINATION_SYSTEM_PROMPT,
                                     destinations_prompt(ir, clauses, rows, links, critic_feedback))
                try:
                    dispositions = validate_dispositions(payload, ir=ir, registry=registry,
                                                         links=links)
                    break
                except (ValueError, TypeError) as exc:
                    if validation_attempt:
                        raise ValueError(f"MANDATE_MAPPING_DESTINATIONS_INVALID: {exc}") from exc
                    critic_feedback = str(exc)
            payload = await call(CRITIC_SYSTEM_PROMPT,
                                 critic_prompt(ir, clauses, rows, links, dispositions))
            critic = validate_critic(payload, ir=ir, dispositions=dispositions)
            objections = [item for item in critic.verdicts if item.verdict != "CONFIRM"]
            if not objections or repair >= self.max_critic_repairs:
                if objections:
                    dispositions = _apply_unconfirmed_critic_verdicts(dispositions, critic)
                complete = all(report is not None and "total_tokens" in report
                               for report in usage_reports)
                usage: dict[str, Any] = {
                    "complete": complete, "expected_calls": len(usage_reports),
                    "reported_calls": sum(report is not None for report in usage_reports),
                }
                if complete:
                    usage["total_tokens"] = sum(report["total_tokens"] for report in usage_reports if report)
                return MappingResult(links=links, dispositions=dispositions,
                                     critic=critic, usage=usage)
            critic_feedback = "; ".join(
                f"{item.requirement_id}/{item.aspect}/{item.raw_row_id}: {item.reason}"
                for item in objections
            )[:4000]
        raise RuntimeError("mapping repair loop exhausted")
