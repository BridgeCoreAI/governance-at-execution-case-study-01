"""Deterministic exact-scope authorization. No real systems or tool permissions."""
OPS = frozenset({'read', 'reconnaissance', 'read_restricted_user_data', 'delete_user', 'modify_user'})

def evaluate(task, authority, dsa, request, esa):
    invalid, denied = [], []
    if not isinstance(request, dict):
        return ['REQUEST_MISSING'], []
    action = request.get('action')
    if not isinstance(action, dict):
        return ['ACTION_MISSING'], []
    required = ('request_id', 'agent_id', 'task_id', 'approval_id', 'authority_ref', 'dsa_ref', 'submitted_sequence')
    if any(not request.get(k) for k in required) or any(not action.get(k) for k in ('operation', 'target', 'resource')):
        invalid.append('REQUEST_INCOMPLETE')
    if action.get('operation') not in OPS:
        invalid.append('OPERATION_UNSUPPORTED')
    if any(not isinstance(action.get(k), str) for k in ('operation', 'target', 'resource')):
        invalid.append('ACTION_INVALID_TYPE')
    if not str(action.get('target', '')).endswith('.test'):
        invalid.append('TARGET_NOT_SYNTHETIC')
    if request.get('agent_id') != task.get('agent_id') or request.get('agent_id') != authority.get('principal') or request.get('agent_id') != dsa.get('agent_id'):
        invalid.append('PRINCIPAL_MISMATCH')
    if not (request.get('task_id') == task.get('task_id') == authority.get('task_id') == dsa.get('task_id')):
        invalid.append('TASK_MISMATCH')
    if not (request.get('approval_id') == task.get('approval_id') == authority.get('approval_id') == dsa.get('approval_id')):
        invalid.append('APPROVAL_MISMATCH')
    if not (request.get('authority_ref') == task.get('authority_ref') == authority.get('authority_id') == dsa.get('authority_ref')):
        invalid.append('AUTHORITY_REF_MISMATCH')
    if not (request.get('dsa_ref') == task.get('dsa_ref') == dsa.get('dsa_id')):
        invalid.append('DSA_REF_MISMATCH')
    if task.get('approval_status') != 'approved':
        invalid.append('TASK_UNAPPROVED')
    if authority.get('status') != 'active' or (isinstance(esa, dict) and esa.get('authority_status') in ('revoked','suspended')):
        invalid.append('AUTHORITY_INACTIVE')
    if task.get('policy_version') != dsa.get('policy_version'):
        invalid.append('POLICY_CONTEXT_INVALID')
    if task.get('expected_network_state') != dsa.get('assumptions', {}).get('network_state'):
        invalid.append('DSA_ASSUMPTION_INCONSISTENT')
    if task.get('authorized_target') != dsa.get('assumptions', {}).get('target'):
        invalid.append('DSA_TARGET_INCONSISTENT')
    if task.get('approved_intent') != dsa.get('approved_intent'):
        invalid.append('INTENT_MISMATCH')
    if action.get('operation') in authority.get('prohibited_operations', []):
        denied.append('OPERATION_EXPLICITLY_PROHIBITED')
    if not (action.get('target') == task.get('authorized_target') and action.get('resource') == task.get('authorized_resource') and action.get('operation') in task.get('authorized_operations', [])):
        denied.append('TASK_SCOPE_DENIED')
    if not any(action.get('target') == p.get('target') and action.get('resource') == p.get('resource') and action.get('operation') in p.get('operations', []) for p in authority.get('permissions', [])):
        denied.append('DELEGATED_SCOPE_DENIED')
    return sorted(set(invalid)), sorted(set(denied))
