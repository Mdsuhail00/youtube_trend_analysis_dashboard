import pandas as pd

# ── Load all 3 country CSV files ─────────────────────────────────
us = pd.read_csv("USvideos.csv", encoding='latin-1')
india = pd.read_csv("INvideos.csv", encoding='latin-1')
gb = pd.read_csv("GBvideos.csv", encoding='latin-1')

# ── Add country column ───────────────────────────────────────────
us['country'] = 'USA'
india['country'] = 'India'
gb['country'] = 'Great Britain'

# ── Merge all 3 into one dataset ─────────────────────────────────
df = pd.concat([us, india, gb], ignore_index=True)

# ── Step 1 - Drop unnecessary columns ───────────────────────────
df.drop(columns=['thumbnail_link', 'description', 'tags'], inplace=True)

# ── Step 2 - Fix date columns ────────────────────────────────────
df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')
df['publish_time'] = pd.to_datetime(df['publish_time'])

# ── Step 3 - Extract useful date parts ──────────────────────────
df['trending_year'] = df['trending_date'].dt.year
df['trending_month'] = df['trending_date'].dt.month
df['trending_month_name'] = df['trending_date'].dt.strftime('%b')
df['publish_hour'] = df['publish_time'].dt.hour
df['publish_day'] = df['publish_time'].dt.day_name()

# ── Step 4 - Add category names ──────────────────────────────────
category_map = {
    1: 'Film & Animation',
    2: 'Autos & Vehicles',
    10: 'Music',
    15: 'Pets & Animals',
    17: 'Sports',
    19: 'Travel & Events',
    20: 'Gaming',
    22: 'People & Blogs',
    23: 'Comedy',
    24: 'Entertainment',
    25: 'News & Politics',
    26: 'Howto & Style',
    27: 'Education',
    28: 'Science & Technology',
    29: 'Nonprofits & Activism'
}
df['category_name'] = df['category_id'].map(category_map).fillna('Other')

# ── Step 5 - Drop nulls ──────────────────────────────────────────
df.dropna(subset=['views', 'likes', 'dislikes', 'comment_count'], inplace=True)

# ── Step 6 - Remove duplicates ───────────────────────────────────
df.drop_duplicates(inplace=True)

# ── Step 7 - Add engagement rate column ─────────────────────────
df['engagement_rate'] = ((df['likes'] + df['dislikes'] + df['comment_count']) / df['views'] * 100).round(2)

# ── Step 8 - Keep only useful columns ───────────────────────────
df = df[['video_id', 'title', 'channel_title', 'category_id',
         'category_name', 'views', 'likes', 'dislikes',
         'comment_count', 'engagement_rate', 'trending_date',
         'trending_year', 'trending_month', 'trending_month_name',
         'publish_hour', 'publish_day', 'country']]

print("Cleaned shape:", df.shape)
print("\nData types:")
print(df.dtypes)
print("\nNull values:")
print(df.isnull().sum())
print("\nCleaning done successfully!")
# ── Fix numeric columns ──────────────────────────────────────────
numeric_cols = ['views', 'likes', 'dislikes', 'comment_count']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ── Drop rows with bad numeric data ─────────────────────────────
df.dropna(subset=numeric_cols, inplace=True)

# ── Convert to integer ───────────────────────────────────────────
for col in numeric_cols:
    df[col] = df[col].astype(int)

# ── Export to Excel for Power BI ─────────────────────────────────
df.to_excel("youtube_cleaned.xlsx", index=False)
print("\nExported to youtube_cleaned.xlsx!")