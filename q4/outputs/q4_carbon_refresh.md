# Q4 Carbon Constraint Refresh

| scenario                  |   operating_cost_CNY |   carbon_tCO2 |   carbon_budget_tCO2 |   carbon_feasible |   mean_wait_hour | hard_pass   |
|:--------------------------|---------------------:|--------------:|---------------------:|------------------:|-----------------:|:------------|
| baseline_local_first      |          1.70619e+09 |   1.74144e+06 |        nan           |               nan |          0       | True        |
| baseline_lowest_price     |          1.60702e+09 |   1.68402e+06 |        nan           |               nan |         77.1671  | True        |
| baseline_lowest_carbon    |          1.63219e+09 |   1.61596e+06 |        nan           |               nan |         32.7886  | True        |
| baseline_joint            |          1.63201e+09 |   1.61185e+06 |        nan           |               nan |          0.27208 | True        |
| carbon_100                |          1.63201e+09 |   1.61185e+06 |          1.61185e+06 |                 1 |          0.27208 | True        |
| carbon_90                 |          1.71934e+09 |   1.51916e+06 |          1.45067e+06 |                 0 |          5.40168 | False       |
| carbon_80                 |          1.7194e+09  |   1.51923e+06 |          1.28948e+06 |                 0 |          6.28912 | False       |
| carbon_70                 |          1.7194e+09  |   1.51923e+06 |          1.1283e+06  |                 0 |          6.28912 | False       |
| price_peak_valley_amplify |          1.50821e+09 |   1.7307e+06  |        nan           |               nan |          0.27036 | True        |
| price_flat                |          1.76617e+09 |   1.59923e+06 |        nan           |               nan |          0.26928 | True        |
| price_carbon_linked       |          1.76044e+09 |   1.59788e+06 |        nan           |               nan |          0.27444 | True        |
| re_minus20                |          1.93343e+09 |   1.83374e+06 |        nan           |               nan |          0.27208 | True        |
| re_plus20                 |          1.34742e+09 |   1.44002e+06 |        nan           |               nan |          0.27208 | True        |
| peak_cap_90               |          1.63209e+09 |   1.6123e+06  |        nan           |               nan |          0.27208 | True        |
| carbon_gap_75             |          1.64891e+09 |   1.57109e+06 |          1.57109e+06 |                 1 |          0.27208 | True        |
| carbon_gap_50             |          1.69298e+09 |   1.53033e+06 |          1.53033e+06 |                 1 |          0.27208 | True        |
| carbon_gap_25             |          1.71934e+09 |   1.51916e+06 |          1.48957e+06 |                 0 |          5.40168 | False       |

