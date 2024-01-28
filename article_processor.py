import nltk
from celery import Celery
from feed_parser import parse_feed
from database import connect_to_database, close_database_connection, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import logging
from sklearn.naive_bayes import MultinomialNB  
from sklearn.feature_extraction.text import CountVectorizer
from config import categories

logging.basicConfig(filename='news_app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Celery('article_processor', broker='pyamqp://guest:guest@localhost//')

@app.task
def process_article(title, content, published, url):
    
    try:
        text = preprocess_text(content)

        category = classify_article(text)

        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cur = conn.cursor()

        sql = """INSERT IGNORE INTO news_articles (title, content, published, url, category) VALUES (%s, %s, %s, %s, %s)"""
        cur.execute(sql, (title, content, published, url, category))
        conn.commit()

        logger.info(f"Article '{title}' classified as {category} and stored in database.")

    except Exception as e:
        logger.error(f"Error processing article: {e}")

    finally:
        if conn:
            conn.close()


def preprocess_text(text):
    
    words = nltk.word_tokenize(text.lower())  

    stop_words = set(nltk.corpus.stopwords.words('english'))  
    words = [word for word in words if word not in stop_words]

    stemmer = nltk.PorterStemmer()  
    words = [stemmer.stem(word) for word in words]

    preprocessed_text = " ".join(words)

    return preprocessed_text


def classify_article(text):
    features = vectorizer.transform([text])  
    category = classifier.predict(features)[0]  
    return category


def train_classifier(labeled_data):

    vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform([text for text, _ in labeled_data])
    y_train = [label for _, label in labeled_data]

    classifier = MultinomialNB()  
    classifier.fit(x_train, y_train)  

    return classifier, vectorizer