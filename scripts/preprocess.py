import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
INPUT_CSV = os.path.join(DATA_DIR, 'tweets.csv')
TWEETS_TXT = os.path.join(DATA_DIR, 'tweets_content.txt')
HASHTAGS_TXT = os.path.join(DATA_DIR, 'hashtags.txt')


def extract_content():
    print("[1/3] Extracting tweet content from CSV...")
    count = 0
    with open(INPUT_CSV, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(TWEETS_TXT, 'w', encoding='utf-8') as fout:
        reader = csv.reader(fin)
        header = next(reader)
        try:
            col_idx = header.index('renderedContent')
        except ValueError:
            col_idx = 2
        print(f"   Using column index {col_idx} ('{header[col_idx]}')")
        for row in reader:
            if len(row) > col_idx and row[col_idx].strip():
                fout.write(row[col_idx].strip() + '\n')
                count += 1
    print(f"   Extracted {count} tweets -> tweets_content.txt")
    return count


def extract_hashtags():
    print("[2/3] Extracting hashtags from tweets...")
    total = 0
    with open(TWEETS_TXT, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(HASHTAGS_TXT, 'w', encoding='utf-8') as fout:
        for line in fin:
            words = line.strip().split()
            for word in words:
                if word.startswith('#'):
                    fout.write(word + '\n')
                    total += 1
    print(f"   Extracted {total} hashtags -> hashtags.txt")
    return total


def show_sample():
    print("\n[3/3] Sample data:")
    print("\n--- First 5 tweets ---")
    with open(TWEETS_TXT, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if i >= 5:
                break
            print(f"  [{i+1}] {line.strip()}")

    print("\n--- First 10 hashtags ---")
    with open(HASHTAGS_TXT, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            print(f"  [{i+1}] {line.strip()}")


if __name__ == '__main__':
    if not os.path.exists(INPUT_CSV):
        print(f"ERROR: {INPUT_CSV} not found!")
        print("Download from Kaggle and place tweets.csv in data/ folder.")
        exit(1)

    tweet_count = extract_content()
    hashtag_count = extract_hashtags()
    show_sample()
    print(f"\nDone. {tweet_count} tweets, {hashtag_count} hashtags extracted.")
