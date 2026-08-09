# Q4 Run Summary

## Recommended joint solution

```json
{
  "preferred_scenario": "baseline_joint",
  "selection_rule": "joint two-stage co-optimization minimizing operating cost under physical constraints; carbon scenarios use hard ε-constraints (infeasible if below NonAI floor or unreachable schedule floor)",
  "operating_cost_CNY": 1632012953.4730585,
  "carbon_tCO2": 1611850.536671484,
  "renewable_utilization": 0.3286225213082708,
  "renewable_utilization_of_deliverable": 1.0,
  "absorbed_re_mwh": 3795842.621511,
  "available_re_raw_mwh": 11550768.36,
  "peak_net_import_sum_MW": 2730.5854,
  "mean_wait_hour": 0.27208,
  "mean_network_latency_ms": 25.89244,
  "qos_loss": 0.54637,
  "hard_pass": true,
  "note_re_utilization": "renewable_utilization = absorbed / attachment AvailableRenewable (6-region sum). renewable_utilization_of_deliverable is LP fill-rate vs deliverable ceiling.",
  "n_tasks_scheduled": 50000,
  "carbon_note": "Absolute 90/80/70% of E0 may be infeasible due to NonAI carbon floor (~1.449e6). Feasible trade-off shown by carbon_gap_75/50."
}
```

## Carbon ε-constraint results

| scenario       |   operating_cost_CNY |   carbon_tCO2 |   carbon_budget_tCO2 | carbon_feasible   |   mean_wait_hour | hard_pass   |
|:---------------|---------------------:|--------------:|---------------------:|:------------------|-----------------:|:------------|
| baseline_joint |          1.63201e+09 |   1.61185e+06 |        nan           | True              |          0.27208 | True        |
| carbon_100     |          1.63201e+09 |   1.61185e+06 |          1.61185e+06 | True              |          0.27208 | True        |
| carbon_90      |          1.71934e+09 |   1.51916e+06 |          1.45067e+06 | False             |          5.40168 | False       |
| carbon_80      |          1.7194e+09  |   1.51923e+06 |          1.28948e+06 | False             |          6.28912 | False       |
| carbon_70      |          1.7194e+09  |   1.51923e+06 |          1.1283e+06  | False             |          6.28912 | False       |
| carbon_gap_75  |          1.64891e+09 |   1.57109e+06 |          1.57109e+06 | True              |          0.27208 | True        |
| carbon_gap_50  |          1.69298e+09 |   1.53033e+06 |          1.53033e+06 | True              |          0.27208 | True        |
| carbon_gap_25  |          1.71934e+09 |   1.51916e+06 |          1.48957e+06 | False             |          5.40168 | False       |


Hard ε-constraint: min cost s.t. E≤ε. Absolute carbon_90/80/70 vs E0 are largely below the NonAI floor or schedule floor and are marked infeasible. `carbon_gap_*` uses ε=NonAI_floor+α(E0−floor) and shows binding budgets with rising cost.


## Full scenario comparison

| scenario                  |   operating_cost_CNY |   carbon_tCO2 |   carbon_budget_tCO2 | carbon_feasible   |   renewable_utilization |   peak_net_import_sum_MW |   mean_wait_hour | hard_pass   |
|:--------------------------|---------------------:|--------------:|---------------------:|:------------------|------------------------:|-------------------------:|-----------------:|:------------|
| baseline_local_first      |          1.70619e+09 |   1.74144e+06 |        nan           | True              |                0.328623 |                  2669.65 |          0       | True        |
| baseline_lowest_price     |          1.60702e+09 |   1.68402e+06 |        nan           | True              |                0.328623 |                  2800    |         77.1671  | True        |
| baseline_lowest_carbon    |          1.63219e+09 |   1.61596e+06 |        nan           | True              |                0.328623 |                  2731.66 |         32.7886  | True        |
| baseline_joint            |          1.63201e+09 |   1.61185e+06 |        nan           | True              |                0.328623 |                  2730.59 |          0.27208 | True        |
| carbon_100                |          1.63201e+09 |   1.61185e+06 |          1.61185e+06 | True              |                0.328623 |                  2730.59 |          0.27208 | True        |
| carbon_90                 |          1.71934e+09 |   1.51916e+06 |          1.45067e+06 | False             |                0.328527 |                  2447    |          5.40168 | False       |
| carbon_80                 |          1.7194e+09  |   1.51923e+06 |          1.28948e+06 | False             |                0.328528 |                  2461.4  |          6.28912 | False       |
| carbon_70                 |          1.7194e+09  |   1.51923e+06 |          1.1283e+06  | False             |                0.328528 |                  2461.4  |          6.28912 | False       |
| price_peak_valley_amplify |          1.50821e+09 |   1.7307e+06  |        nan           | True              |                0.328623 |                  2631.25 |          0.27036 | True        |
| price_flat                |          1.76617e+09 |   1.59923e+06 |        nan           | True              |                0.328623 |                  2095.41 |          0.26928 | True        |
| price_carbon_linked       |          1.76044e+09 |   1.59788e+06 |        nan           | True              |                0.328623 |                  2709.82 |          0.27444 | True        |
| re_minus20                |          1.93343e+09 |   1.83374e+06 |        nan           | True              |                0.328623 |                  2800    |          0.27208 | True        |
| re_plus20                 |          1.34742e+09 |   1.44002e+06 |        nan           | True              |                0.328443 |                  2585.41 |          0.27208 | True        |
| peak_cap_90               |          1.63209e+09 |   1.6123e+06  |        nan           | True              |                0.328623 |                  2457.53 |          0.27208 | True        |
| carbon_gap_75             |          1.64891e+09 |   1.57109e+06 |          1.57109e+06 | True              |                0.328623 |                  2709.82 |          0.27208 | True        |
| carbon_gap_50             |          1.69298e+09 |   1.53033e+06 |          1.53033e+06 | True              |                0.328623 |                  2540.21 |          0.27208 | True        |
| carbon_gap_25             |          1.71934e+09 |   1.51916e+06 |          1.48957e+06 | False             |                0.328527 |                  2447    |          5.40168 | False       |