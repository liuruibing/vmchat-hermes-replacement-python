import asyncio
import json
from types import SimpleNamespace

import pytest

from app.artifacts.store import SqliteArtifactStore
from app.compatibility.hermes_request import GlobalQueryParameters, VmChatInput
from app.mandate_risk.catalogue import load_prebuilt_registry
from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk_v2.mapping import MappingResult
from app.mandate_risk_v2.mapping_models import CriticReview, FinalMappingReview
from app.mandate_risk_v2.models import EvidenceRef, Requirement, RequirementIR
from app.mandate_risk_v2.result import MatchedMetricResult, MetricReference, StrategyEvidenceResult, V2AnalysisResult
from app.mandate_risk_v2.session_results import MandateAnalysisStore
from app.mandate_risk_v2.strategy_evidence import StrategyEvidencePipeline
from app.session.manager import SessionManager
from app.session.store import SqliteSessionStore
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.mandate_risk_v2_graph import ParallelMandateAnalysis, join_strategy
from app.workflow.graphs.unified_agent import MandateRiskCopilotWorkflow


def make_result():
    metric = MatchedMetricResult(metric=MetricReference(raw_row_id=14, source_row=14, metric_name='跟踪误差'),
                                match_score=95, score_reason='原文明确约束主动风险')
    return V2AnalysisResult(document_name='mandate.pdf', metric_catalogue_name='test',
                            analysis_mode='screening', screened_metrics=[metric])


def context(question='请分析', *, document_ids=None, provider=None, operation='ask', loader=None):
    return WorkflowContext(
        input_val=VmChatInput(userMessage=question, globalQueryParameters=GlobalQueryParameters()),
        provider=provider, agent_id='mandate-risk-copilot', role_id='requirement-analyst',
        session_id='session-a', document_ids=document_ids or [],
        document_loader=loader, request_context={'operation': operation},
    )


@pytest.mark.anyio
async def test_requirement_first_graph_preserves_unmatched_rules_and_waits_before_mapping():
    extraction_started, strategy_started = asyncio.Event(), asyncio.Event()
    text = "Industry exposure must not exceed 20%.\n\nBorrowing is not permitted."
    clauses = split_document_clauses(text)
    ir = RequirementIR(document_name='mandate.pdf', requirements=[
        Requirement(requirement_id='R-1', requirement_type='QUANTITATIVE_LIMIT',
                    semantic_summary='行业集中度上限', evidence=EvidenceRef(clause_ids=['c0001']),
                    conditions=['Only during build-up']),
        Requirement(requirement_id='R-2', requirement_type='PROHIBITION',
                    semantic_summary='禁止借款', evidence=EvidenceRef(clause_ids=['c0002'])),
    ])
    extracted = SimpleNamespace(requirement_ir=ir, clauses=clauses,
                                usage={'complete': True, 'total_tokens': 3})

    class Extraction:
        async def run(self, **kwargs):
            extraction_started.set()
            await asyncio.wait_for(strategy_started.wait(), 1)
            return extracted

    class Mapping:
        async def run(self, *, ir, **kwargs):
            assert extraction_started.is_set()
            return MappingResult(links=[], dispositions=FinalMappingReview.model_validate({
                'dispositions': [
                    {'requirement_id': req.requirement_id, 'reason': req.semantic_summary,
                     'destinations': [{
                         'destination': destination, 'raw_row_ids': [],
                         'aspect': req.semantic_summary, 'reason': reason,
                         'evidence_clause_ids': req.evidence.clause_ids,
                     }]}
                    for req, destination, reason in [
                        (ir.requirements[0], 'LIBRARY_GAP', '行业偏离度不能替代行业绝对集中度'),
                        (ir.requirements[1], 'NON_METRIC', '交易禁令仍需执行'),
                    ]
                ],
            }), critic=CriticReview(verdicts=[]), usage={'complete': True, 'total_tokens': 4})

    class Strategy:
        async def run(self, **kwargs):
            strategy_started.set()
            await asyncio.wait_for(extraction_started.wait(), 1)
            return StrategyEvidenceResult(), {'complete': True, 'total_tokens': 5}

    ctx = context(document_ids=['doc-a'], operation='analyze',
                  loader=lambda _: {'filename': 'mandate.pdf', 'text': text})
    graph = ParallelMandateAnalysis(load_prebuilt_registry(), requirement_pipeline=Extraction(),
                                   mapping_pipeline=Mapping(), strategy_pipeline=Strategy())
    completed = await graph.run(ctx, on_progress=lambda event: None)
    result = completed.metadata['mandate_risk_v2']['result']
    assert result['analysis_mode'] == 'detailed'
    assert [item['requirement']['requirement_id'] for item in result['requirements']] == ['R-1', 'R-2']
    assert result['requirements'][0]['requirement']['conditions'] == ['Only during build-up']
    assert result['library_gaps'][0]['requirement']['requirement']['requirement_id'] == 'R-1'
    assert result['non_metric_requirements'][0]['evidence'][0]['text'] == 'Borrowing is not permitted.'
    assert result['screened_metrics'] == []
    assert 'Industry exposure must not exceed 20%.' in completed.output
    assert 'Borrowing is not permitted.' in completed.output
    assert completed.usage['total_tokens'] == 12


