"""H2 decision-only engine. It never invokes any tool or changes protected state."""
from .policy_evaluator import evaluate
from .reconciliation import reconcile

DISPOSITIONS = ('ALLOW', 'ALLOW_WITH_MITIGATION', 'REVALIDATE', 'ESCALATE', 'REFUSE_PAUSE')

def decide(task, authority, dsa, esa, request, sequence=1):
    invalid, denied = evaluate(task, authority, dsa, request, esa)
    rec = reconcile(dsa, esa, request)
    # Preserve secondary divergence evidence, even where refusal wins precedence.
    reasons = sorted(set(invalid + denied + rec['reasons']))
    if invalid or denied:
        disposition = 'REFUSE_PAUSE'
    elif rec['revalidate']:
        disposition = 'REVALIDATE'
    else:
        disposition = 'ALLOW'  # Escalation policy not defined in initial fixtures.
    action = request.get('action') if isinstance(request, dict) else None
    action = action if isinstance(action, dict) else {}
    return {
        'decision_id': f'DEC-{sequence:04d}',
        'request_id': request.get('request_id') if isinstance(request, dict) else None,
        'principal': request.get('agent_id') if isinstance(request, dict) else None,
        'task_id': request.get('task_id') if isinstance(request, dict) else None,
        'operation': action.get('operation'), 'target': action.get('target'), 'resource': action.get('resource'),
        'authority_id': authority.get('authority_id'), 'authority_version': authority.get('authority_version'),
        'dsa_id': dsa.get('dsa_id'), 'dsa_version': dsa.get('dsa_version'),
        'esa_id': esa.get('esa_id') if isinstance(esa, dict) else None,
        'esa_version': esa.get('esa_version') if isinstance(esa, dict) else None,
        'policy_version': dsa.get('policy_version'), 'disposition': disposition,
        'reason_codes': reasons, 'reconciliation': rec, 'execution_eligible': disposition == 'ALLOW',
        'sequence': sequence, 'provenance': 'HARNESS-OBSERVATION'
    }
