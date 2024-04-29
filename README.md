# Introduction

This repository seeks to document proper names in various Bible translations aligned by verse reference.

## Why this is useful

I've always imagined that it could be hugely helpful to have this large multilingual Biblical names database.  It would help machine translation, for sure.  But it could also be used as an enabler in starting up new projects.  Imagine the dataset was online and integrated with our BT tools, and we could offer new teams an easy way to get started with their names list for their translation brief.  Or, perhaps we could dynamically recognize how teams are translating the names ("Hey, I think you're reusing the names from the TBI, can I help?") and assist them with populate the names in their KBT list. - MM

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
    GROUP_CONCAT(DISTINCT macula_eng) FILTER (WHERE macula_eng <> "") AS macula_eng,
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

**Note**: If you use a filter like `tbi <> ""`, it may be wise to also check what names map to an empty slot for tbi. The reason the filter is there is that the `GROUP_CONCAT` function can produce a long line which makes the text much less readable on the command line.