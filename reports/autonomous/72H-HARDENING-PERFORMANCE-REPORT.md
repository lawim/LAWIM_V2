# LAWIM_V2 — 72H AUTONOMOUS HARDENING PERFORMANCE REPORT

## Hot Path Benchmarks (bench_hot_paths.py)
| Operation | Iterations | Mean (ms) | Median (ms) | P95 (ms) |
|-----------|-----------|-----------|-------------|----------|
| repository.list_properties | 50 | 0.517 | 0.422 | 1.113 |
| services.list_conversations | 50 | 0.172 | 0.184 | 0.202 |
| services.bootstrap | 50 | 1.439 | 1.279 | 2.701 |
| repository.search_locations | 50 | 0.126 | 0.109 | 0.179 |

## Runtime Benchmarks (benchmark_runtime.py)
| Route | Iterations | P50 (ms) | P95 (ms) | Max (ms) |
|-------|-----------|----------|----------|----------|
| /readyz | 20 | 1.04 | 1.68 | 1.90 |
| /api/health | 20 | 3.65 | 6.50 | 15.19 |
| /api/properties?limit=10 | 20 | 1.64 | 3.40 | 4.04 |
| /api/bootstrap | 20 | 3.42 | 5.01 | 6.22 |

## Frontend Bundle
| Asset | Size | Gzip |
|-------|------|------|
| Total precached | 771.60 KiB | — |
| admin-BoqVoI0D.js | 233.05 kB | 45.52 kB |
| web-DBacQ9Xo.js | 94.83 kB | 19.69 kB |
| vendor-react-C6-hJ9ci.js | 144.35 kB | 46.68 kB |
| vendor-QpRix5i2.js | 94.76 kB | 26.51 kB |
| Build time | 4.33s | — |

## Assessment
All measured operations are well within acceptable latency thresholds. No regressions introduced.
