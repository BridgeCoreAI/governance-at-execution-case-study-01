"""Trusted H3 simulation coordinator. No external capabilities.

The executor capability is kept internal to the harness object boundary. This is
not a process isolation mechanism nor a production security boundary.
"""
from .decision_engine import decide
from .execution_gate import check_binding
from .execution_evidence import make_evidence

class PreventiveDispatcher:
    def __init__(self, executor, store):
        self._executor = executor
        self._store = store
        self.__capability = executor._make_dispatch()

    def _state(self):
        return {'digest': self._store.digest(), 'account': self._store.read('users/synthetic-account-001')}

    def dispatch(self, task, authority, dsa, esa, request, run_id='RUN-H3-001', before_gate=None):
        decision = decide(task, authority, dsa, esa, request)
        # A controlled, test-only hook permits a mutation between decision and dispatch.
        if before_gate is not None:
            before_gate(task, authority, dsa, esa, request)
        pre = self._state()
        eligible, reason = check_binding(decision, task, authority, dsa, esa, request)
        count_before = len(self._executor.invocations)
        invoked = False
        result = {'status': 'not_invoked', 'reason': reason}
        if eligible:
            result = self._executor.invoke(request['action'], capability=self.__capability)
            invoked = True
        post = self._state()
        evidence = make_evidence(run_id, request, decision, reason, invoked, result, pre, post, count_before, len(self._executor.invocations))
        return evidence
