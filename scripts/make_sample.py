"""Generate a deterministic, entirely artificial example log dataset."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/sample/illustrative_logs.csv"

def main() -> None:
    rng = np.random.default_rng(42)
    times = pd.date_range("2026-01-12", periods=7 * 24 * 12, freq="5min")
    services = ["kernel", "sshd", "cron", "network", "storage"]
    records = []
    for t in times:
        # A few fixed bursts are introduced ONLY for demonstrating anomaly charts.
        burst = (t.day == 14 and t.hour in (10, 11)) or (t.day == 17 and t.hour == 16)
        count = int(rng.poisson(2.5 + (8 if burst else 0)))
        for _ in range(count):
            service = str(rng.choice(services, p=[.22, .23, .13, .24, .18]))
            level = str(rng.choice(["INFO", "WARN", "ERROR"], p=[.77, .18, .05] if not burst else [.27, .31, .42]))
            event = {"INFO":"routine_event", "WARN":"retry_or_delay", "ERROR":"operation_error"}[level]
            records.append((t.isoformat(), service, level, event, "SYNTHETIC example; not a real system event"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records, columns=["timestamp", "service", "level", "event", "message"]).to_csv(OUTPUT, index=False)
    print(f"Generated {len(records)} synthetic rows: {OUTPUT}")

if __name__ == "__main__":
    main()
