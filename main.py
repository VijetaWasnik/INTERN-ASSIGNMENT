from article_processor import process_article
from feed_parser import parse_feed
from database import connect_to_database, close_database_connection
import mysql.connector

feeds = ["http://rss.cnn.com/rss/cnn_topstories.rss", "http://qz.com/feed", "http://feeds.foxnews.com/foxnews/politics"]

if __name__ == "__main__":
    seen_articles = set()  

    for feed_url in feeds:
        for title, content, published, url in parse_feed(feed_url):
            process_article.delay(title, content, published, url)

    conn = connect_to_database()
    close_database_connection(conn)
