# Data Cleaning Protocol

The following changes were performed with the raw data set:

– Removing 46 incomplete responses
- Removing invalid answers that took too long or not long enough
– Removing custom LimeSurvey strings from column names
– Converting the string answers to the comprehension questions to `1` (correct) or `0` (incorrect)
– Converting `yes` and `no` to `1` and `0`
– Converting the preferred Richardson maturity level from number plus string to number only (`0` to `3`)
– Adding binary variables (`1` or `0`) for is_Student, is_Academia, and is_Canada
– Renaming some columns for convenient access in the analysis script