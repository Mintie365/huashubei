"""Re-run carbon ε-constraint scenarios using the saved baseline_joint schedule.

Rebuilds AI power from schedule_baseline_joint.csv, then runs absolute and
gap-based carbon targets with hard enforcement. Updates scenario_summary.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

Q4_DIR = Path(__file__).resolve().parent
if str(Q4_DIR) not in sys.path:
    sys.path.insert(0, str(Q4_DIR))

from config import EXECUTION_END, FIGURES, OUT, REGIONS, TABLES
from data_loader import load_data
from plot_results import plot_carbon_tradeoff, plot_scenario_bars
from power_opt import non_ai_carbon_floor
from scenarios import run_carbon_epsilon
from schedule import place

REGION_INDEX = {r: i for i, r in enumerate(REGIONS)}


def ai_power_from_schedule(schedule: pd.DataFrame) -> np.ndarray:
    ai = np.zeros((len(REGIONS), EXECUTION_END + 1), dtype=float)
    gpu = np.zeros((len(REGIONS), EXECUTION_END), dtype=float)
    for row in schedule.itertuples(index=False):
        place(
            float(row.GPU_Demand),
            float(row.PowerPerGPU),
            REGION_INDEX[row.ExecutionRegion],
            int(row.StartHour),
            int(row.EstimatedDuration_min),
            gpu,
            ai[:, :EXECUTION_END],
        )
    return ai


def main() -> None:
    t0 = time.time()
    data = load_data()
    sched_path = TABLES / "schedule_baseline_joint.csv"
    metrics_path = TABLES / "metrics_baseline_joint.json"
    if not sched_path.exists() or not metrics_path.exists():
        raise FileNotFoundError("Need baseline_joint schedule/metrics; run run_q4.py first")

    schedule = pd.read_csv(sched_path)
    base_metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    ai_power = ai_power_from_schedule(schedule)
    E0 = float(base_metrics["carbon_tCO2"])
    floor = non_ai_carbon_floor(data)
    print(f"E0={E0:.1f}, NonAI_floor={floor:.1f}, tasks={len(schedule)}", flush=True)

    joint_result = {"schedule": schedule, "ai_power": ai_power, "metrics": base_metrics}

    targets: list[tuple[str, float]] = [
        ("carbon_100", E0),
        ("carbon_90", 0.9 * E0),
        ("carbon_80", 0.8 * E0),
        ("carbon_70", 0.7 * E0),
    ]
    if E0 > floor + 1.0:
        gap = E0 - floor
        targets += [
            ("carbon_gap_75", floor + 0.75 * gap),
            ("carbon_gap_50", floor + 0.50 * gap),
            ("carbon_gap_25", floor + 0.25 * gap),
        ]

    carbon_rows = []
    for name, budget in targets:
        result = run_carbon_epsilon(
            data,
            name=name,
            carbon_budget_total=budget,
            task_subset=None,
            base_schedule=joint_result["schedule"],
            base_ai=joint_result["ai_power"],
            out_tables=TABLES,
            non_ai_floor=floor,
            max_delay_scan=24,
        )
        m = dict(result["metrics"])
        peaks = m.pop("peak_net_import_by_region_MW", {}) or {}
        checks = m.pop("resource_checks", {}) or {}
        row = m
        for region, val in peaks.items():
            row[f"peak_{region}"] = val
        row["resource_hard_pass"] = checks.get("hard_pass", True)
        carbon_rows.append(row)
        print(
            f"DONE {name}: actual={m['carbon_tCO2']:.1f} budget={budget:.1f} "
            f"feasible={m.get('carbon_feasible')} cost={m['operating_cost_CNY']:.1f}",
            flush=True,
        )

    summary_path = TABLES / "scenario_summary.csv"
    if summary_path.exists():
        old = pd.read_csv(summary_path)
        carbon_names = {r["scenario"] for r in carbon_rows}
        kept = old[~old["scenario"].isin(carbon_names) & ~old["scenario"].astype(str).str.startswith("carbon_")]
        # keep non-carbon; replace all carbon_* rows
        kept = old[~old["scenario"].astype(str).str.startswith("carbon_")]
        new = pd.concat([kept, pd.DataFrame(carbon_rows)], ignore_index=True)
        # stable-ish order: baselines first, then carbon, then others
        order = {n: i for i, n in enumerate(old["scenario"].tolist())}
        for r in carbon_rows:
            order.setdefault(r["scenario"], 10_000 + len(order))
        new["_ord"] = new["scenario"].map(lambda s: order.get(s, 10**9))
        new = new.sort_values("_ord").drop(columns=["_ord"])
    else:
        new = pd.DataFrame(carbon_rows)
    new.to_csv(summary_path, index=False, encoding="utf-8-sig")

    plot_scenario_bars(new, FIGURES / "01_scenario_metrics.png")
    plot_carbon_tradeoff(new, FIGURES / "02_cost_carbon_tradeoff.png")

    show = new[
        [
            c
            for c in [
                "scenario",
                "operating_cost_CNY",
                "carbon_tCO2",
                "carbon_budget_tCO2",
                "carbon_feasible",
                "mean_wait_hour",
                "hard_pass",
            ]
            if c in new.columns
        ]
    ]
    md = ["# Q4 Carbon Constraint Refresh\n", show.to_markdown(index=False), "\n"]
    (OUT / "q4_carbon_refresh.md").write_text("\n".join(md), encoding="utf-8")
    print(show.to_string(index=False))
    print(f"Elapsed {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
