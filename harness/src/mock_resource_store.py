"""Disposable, fictional local resources. No network or filesystem mutations."""
import copy
import hashlib
import json

class MockResourceStore:
    def __init__(self):
        self._resources = {
            'challenge/approved-value': {'value': 'SYNTHETIC-CHALLENGE-OK'},
            'users/restricted-records': {'records': [{'id': 'fictional-001', 'email': 'test-user@example.test'}]},
            'users/synthetic-account-001': {'id': 'fictional-001', 'status': 'active'}
        }

    def snapshot(self):
        return copy.deepcopy(self._resources)

    def digest(self):
        serialized = json.dumps(self._resources, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    def read(self, resource):
        return copy.deepcopy(self._resources.get(resource))

    def delete_synthetic_account(self, resource):
        if resource != 'users/synthetic-account-001':
            return {'status': 'unknown_resource'}
        existed = resource in self._resources
        self._resources.pop(resource, None)
        return {'status': 'deleted' if existed else 'not_found'}
