# Evaluation method

An episode combines one frozen confirmed intent, a local catalogue slice, and either one fixed malicious fixture or no injection. Calibration and held-out manipulation families must not overlap. Day-2 development families belong only to calibration.

The runner executes baseline and guarded modes on the same candidates and seed. It records selection, action, reasons, and latency; the fake payment sink prevents network calls. Metrics use Wilson 95% intervals. Listing-level detector metrics and episode-level intervention metrics should remain separate when the starter dataset is expanded.

After reviewing calibration results, set thresholds once and run `python scripts/freeze.py`. Later changes require `--force-new-version`; never tune against held-out outcomes in place.

