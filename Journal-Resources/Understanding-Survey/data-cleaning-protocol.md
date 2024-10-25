# Data Cleaning Protocol

The following changes were performed with the raw data set:

– Removing 48 incomplete responses
- Removing invalid answers that took too long or not long enough: 2 complete response and 12 single answers to questions
– Removing custom LimeSurvey strings from column names
– Removing the strings `(very easy)` and `(very hard)` from the answers to rating questions
– Converting the string answers to the comprehension questions to `1` (correct) or `0` (incorrect)
– Converting `yes` and `no` to `1` and `0`
– Converting the preferred Richardson maturity level from number plus string to number only (`0` to `3`)
– Resolving and harmonizing free-text answers (`other`) for current role and technical API perspective
– Harmonizing country names
– Adding binary variables (`1` or `0`) for is Student, is Academia, and is Germany
– Renaming some columns for convenient access in the analysis script