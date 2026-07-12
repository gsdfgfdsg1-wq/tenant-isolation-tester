import unittest
from isolation import audit


class IsolationTests(unittest.TestCase):
    def test_accepts_same_tenant_response(self):
        self.assertTrue(audit([{ "request": {"tenant": "a"}, "response": {"tenant": "a", "resource_tenants": ["a"]}}])["isolated"])

    def test_detects_response_mismatch(self):
        report = audit([{ "request": {"tenant": "a"}, "response": {"tenant": "b"}}])
        self.assertEqual(report["findings"][0]["kind"], "response-tenant-mismatch")

    def test_detects_cache_and_resource_leaks(self):
        report = audit([{ "request": {"tenant": "a"}, "response": {"cache_tenant": "b", "resource_tenants": ["b"]}}])
        self.assertEqual(len(report["findings"]), 2)


if __name__ == "__main__":
    unittest.main()
