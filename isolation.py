#!/usr/bin/env python3
"""Audit recorded API exchanges for cross-tenant isolation violations."""
import argparse
import json
from pathlib import Path


def audit(exchanges):
    findings = []
    for index, item in enumerate(exchanges):
        request_tenant = item.get("request", {}).get("tenant")
        response = item.get("response", {})
        response_tenant = response.get("tenant")
        cache_tenant = response.get("cache_tenant")
        resources = response.get("resource_tenants", [])
        if response_tenant and response_tenant != request_tenant:
            findings.append({"case": index, "kind": "response-tenant-mismatch", "expected": request_tenant, "actual": response_tenant})
        if cache_tenant and cache_tenant != request_tenant:
            findings.append({"case": index, "kind": "cache-key-leak", "expected": request_tenant, "actual": cache_tenant})
        for tenant in resources:
            if tenant != request_tenant:
                findings.append({"case": index, "kind": "resource-tenant-leak", "expected": request_tenant, "actual": tenant})
    return {"findings": findings, "isolated": not findings, "cases": len(exchanges)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exchanges")
    args = parser.parse_args()
    report = audit(json.loads(Path(args.exchanges).read_text()))
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["isolated"] else 1)


if __name__ == "__main__":
    main()
