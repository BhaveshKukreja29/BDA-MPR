import os
import mmh3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')
HASHTAGS_TXT = os.path.join(DATA_DIR, 'hashtags.txt')

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("Loading hashtags...")
with open(HASHTAGS_TXT, 'r', encoding='utf-8', errors='ignore') as f:
    hashtags = [line.strip() for line in f if line.strip()]

total_lines = len(hashtags)
print(f"Total hashtags (lines in file): {total_lines}")

print("\n" + "=" * 60)
print("Computing hashtag frequencies...")
freq = Counter(hashtags)
top_10 = freq.most_common(10)

print("\nTop 10 Most Frequent Hashtags:")
print(f"{'Hashtag':<35} {'Count':>10}")
print("-" * 46)
for tag, count in top_10:
    print(f"{tag:<35} {count:>10}")

print("\n" + "=" * 60)
print("Running Flajolet-Martin Algorithm...")


def flajolet_martin(hashtags):
    max_trailing_zeros = 0
    for tag in hashtags:
        hash_val = mmh3.hash(tag, signed=False)
        binary_hash = bin(hash_val)[2:]
        trailing_zeros = len(binary_hash) - len(binary_hash.rstrip('0'))
        max_trailing_zeros = max(max_trailing_zeros, trailing_zeros)
    print(f"Maximum trailing zeros observed: {max_trailing_zeros}")
    estimated_unique = 2 ** max_trailing_zeros
    print(f"Estimation Formula Used: 2 ** {max_trailing_zeros} = {estimated_unique}")
    return estimated_unique, max_trailing_zeros


estimated_unique, max_tz = flajolet_martin(hashtags)
actual_unique = len(set(hashtags))
print(f"\nEstimated number of unique hashtags (FM): {estimated_unique}")
print(f"Actual number of unique hashtags:         {actual_unique}")

print("\n" + "=" * 60)
print("Generating visualizations...")

categories = ['Total Hashtags', 'Estimated Unique Hashtags']
values = [total_lines, estimated_unique]

plt.figure(figsize=(8, 6))
bars = plt.bar(categories, values, color=['skyblue', 'orange'])
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}',
             ha='center', va='bottom')
plt.yscale('log')
plt.title('Hashtag Count vs Estimated Unique Hashtags (Flajolet-Martin)')
plt.ylabel('Count (log scale)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'fm_comparison.png'), dpi=150)
plt.close()
print("  fm_comparison.png saved")

top_tags = [t[0] for t in top_10]
top_counts = [t[1] for t in top_10]

plt.figure(figsize=(10, 7))
bars = plt.barh(top_tags[::-1], top_counts[::-1], color='skyblue')
for bar, count in zip(bars, top_counts[::-1]):
    plt.text(bar.get_width() + max(top_counts)*0.01, bar.get_y() + bar.get_height()/2,
             f'{count}', ha='left', va='center')
plt.title('Top 10 Most Frequent Hashtags')
plt.xlabel('Frequency')
plt.ylabel('Hashtag')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'top10_barchart.png'), dpi=150)
plt.close()
print("  top10_barchart.png saved")

plt.figure(figsize=(12, 9))
wedges, texts, autotexts = plt.pie(
    top_counts, labels=None, autopct='%1.1f%%',
    startangle=140, pctdistance=0.85, textprops={'fontsize': 9}
)
plt.legend(top_tags, loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=8)
plt.title('Top 10 Hashtags Distribution')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'top10_piechart.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  top10_piechart.png saved")

wc = WordCloud(width=800, height=400, background_color='white',
               max_words=200, colormap='Dark2')
wc.generate_from_frequencies(freq)

plt.figure(figsize=(12, 6))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Hashtags')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'wordcloud.png'), dpi=150)
plt.close()
print("  wordcloud.png saved")

with open(os.path.join(OUTPUT_DIR, 'results.txt'), 'w') as f:
    f.write(f"Total hashtags: {total_lines}\n")
    f.write(f"Actual unique hashtags: {actual_unique}\n")
    f.write(f"FM max trailing zeros: {max_tz}\n")
    f.write(f"FM estimated unique: {estimated_unique}\n")
    f.write(f"FM formula: 2^{max_tz} = {estimated_unique}\n\n")
    f.write("Top 10 Hashtags:\n")
    for tag, count in top_10:
        f.write(f"  {tag:<35} {count}\n")

print("  results.txt saved")
print(f"\n{'=' * 60}")
print("All done. Check output/ folder for results.")
