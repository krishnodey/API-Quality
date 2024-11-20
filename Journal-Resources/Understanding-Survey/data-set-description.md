# Data Set Description

General remarks:
- The substring `P` means "Patterns (following design practices)", while `AP` means "Antipatterns (ignoring API design praitces)" (violation treatment)
- Empty cells mean no answer provided

Columns:
- Columns C to CG: for each of the 14 patterns and antipatterns there is a column pair consisting of a comprehension question (1 for correct, 0 for incorrect) and a rating question for Understandability and Readability​ (from 1 for `very easy` up to 5 for `very difficult`)
- Columns CH to DI: for each of the patterns and antipatterns, there is a column with the required time for the comprehension task in seconds
- Columns DK to DT: demographic information
- Column CS (`RichardsonMaturity`): participant knew about the Richardson maturity model (1) or not (0)
- Column DT (`MaturityLevel`): the minimum preferred Richardson maturity level of an API (0 to 3); in the survey, this had the following options:
    - "0 - The swamp of POX"
    - "1 - Resources"
    - "2 - HTTP Verbs"
    - "3 - Hypermedia controls"
- Column DU: final free-text comments from participants