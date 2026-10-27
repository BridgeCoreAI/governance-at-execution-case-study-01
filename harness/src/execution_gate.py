"""Decision binding check only. H3 will add the isolated mock executor."""

def check_binding(decision, task, authority, dsa, esa, request):
    if decision.get('disposition') != 'ALLOW' or not decision.get('execution_eligible'):
        return False, 'NON_ALLOW_DISPOSITION'
    action = request.get('action', {})
    pairs = (
        (decision.get('request_id'), request.get('request_id')),
        (decision.get('principal'), request.get('agent_id')),
        (decision.get('task_id'), request.get('task_id')),
        (decision.get('operation'), action.get('operation')),
        (decision.get('target'), action.get('target')),
        (decision.get('resource'), action.get('resource')),
        (decision.get('authority_id'), authority.get('authority_id')),
        (decision.get('authority_version'), authority.get('authority_version')),
        (decision.get('dsa_id'), dsa.get('dsa_id')),
        (decision.get('dsa_version'), dsa.get('dsa_version')),
        (decision.get('esa_id'), esa.get('esa_id')),
        (decision.get('esa_version'), esa.get('esa_version')),
        (decision.get('policy_version'), esa.get('policy_version')),
        (decision.get('policy_version'), dsa.get('policy_version')),
        (decision.get('policy_version'), task.get('policy_version')),
    )
    if any(a is None or b is None or a != b for a,b in pairs):
        return False, 'BINDING_MISMATCH'
    if authority.get('status') != 'active' or esa.get('authority_status') != 'active' or esa.get('evidence_freshness') != 'current':
        return False, 'CURRENT_STATE_INVALID'
    if dsa.get('assumptions', {}).get('network_state') != esa.get('observed_network_state') or dsa.get('assumptions', {}).get('target') != esa.get('current_target'):
        return False, 'STATE_CHANGED'
    if not any(action.get('target') == p.get('target') and action.get('resource') == p.get('resource') and action.get('operation') in p.get('operations', []) for p in authority.get('permissions', [])):
        return False, 'AUTHORITY_CHANGED'
    return True, 'BINDING_VALID'
