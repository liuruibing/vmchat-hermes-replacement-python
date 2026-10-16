from __future__ import annotations


class MandateAnalysisStore:
    """Persist full reports in the existing artifact DB; sessions hold references."""

    kind = 'mandate-risk-v2-result'

    def __init__(self, artifact_store, session_manager):
        self.artifacts = artifact_store
        self.sessions = session_manager

    def save(self, *, session_id, document_id, run_id, result, agent_id, role_id):
        if not session_id or not document_id:
            raise ValueError('MANDATE_RESULT_REQUIRES_SESSION_AND_DOCUMENT')
        artifact = self.artifacts.create(
            session_id=session_id, kind=self.kind, payload=result,
            metadata={'document_id': document_id, 'run_id': run_id,
                      'catalogue_sha256': result.get('metric_catalogue_sha256')},
        )
        state = self.sessions.get_or_create(session_id, agent_id=agent_id, role_id=role_id)
        references = dict(state.semanticState.get('mandate_analysis_results') or {})
        references.pop(document_id, None)
        references[document_id] = artifact.id
        # Bound lightweight references independently of full report sizes.
        state.semanticState['mandate_analysis_results'] = dict(list(references.items())[-100:])
        self.sessions.store.put(state)
        return artifact.id

    def load(self, session_id, document_id):
        state = self.sessions.store.get(session_id)
        if state is None:
            return None
        reference = (state.semanticState.get('mandate_analysis_results') or {}).get(document_id)
        artifact = self.artifacts.get(reference) if reference else None
        if (artifact is None or artifact.kind != self.kind or artifact.sessionId != session_id
                or artifact.metadata.get('document_id') != document_id):
            return None
        return artifact.payload
