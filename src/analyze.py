"""Reproducible analysis for the demonstration CSV format only."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REQUIRED = {"timestamp", "service", "level", "event"}

def load_logs(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    missing = REQUIRED - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    invalid = int(data["timestamp"].isna().sum())
    if invalid:
        raise ValueError(f"Invalid timestamp rows: {invalid}; inspect raw source before cleaning")
    if data.empty:
        raise ValueError("Input contains no log rows")
    return data.sort_values("timestamp").copy()

def anomaly_flags(hourly_error_counts: pd.Series, threshold: int = 12) -> pd.Series:
    """Flag counts strictly greater than threshold; not a failure classifier."""
    return hourly_error_counts > threshold

def save_bar(series: pd.Series, title: str, ylabel: str, path: Path, color="steelblue") -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    series.plot(kind="bar", ax=ax, color=color)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("docs/figures"))
    args = parser.parse_args()
    data = load_logs(args.input)
    out = args.output
    out.mkdir(parents=True, exist_ok=True)

    save_bar(data.service.value_counts(), "Events by service (synthetic)", "Event count", out / "01_events_by_service.png")
    hourly = data.set_index("timestamp").resample("1h").size()
    fig, ax = plt.subplots(figsize=(9, 4))
    hourly.plot(ax=ax)
    ax.set(title="Events by hour (synthetic)", xlabel="Timestamp", ylabel="Events per hour")
    fig.tight_layout(); fig.savefig(out / "02_events_over_time.png", dpi=160); plt.close(fig)

    levels = data.level.value_counts().reindex(["INFO", "WARN", "ERROR"], fill_value=0)
    save_bar(levels, "Log severity distribution (synthetic)", "Event count", out / "03_severity_distribution.png")

    hourly_errors = data.loc[data.level.eq("ERROR")].set_index("timestamp").resample("1h").size()
    hourly_errors = hourly_errors.reindex(hourly.index, fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 4))
    hourly_errors.plot(ax=ax, color="darkorange")
    ax.set(title="Error events by hour (synthetic)", xlabel="Timestamp", ylabel="Error events per hour")
    fig.tight_layout(); fig.savefig(out / "04_errors_over_time.png", dpi=160); plt.close(fig)

    threshold = 12
    flags = anomaly_flags(hourly_errors, threshold=threshold)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(hourly_errors.index, hourly_errors.values, label="Error count")
    ax.axhline(threshold, linestyle="--", color="firebrick", label="Heuristic threshold")
    ax.scatter(hourly_errors.index[flags], hourly_errors[flags], color="firebrick", label="Flagged hour", zorder=3)
    ax.set(title="Illustrative anomaly flags — not verified failures", xlabel="Timestamp", ylabel="Error events per hour")
    ax.legend()
    fig.tight_layout(); fig.savefig(out / "05_hourly_anomaly_flags.png", dpi=160); plt.close(fig)

    summary = {"source_type": "synthetic_demo_only", "rows": len(data), "start": str(data.timestamp.min()), "end": str(data.timestamp.max()), "services": data.service.nunique(), "error_count": int(data.level.eq("ERROR").sum()), "flagged_hours": int(flags.sum()), "anomaly_rule": f"hourly ERROR count > {threshold}"}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
