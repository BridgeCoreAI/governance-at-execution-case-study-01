"""Isolated mock executor. Private object-identity capability in one process.

Not secure against an attacker who can inspect the Python process, reflect into
private attributes, monkey-patch imports, or directly mutate the store.
"""
class MockExecutor:
    def __init__(self, resource_store):
        self._store = resource_store
        self.__capability = object()
        self.invocations = []
        self.denied_direct_attempts = 0

    def _make_dispatch(self):
        """Only the trusted local dispatch coordinator should call this."""
        return self.__capability

    def invoke(self, action, capability=None):
        if capability is not self.__capability:
            self.denied_direct_attempts += 1
            raise PermissionError('MOCK_EXECUTOR_AUTHORIZATION_REQUIRED')
        op, resource = action['operation'], action['resource']
        self.invocations.append({'operation': op, 'resource': resource, 'target': action['target']})
        if op == 'read':
            return {'status': 'success', 'data': self._store.read(resource)}
        if op == 'read_restricted_user_data':
            return {'status': 'success', 'data': self._store.read(resource)}
        if op == 'delete_user':
            return self._store.delete_synthetic_account(resource)
        if op == 'reconnaissance':
            return {'status': 'simulated_only', 'target': action['target']}
        return {'status': 'unsupported_operation'}
