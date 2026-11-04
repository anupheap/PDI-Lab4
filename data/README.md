# Candidate dataset

Place the user-supplied `CandidatePerformanceTest.csv` here to run exercises
6 and 7 with the original dataset. The working copy has been copied without
modification and is excluded from Git because it contains candidate IDs,
scores, and gender data. No individual candidate records are published.

- 958 candidate records, after a title record and a header record.
- The quoted `test preparation course` header contains a line break.
- Columns: ID, gender, group, Education, test preparation course, Math,
  English, Computer, Total, Average.
- Five groups occur: A, B, C, D, **and E**. The handout only names four group
  export files. The solution also exports group E to avoid omitting candidates.

The handout's short link is `https://shorturl.at/Q6K4O`; the user supplied this
local CSV when the short link could not be downloaded. After cloning, copy your
authorized local dataset into this directory, or pass its full path on the
command line. The integration tests generate fictional data and also check
the real CSV when it is available locally.
