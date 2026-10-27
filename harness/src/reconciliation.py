"""Synthetic DSA/ESA reconciliation. HARNESS-SPECIFICATION, not frozen implementation."""

def reconcile(dsa, esa, request):
    reasons = []
    if not isinstance(esa, dict):
        return {'material': True, 'revalidate': True, 'reasons': ['ESA_MISSING'], 'differences': ['ESA unavailable']}
    differences = []
    if esa.get('evidence_freshness') != 'current':
        reasons.append('ESA_STALE')
    expected = dsa.get('assumptions', {}).get('network_state')
    observed = esa.get('observed_network_state')
    if expected != observed:
        reasons.append('MR-001_NETWORK_DIVERGENCE')
        differences.append({'field': 'network_state', 'expected': expected, 'actual': observed})
    if esa.get('policy_version') != dsa.get('policy_version'):
        reasons.append('MR-004_POLICY_DIVERGENCE')
        differences.append({'field': 'policy_version', 'expected': dsa.get('policy_version'), 'actual': esa.get('policy_version')})
    if esa.get('current_target') != dsa.get('assumptions', {}).get('target'):
        reasons.append('MR-002_ENV_TARGET_DIVERGENCE')
        differences.append({'field': 'current_target', 'expected': dsa.get('assumptions', {}).get('target'), 'actual': esa.get('current_target')})
    if esa.get('authority_status') not in ('active',):
        reasons.append('MR-003_AUTHORITY_STATUS')
    return {'material': bool(reasons), 'revalidate': bool(reasons), 'reasons': reasons, 'differences': differences}
