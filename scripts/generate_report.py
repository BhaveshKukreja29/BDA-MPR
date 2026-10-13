import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPORT_PATH = os.path.join(PROJECT_DIR, 'output.md')


def read_results():
    results = {}
    with open(os.path.join(OUTPUT_DIR, 'results.txt'), 'r') as f:
        for line in f:
            if line.startswith('Total hashtags:'):
                results['total'] = line.split(':')[1].strip()
            elif line.startswith('Actual unique'):
                results['actual_unique'] = line.split(':')[1].strip()
            elif line.startswith('FM max trailing'):
                results['max_tz'] = line.split(':')[1].strip()
            elif line.startswith('FM estimated'):
                results['fm_unique'] = line.split(':')[1].strip()
            elif line.startswith('FM formula'):
                results['fm_formula'] = line.split(':',1)[1].strip()
    top10 = []
    in_top = False
    with open(os.path.join(OUTPUT_DIR, 'results.txt'), 'r') as f:
        for line in f:
            if 'Top 10' in line:
                in_top = True
                continue
            if in_top and line.strip():
                parts = line.strip().rsplit(None, 1)
                if len(parts) == 2:
                    top10.append((parts[0], parts[1]))
    results['top10'] = top10
    return results


def generate_report(results):
    top10_rows = ""
    for tag, count in results['top10']:
        top10_rows += f"| {tag} | {count} |\n"

    img_dir = os.path.join(PROJECT_DIR, 'output')

    report = f"""# Twitter Trending Hashtags Analysis

## Big Data Analytics Mini Project (CSC702)

---

## 1. Data Preprocessing

Extracted `renderedContent` column from tweets CSV. Split tweet text on whitespace and filtered words starting with `#` to produce a flat hashtags file. Equivalent Hive query:

```sql
CREATE TABLE hashtags AS
SELECT word AS hashtag FROM tweets
LATERAL VIEW explode(split(tweet,' ')) t AS word
WHERE word LIKE '#%';
```

---

## 2. Hashtag Statistics

| Metric | Value |
|--------|-------|
| Total Hashtags | {results['total']} |
| Unique Hashtags | {results['actual_unique']} |

---

## 3. Top 10 Hashtags by Frequency

| Hashtag | Count |
|---------|-------|
{top10_rows}

### Bar Chart

![Top 10 Hashtags]({img_dir}/top10_barchart.png)

### Distribution

![Hashtag Distribution]({img_dir}/top10_piechart.png)

---

## 4. Flajolet Martin Algorithm

Probabilistic cardinality estimation using MurmurHash3. Counts maximum trailing zeros in binary hash values to approximate the number of distinct elements.

| Parameter | Value |
|-----------|-------|
| Max Trailing Zeros | {results['max_tz']} |
| Formula | {results['fm_formula']} |
| Estimated Unique | {results['fm_unique']} |
| Actual Unique | {results['actual_unique']} |

### Comparison Chart

![FM Comparison]({img_dir}/fm_comparison.png)

---

## 5. Word Cloud

![Word Cloud]({img_dir}/wordcloud.png)

---

## 6. Technology Mapping

| Component | Original (Hadoop) | Local (Python) |
|-----------|--------------------|----------------|
| Storage | HDFS | Local filesystem |
| Query Engine | Hive | csv module, Counter |
| Cardinality | Flajolet Martin (mmh3) | Flajolet Martin (mmh3) |
| Visualization | R ggplot2, wordcloud | matplotlib, wordcloud |
"""

    with open(REPORT_PATH, 'w') as f:
        f.write(report)
    print(f"Report generated: {REPORT_PATH}")


if __name__ == '__main__':
    results = read_results()
    generate_report(results)
