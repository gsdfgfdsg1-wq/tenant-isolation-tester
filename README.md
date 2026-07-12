# tenant-isolation-tester

A defensive, dependency-free CLI for auditing recorded API exchanges for cross-tenant data exposure.

## Quick start

```bash
python isolation.py exchanges.json
```

Each exchange provides a request tenant and optional response tenant, cache tenant, and resource tenant list. The analyzer flags response mismatches, cache-key leakage, and resource ownership leaks. It performs no network requests and exits nonzero on findings.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
