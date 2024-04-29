# Introduction

...

# Data Sources

This data uses Macula [Greek](https://github.com/Clear-Bible/macula-greek/) and [Hebrew](https://github.com/Clear-Bible/macula-hebrew/) combined with alignments provided by UBS and generated using [eflomal](https://github.com/robertostling/eflomal). It pulls together these sources to produce a list of names in the Bible to support Bible translation work.

# Usage

Using sqlite, you can create a list of mappings from one language to another for a given langauge pair.

For example, if you wanted the TBI-BBC mappings for Luke, open `sqlite3`:

```sqlite3
.mode tabs
.import names.tsv names
```

This will load the tsv `file` into a `names` table. Now you can select the columns you want:

```sql
SELECT
    tbi,
    GROUP_CONCAT(DISTINCT bbc) FILTER (WHERE bbc <> "") AS bbc,
    GROUP_CONCAT(DISTINCT eng) FILTER (WHERE eng <> "") AS eng,
    COUNT(ref) AS refs
    -- GROUP_CONCAT(DISTINCT ref) AS refs
FROM
    names
WHERE
    ref LIKE "LUK%" AND
    tbi <> ""
GROUP BY
    tbi
ORDER BY
    tbi;
```
