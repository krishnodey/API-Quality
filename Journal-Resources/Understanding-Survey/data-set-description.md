# Data Set Description

General remarks:
- The substring `FR` means "following the rule", while `IR` means "ignoring the rule" (violation treatment)
- Empty cells mean no answer provided

Columns:
- Column B (`group_id`): refers to the two existing task orders (1 or 2)
- Columns C to AX: for each of the 12 rules and each treatment (`FR` or `IR`), there is a column pair consisting of a comprehension question (1 for correct, 0 for incorrect) and a rating question (from 1 for `very easy` up to 5 for `very difficult`)
- Columns AY to BV: for each of the 12 rules and each treatment (`FR` or `IR`), there is a column with the required time for the comprehension task in seconds
- Columns BW to CF: demographic information
- Column CE (`RichardsonMaturity`): participant knew about the Richardson maturity model (1) or not (0)
- Column CF (`MaturityLevel`): the minimum preferred Richardson maturity level of an API (0 to 3); in the survey, this had the following options:
    - "0 - The swamp of POX"
    - "1 - Resources"
    - "2 - HTTP Verbs"
    - "3 - Hypermedia controls"
- Column CG: final free-text comments from participants