@pytest.mark.anyio
async def test_failed_parallel_branch_cancels_sibling():
    started, cancelled = asyncio.Event(), asyncio.Event()

    class Extraction:
        async def run(self, **kwargs):
            await started.wait()
            raise ValueError('extraction failed')

    class Strategy:
        async def run(self, **kwargs):
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                cancelled.set()

    graph = ParallelMandateAnalysis(requirement_pipeline=Extraction(), strategy_pipeline=Strategy())
    ctx = context(document_ids=['doc-a'], loader=lambda _: {'text': 'Tracking error below 3%.'})
    with pytest.raises(ValueError, match='extraction failed'):
        await graph.run(ctx, on_progress=lambda event: None)
    assert cancelled.is_set()


@pytest.mark.anyio
@pytest.mark.parametrize('bad_id', ['c9999', None])
async def test_independent_strategy_rejects_fabricated_evidence_and_unknown_metrics(bad_id):
    class Provider:
        async def run_skill(self, request):
            payload = {'sections': [], 'points': [{
                'title': '主动风险', 'summary': '控制主动风险', 'evidence_clause_ids': ['c0001'],
                'metric_links': [{'raw_row_id': 14 if bad_id else 9999, 'basis': 'EXPLICIT',
                                  'reason': '原文限制', 'evidence_clause_ids': [bad_id or 'c0001']}],
            }]}
            yield SimpleNamespace(contentDelta=json.dumps(payload), usage={'total_tokens': 3})
    with pytest.raises(ValueError, match='STRATEGY_EVIDENCE_INVALID'):
        await StrategyEvidencePipeline().run(document_name='test.pdf',
            clauses=split_document_clauses('Tracking error below 3%.'),
            catalogue_rows=load_prebuilt_registry().all(), provider=Provider())


def test_session_report_survives_reopen_and_is_scoped_to_document_and_session(tmp_path):
    artifact_path, session_path = str(tmp_path / 'artifacts.db'), str(tmp_path / 'sessions.db')
    artifacts, sessions = SqliteArtifactStore(artifact_path), SqliteSessionStore(session_path)
    store = MandateAnalysisStore(artifacts, SessionManager(sessions))
    original = make_result().model_dump(mode='json')
    store.save(session_id='a', document_id='doc-a', run_id='run-1', result=original,
               agent_id='mandate-risk-copilot', role_id='requirement-analyst')
    artifacts.close()
    sessions.close()
    artifacts, sessions = SqliteArtifactStore(artifact_path), SqliteSessionStore(session_path)
    try:
        store = MandateAnalysisStore(artifacts, SessionManager(sessions))
        assert store.load('a', 'doc-a')['screened_metrics'][0]['match_score'] == 95
        assert store.load('a', 'doc-b') is None
        assert store.load('b', 'doc-a') is None
        # A forged cross-session pointer must not reveal another session's PDF.
        victim = store.sessions.get_or_create('b')
        victim.semanticState = store.sessions.store.get('a').semanticState
        store.sessions.store.put(victim)
        assert store.load('b', 'doc-a') is None
    finally:
        artifacts.close()
        sessions.close()


class AnswerProvider:
    def __init__(self):
        self.payload = None

    async def run_skill(self, request):
        self.payload = json.loads(request.user_prompt)
        yield SimpleNamespace(contentDelta='依据已提供的资料回答。', usage={'total_tokens': 5})


