# Introduction

This repository seeks to document proper names in various Bible translations aligned by verse reference.

## What this data is

| ref        | text     | macula_lemma | macula_eng | hcb       | cu2010s  | cu2010t  | rso94      | sruv06   | tbi      | lsg10     | rv09     | tpb08    | bbc      |
| ---------- | -------- | ------------ | ---------- | --------- | -------- | -------- | ---------- | -------- | -------- | --------- | -------- | -------- | -------- |
| LUK 1:3!11 | Θεόφιλε  | Θεόφιλος     | Theophilus | Tiyofilus | 提阿非罗 | 提阿非罗 | Феофил     | Theofilo | Teofilus | Théophile | Teófilo  |          |          |
| LUK 1:5!5  | Ἡρῴδου   | Ἡρῴδης       | Herod      | Hiridus   | 希律     | 希律     | Ирода      | herode   | herodes  | Hérode    | Herodes  | herot    | Herodes  |
| LUK 1:5!8  | Ἰουδαίας | Ἰουδαία      | Judea      | Yahudiya  | 犹太     | 猶太     | Иудейского | Yudea    | yudea    | Judée     | Judea    | judia    | Judea    |
| LUK 1:5!12 | Ζαχαρίας | Ζαχαρίας     | Zechariah  | Zakariya  | 撒迦利亚 | 撒迦利亞 | Захария    | Zakaria  | zakharia | Zacharie  | Zacarías | sekaraia | Sakarias |
| LUK 1:5!15 | Ἀβιά     | Ἀβιά         | Abijah     | Abiya     | 亚比雅   | 亞比雅   | Авиевой    | Abiya    | abia     | Abia      | Abías    | abiya    | Abia     |

## Languages currently included:

- **ARBNAV**: Arabic (NAV)
- **BBC**: Toba
- **BSB**: English
- **CU2010S**: Chinese Simplified
- **CU2010T**: Chinese Traditional
- **ESVUK16**: English
- **ENGULB**: English
- **HCB**: Hausa
- **LSG10**: French
- **RSO94**: Russian
- **RV09**: Spanish
- **SRUV06**: Swahili
- **TBI**: Indonesian
- **TGLULB**: Tagalog
- **TPB08**: Tok Pisin

## Why this is useful

...

# Data Sources

This data uses Macula [Greek](https://github.com/Clear-Bible/macula-greek/) and [Hebrew](https://github.com/Clear-Bible/macula-hebrew/) combined with alignments provided by UBS and generated using [eflomal](https://github.com/robertostling/eflomal). Note that stopwords are used to filter out poor alignments. The `names.tsv` file pulls together these sources to produce a list of names in the Bible to support Bible translation work.

# Usage

## Extraction Helper

The `scripts/extract_name_pairs.py` script exports columns of name pairs, dropping any rows with empty values.

```
python scripts/extract_name_pairs.py [-h] [-l] [column_one] [column_two]

Extract name pairs from a TSV file

positional arguments:
  column_one  Name of the first column to extract
  column_two  Name of the second column to extract

options:
  -h, --help  show this help message and exit
  -l, --list  List available columns
```

**Note**: You are expected to run python from the project root so that the relative path to `./names.tsv` is valid.

## Sqlite

Using sqlite, you can create a list of mappings from one language to another for a given langauge pair.

For example, if you wanted the TBI-BBC mappings for Luke, open `sqlite3`:

```sqlite3
.mode tabs
.import names.tsv names
```

This will load the tsv `file` into a `names` table. To get a table like the one above in order to explore the data, you could try something like:

```sql
SELECT * FROM names WHERE ref LIKE "LUK 1:%";
```

A more interesting/useful query would be one that groups equivalents across a language pair. For example, if we wanted to map TBI proper nouns to BBC translations and count the references, we could do something like this (I've included a commented column that will list every verse in which the name appears):

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
