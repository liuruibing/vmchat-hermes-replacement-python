from __future__ import annotations

import time
from typing import Any, Callable, TypedDict

from langgraph.graph import END, START, StateGraph

from app.compatibility.hermes_events import ReasoningDeltaEvent, RunCompletedEvent
from app.mandate_risk.catalogue import load_prebuilt_registry
from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk_v2.mapping import MappingPipeline
from app.mandate_risk_v2.pipeline import RequirementExtractionPipeline
from app.mandate_risk_v2.report import render_v2_report
from app.mandate_risk_v2.result import UnlinkedMetric, build_v2_analysis_result
from app.mandate_risk_v2.strategy_evidence import StrategyEvidencePipeline
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.mandate_risk_v2 import _resolve_uploaded_document


class AnalysisState(TypedDict, total=False):
    extraction: Any
    mapping: Any
    analysis: Any
    strategy: Any
    strategy_usage: dict
    requirement_seconds: float
    mapping_seconds: float
    strategy_seconds: float
    completed: Any


def join_strategy(analysis, strategy):
    """Keep independent evidence only; missing associations stay explicitly unlinked."""
    selected = {item.metric.raw_row_id: item for item in analysis.screened_metrics}
    points = [point.model_copy(update={
        'metric_links': [link for link in point.metric_links if link.raw_row_id in selected],
    }) for point in strategy.points]
    linked = {link.raw_row_id for point in points for link in point.metric_links}
    unlinked = {item.raw_row_id: item for item in strategy.unlinked_metrics}
    missing = [unlinked.get(row_id) or UnlinkedMetric(
        raw_row_id=row_id, metric_name=item.metric.metric_name,
        reason='独立策略提取未建立可靠关联；指标筛选依据仍保留，不代表存在策略关联。',
    ) for row_id, item in selected.items() if row_id not in linked]
    return strategy.model_copy(update={'points': points, 'unlinked_metrics': missing})


class ParallelMandateAnalysis:
    """Extract all requirements before mapping; read strategy independently."""

    def __init__(self, metric_registry=None, *, requirement_pipeline=None,
                 mapping_pipeline=None, strategy_pipeline=None):
        self.metric_registry = metric_registry
        self.requirements = requirement_pipeline or RequirementExtractionPipeline()
        self.mapping = mapping_pipeline or MappingPipeline(concurrency=1)
        self.strategy = strategy_pipeline or StrategyEvidencePipeline(concurrency=1)

    async def run(self, context: WorkflowContext, *, on_progress: Callable[[ReasoningDeltaEvent], None]):
        started = time.perf_counter()
        name, text = _resolve_uploaded_document(context)
        clauses = split_document_clauses(text)
        registry = self.metric_registry or load_prebuilt_registry()
        sequence = 0

        def progress(message):
            nonlocal sequence
            sequence += 1
            on_progress(ReasoningDeltaEvent(delta=message, sequence=sequence))

        async def extract(_state):
            tick = time.perf_counter()
            result = await self.requirements.run(
                document_name=name, document_text=text,
                provider=context.provider, signal=context.signal,
            )
            progress(f'原文要求及覆盖复核完成：{len(result.requirement_ir.requirements)} 项；开始映射指标库并保留未匹配要求。')
            return {'extraction': result, 'requirement_seconds': time.perf_counter() - tick}

        async def map_requirements(state):
            tick = time.perf_counter()
            extraction = state['extraction']
            mapping = await self.mapping.run(
                ir=extraction.requirement_ir, clauses=extraction.clauses,
                registry=registry, provider=context.provider, signal=context.signal,
            )
            analysis = build_v2_analysis_result(
                ir=extraction.requirement_ir, clauses=extraction.clauses,
                registry=registry, mapping=mapping,
            )
            progress(f'要求去向及指标复核完成：{len(analysis.matched_metrics)} 项直接关联指标，'
                     f'{len(analysis.candidate_metrics)} 项待确认候选；库内缺口和非指标要求均保留。')
            return {'mapping': mapping, 'analysis': analysis,
                    'mapping_seconds': time.perf_counter() - tick}

        async def strategy(_state):
            tick = time.perf_counter()
            result, usage = await self.strategy.run(
                document_name=name, clauses=clauses, catalogue_rows=registry.all(),
                provider=context.provider, signal=context.signal,
            )
            progress('独立策略原文提取完成。')
            return {'strategy': result, 'strategy_usage': usage,
                    'strategy_seconds': time.perf_counter() - tick}

        def join(state):
            analysis = state['analysis']
            analysis.strategy_evidence = join_strategy(analysis, state['strategy'])
            extraction, mapping = state['extraction'], state['mapping']
            phases = {
                'requirement_phase': extraction.usage,
                'mapping_phase': mapping.usage,
                'strategy_evidence_phase': state['strategy_usage'],
            }
            complete = all(phase.get('complete') for phase in phases.values())
            usage = {
                'complete': complete, 'analysis_mode': 'detailed', **phases,
                'timing_seconds': {
                    'requirements': round(state['requirement_seconds'], 3),
                    'mapping': round(state['mapping_seconds'], 3),
                    'strategy_evidence': round(state['strategy_seconds'], 3),
                    'analysis_total': round(time.perf_counter() - started, 3),
                },
                'result_counts': {
                    key: len(getattr(analysis, key)) for key in (
                        'requirements', 'screened_metrics', 'matched_metrics',
                        'candidate_metrics', 'pending_review', 'library_gaps',
                        'non_metric_requirements', 'contextual_facts',
                    )
                },
            }
            if complete:
                usage['total_tokens'] = sum(phase.get('total_tokens', 0) for phase in phases.values())
            progress('原文要求分析完成：指标关联、待确认、库内缺口及配置/治理要求已分别整理；不代表合规结论。')
            return {'completed': RunCompletedEvent(
                output=render_v2_report(
                    ir=extraction.requirement_ir, clauses=extraction.clauses,
                    registry=registry, mapping=mapping, analysis=analysis,
                ),
                usage=usage,
                metadata={'mandate_risk_v2': {'phase': 'complete', 'mode': 'detailed',
                                             'result': analysis.model_dump(mode='json')}},
            )}

        builder = StateGraph(AnalysisState)
        builder.add_node('extract_requirements', extract)
        builder.add_node('map_requirements', map_requirements)
        builder.add_node('extract_strategy', strategy)
        builder.add_node('join', join)
        builder.add_edge(START, 'extract_requirements')
        builder.add_edge(START, 'extract_strategy')
        builder.add_edge('extract_requirements', 'map_requirements')
        builder.add_edge(['map_requirements', 'extract_strategy'], 'join')
        builder.add_edge('join', END)
        progress('先逐节识别原文要求并复核覆盖，再映射完整指标库；同时独立整理策略原文。')
        result = await builder.compile().ainvoke({})
        return result['completed']
