import feedparser
from hashlib import sha256
from datetime import datetime
from database import NewsArticle, Session

def parse_rss(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        content_hash = sha256(entry.content.encode('utf-8')).hexdigest()
        if not Session.query(NewsArticle).filter_by(content_hash=content_hash).first():
            pub_date = datetime.fromtimestamp(entry.published_parsed)
            articles.append({
                'title': entry.title,
                'content': entry.content,
                'pub_date': pub_date,
                'source_url': entry.link
            })

    return articles

def parse_rss_with_error_handling(feed_url):
    try:
        return parse_rss(feed_url)
    except Exception as e:
        logging.error(f"Error parsing feed {feed_url}: {str(e)}")
        return []
