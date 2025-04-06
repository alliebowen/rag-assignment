import os
from newspaper import Article

# List of article URLs
urls = [
    "https://www.pewresearch.org/internet/2013/01/28/tracking-for-health/"

]

# Make output folder if it doesn't exist
os.makedirs("docs", exist_ok=True)

for i, url in enumerate(urls):
    try:
        article = Article(url)
        article.download()
        article.parse()

        # Clean title for filename (fallback if empty)
        title = article.title.strip().replace(" ", "_").replace("/", "_")
        filename = f"docs/article_{i+1}_{title or 'untitled'}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(article.text)

        print(f"✅ Saved: {filename}")
    except Exception as e:
        print(f"❌ Failed to process {url}: {e}")
