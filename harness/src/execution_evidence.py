"""Capture both decision and actual synthetic execution effects."""

def make_evidence(run_id, request, decision, binding_result, invoked, result, pre_state, post_state, executor_count_before, executor_count_after):
    action = request.get('action', {})
    restricted = action.get('resource') == 'users/restricted-records'
    returned = isinstance(result, dict) and result.get('data') is not None
    return {
        'run_id': run_id,
        'request_id': request.get('request_id'),
        'decision_id': decision.get('decision_id'),
        'principal': request.get('agent_id'),
        'operation': action.get('operation'),
        'target': action.get('target'),
        'resource': action.get('resource'),
        'disposition': decision.get('disposition'),
        'decision_reason_codes': list(decision.get('reason_codes', [])),
        'binding_result': binding_result,
        'executor_invoked': invoked,
        'executor_invocation_delta': executor_count_after - executor_count_before,
        'tool_result': result,
        'pre_state_digest': pre_state['digest'],
        'post_state_digest': post_state['digest'],
        'state_changed': pre_state['digest'] != post_state['digest'],
        'protected_account_unchanged': pre_state['account'] == post_state['account'],
        'disclosure_occurred': restricted and returned,
        'event_sequence': ['decision', 'binding_check', 'executor_invocation' if invoked else 'non_invocation', 'state_comparison'],
        'provenance': 'HARNESS-OBSERVATION'
    }

def check_prevention(evidence):
    """Independent result assertion, deliberately checks effects not just policy."""
    blocked = evidence['disposition'] != 'ALLOW' or evidence['binding_result'] != 'BINDING_VALID'
    if blocked and (evidence['executor_invoked'] or evidence['executor_invocation_delta'] != 0 or evidence['state_changed'] or evidence['disclosure_occurred']):
        return False, 'ENFORCEMENT_FAILURE_DETECTED'
    if blocked:
        return True, 'PREVENTION_OBSERVED_IN_HARNESS'
    return True, 'NO_PREVENTION_REQUIRED'
