# Twitter Trending Hashtags Analysis

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
| Total Hashtags | 2929192 |
| Unique Hashtags | 110728 |

---

## 3. Top 10 Hashtags by Frequency

| Hashtag | Count |
|---------|-------|
| #FarmersProtest | 1012052 |
| #farmersprotest | 38766 |
| #Farmers | 24611 |
| #IStandWithFarmers | 24344 |
| #FarmLaws | 18460 |
| #StandWithFarmers | 15983 |
| #FarmersProtests | 15241 |
| #Tractor2Twitter | 13407 |
| #HumanRights | 12461 |
| #India | 12300 |


### Bar Chart

![Top 10 Hashtags](/home/bhaveshkukreja/Desktop/BDA-MPR-Project/output/top10_barchart.png)

### Distribution

![Hashtag Distribution](/home/bhaveshkukreja/Desktop/BDA-MPR-Project/output/top10_piechart.png)

---

## 4. Flajolet Martin Algorithm

Probabilistic cardinality estimation using MurmurHash3. Counts maximum trailing zeros in binary hash values to approximate the number of distinct elements.

| Parameter | Value |
|-----------|-------|
| Max Trailing Zeros | 15 |
| Formula | 2^15 = 32768 |
| Estimated Unique | 32768 |
| Actual Unique | 110728 |

### Comparison Chart

![FM Comparison](/home/bhaveshkukreja/Desktop/BDA-MPR-Project/output/fm_comparison.png)

---

## 5. Word Cloud

![Word Cloud](/home/bhaveshkukreja/Desktop/BDA-MPR-Project/output/wordcloud.png)

---

## 6. Technology Mapping

| Component | Original (Hadoop) | Local (Python) |
|-----------|--------------------|----------------|
| Storage | HDFS | Local filesystem |
| Query Engine | Hive | csv module, Counter |
| Cardinality | Flajolet Martin (mmh3) | Flajolet Martin (mmh3) |
| Visualization | R ggplot2, wordcloud | matplotlib, wordcloud |