@pytest.mark.anyio
async def test_definition_question_does_not_load_pdf_or_send_report_history():
    provider = AnswerProvider()

    def forbidden(_):
        pytest.fail('definition-only question loaded PDF')

    ctx = context('跟踪误差的计算公式是什么？', document_ids=['doc-a'], provider=provider, loader=forbidden)
    events = [event async for event in MandateRiskCopilotWorkflow().stream(ctx)]
    assert events[-1].metadata['copilot']['intent'] == 'metric_qa'
    knowledge = provider.payload['metric_knowledge']
    assert [row['raw_row_id'] for row in knowledge] == [14]
    assert 'history' not in provider.payload
    assert 'relevant_clauses' not in provider.payload


@pytest.mark.anyio
async def test_mixed_pdf_question_reads_report_and_never_restarts_analysis():
    provider = AnswerProvider()
    ctx = context('分析一下为什么选跟踪误差，以及它的计算公式和PDF依据是什么？',
                  document_ids=['doc-a'], provider=provider,
                  loader=lambda _: {'filename': 'mandate.pdf', 'text': '[Page 2]\nTracking error below 3%.'})
    ctx.analysis_result_loader = lambda _: make_result().model_dump(mode='json')
    events = [event async for event in MandateRiskCopilotWorkflow().stream(ctx)]
    assert events[-1].metadata['copilot']['intent'] == 'doc_qa'
    assert provider.payload['analysis']['screened_metrics'][0]['match_score'] == 95
    assert provider.payload['relevant_clauses'][0]['page'] == 2
    assert provider.payload['metric_knowledge'][0]['raw_row_id'] == 14


@pytest.mark.anyio
async def test_metric_question_works_without_document_and_preserves_report_contract():
    ctx = context('什么是跟踪误差？', provider=AnswerProvider())
    events = [event async for event in MandateRiskCopilotWorkflow().stream(ctx)]
    assert events[-1].event == 'run.completed'
    assert events[-1].metadata['copilot']['intent'] == 'metric_qa'
    assert 'mandate_risk_v2' not in events[-1].metadata


@pytest.mark.anyio
async def test_unanalysed_document_is_not_presented_as_a_previous_report():
    provider = AnswerProvider()
    ctx = context('这份PDF为什么没有选夏普比率？', document_ids=['new-doc'], provider=provider,
                  loader=lambda _: {'text': 'Cash only.'})
    ctx.analysis_result_loader = lambda _: None
    events = [event async for event in MandateRiskCopilotWorkflow().stream(ctx)]
    assert events[-1].metadata['copilot']['intent'] == 'doc_qa'
    assert 'analysis' not in provider.payload
    assert 'analysis_status' in provider.payload


@pytest.mark.anyio
async def test_why_identified_as_risk_metric_routes_to_doc_qa_and_loads_evidence():
    provider = AnswerProvider()
    ctx = context('股息覆盖率 为什么会被识别为风险指标，证据是什么',
                  document_ids=['doc-a'], provider=provider,
                  loader=lambda _: {'filename': 'mandate.pdf', 'text': '[Page 1]\nCash only.\n[Page 2]\nMSCI China A High Dividend Yield Index shall be tracked.'})
    res = make_result()
    res.screened_metrics[0].metric.raw_row_id = 19
    res.screened_metrics[0].metric.metric_name = '股息覆盖率'
    res.screened_metrics[0].requirements = [
        SimpleNamespace(mapping_evidence=[{'clause_id': 'c0002', 'page': 2, 'text': 'MSCI China A High Dividend Yield Index shall be tracked.'}])
    ]
    ctx.analysis_result_loader = lambda _: res.model_dump(mode='json')
    events = [event async for event in MandateRiskCopilotWorkflow().stream(ctx)]
    assert events[-1].metadata['copilot']['intent'] == 'doc_qa'
    assert events[-1].metadata['copilot']['document_loaded'] is True
    assert provider.payload['analysis']['screened_metrics'][0]['metric']['metric_name'] == '股息覆盖率'
    # Priority evidence clause c0002 must be included in relevant_clauses
    clause_ids = [c['clause_id'] for c in provider.payload['relevant_clauses']]
    assert 'c0002' in clause_ids
