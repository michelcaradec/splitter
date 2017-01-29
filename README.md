# Splitter

Utility to split file into multiple segments.

```bash
cat sample/data.txt | python splitter.py -batchcount:3 -output:output -reject:header.txt -skip:1
```

## Arguments

| Argument | Description |
|---|---|
| batchcount | Maximum number of lines per segment. |
| batchsize | Maximum size per segment. |
| output | Output file name. Will be appended with suffix `partXXXXX` made of a segment number (starting at 1) encoded on 5 positions (`part00001`, `part00002`, etc.). |
| skip | Number of lines to ignore (typically headers). |
| skipreject | File name where to store ignored lines. |
| skipinsert | Add ignored lines at the beginning of each segment. |

Notes:

- If neither `batchcount` nor `batchsize` arguments are provided, `batchcount` will be set to **1Mb**.
- `batchsize` argument  can be expressed in:
    - Bytes: `2147483648`
    - KBytes: `2097152KB`
    - MBytes: `2048MB`
    - GBytes: `2GB`
    - TBytes: `1TB`

## Examples

#### Split in segments of 4 lines, no header

```bash
cat sample/data.txt | python splitter.py -batchcount:4 -output:output -skip:1
```

#### Split in segments of 4 lines, header redirected to file header.txt 

```bash
cat sample/data.txt | python splitter.py -batchcount:4 -output:output -skip:1 -skipreject:header.txt
```

#### Split in segments of 4 lines, header at beginning of each segment

```bash
cat sample/data.txt | python splitter.py -batchcount:4 -output:output -skip:1 -skipinsert
```

#### Split in segments of 1 GB, no header

```bash
cat sample/data.txt | python splitter.py -batchsize:1gb -output:output -skip:1
```
