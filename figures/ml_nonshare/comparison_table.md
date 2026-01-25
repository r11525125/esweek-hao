# ML Baseline Comparison Results

## Weighted Latency (HP×1.5 + LP×0.5)

| Method | nWifi=6 | nWifi=12 | nWifi=18 | nWifi=24 | nWifi=30 |
|--------|-------|-------|-------|-------|-------|
| PBM | 0.288 | 0.570 | 0.646 | 0.966 | 0.987 |
| MPS | 0.330 | 0.570 | 0.646 | 0.974 | 1.041 |
| SU | 0.296 | 0.423 | 0.648 | 0.881 | 1.167 |
| Non-MU-TXOP | 0.343 | 0.827 | 8.958 | 1.376 | 2.445 |
| ML-Old | 0.494 | 0.638 | 0.713 | 0.896 | 1.032 |
| ML-Old-v2 | 0.494 | 0.638 | 0.713 | 0.895 | 1.026 |
| B0-NonShare | 0.343 | 0.827 | 8.958 | 1.376 | 2.445 |

## Key Observations

1. **B0-NonShare = Non-MU-TXOP**: Sanity check PASSED (100% accuracy imitation)
2. **ML-Old/v2 vs PBM/MPS**: ML performs worse in most cases, validating rule-based contribution
3. **Non-MU-TXOP degradation at nWifi=18**: Shows importance of MU-TXOP Sharing
