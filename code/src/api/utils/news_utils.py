import feedparser
import re
import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import List, Dict, Tuple

nltk.download('vader_lexicon')


class NewsUtils:
    """
    A utility class for fetching and analyzing financial news articles.

    Methods:
        get_google_news(company: str, keywords: str) -> List[Dict]:
            Fetches news articles from Google News RSS for a given company and keywords.

        compute_risk_and_confidence(article: Dict) -> Tuple[float, float]:
            Computes the risk score and confidence for a news article based on its headline.

        filter_top_negative_news(news_list: List[Dict], top_n: int = 5) -> List[Dict]:
            Filters and sorts the given list of news articles to return the top negative articles.
    """

    @staticmethod
    def get_google_news(company: str, keywords: str) -> List[Dict]:
        """
        Fetches news articles from Google News RSS based on the company and keywords.

        Args:
            company (str): The name of the company (e.g., 'Adani Enterprises Limited').
            keywords (str): Keywords to include in the search (e.g., 'money laundering fraud scandal bribery').

        Returns:
            List[Dict]: A list of articles, each represented as a dictionary containing 'title', 'link', and 'published'.
        """
        query = f"{company} {keywords}".replace(" ", "+")
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return [{"title": entry.title, "link": entry.link, "published": entry.published} for entry in feed.entries if
                company.lower() in entry.title.lower()]

    @staticmethod
    def compute_risk_and_confidence(article: Dict) -> Tuple[float, float]:
        """
        Computes a risk score and confidence level for a news article based on its headline.

        Risk Score:
            If the headline is negative, risk = abs(compound score) * 100, otherwise 0.
        Confidence:
            Derived from the negative sentiment proportion (neg * 100).

        Args:
            article (Dict): A dictionary representing a news article with at least a 'title' key.

        Returns:
            Tuple[float, float]: A tuple containing the risk score and confidence.
        """
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(article['title'])
        risk = abs(min(0, sentiment['compound'])) * 100
        confidence = sentiment['neg'] * 100
        return risk, confidence

    @staticmethod
    def filter_top_negative_news(news_list: List[Dict], top_n: int = 5) -> List[Dict]:
        """
        Computes risk scores for all articles, filters out those with no negative risk,
        sorts them in descending order by risk, and returns the top_n articles.

        Args:
            news_list (List[Dict]): A list of news articles.
            top_n (int): The number of top negative articles to return.

        Returns:
            List[Dict]: A list of the top negative news articles, each augmented with 'neg_sentiment_score' and 'confidence'.
        """
        news_with_scores = []
        for article in news_list:
            risk, confidence = NewsUtils.compute_risk_and_confidence(article)
            article['neg_sentiment_score'] = risk
            article['confidence'] = confidence
            news_with_scores.append(article)
        negative_articles = [article for article in news_with_scores if article['neg_sentiment_score'] > 0]
        negative_articles.sort(key=lambda x: x['neg_sentiment_score'], reverse=True)

        return negative_articles[:top_n]


if __name__ == "__main__":
    company_name = "Deutsche Bank"
    keywords = "money laundering OR fraud OR tax evasion OR corruption OR scandal"
    news_articles = NewsUtils.get_google_news(company_name, keywords)
    print("Fetched News Articles:")
    for article in news_articles:
        print(f"Title: {article['title']}")
    top_negative_news = NewsUtils.filter_top_negative_news(news_articles, top_n=3)
    print("\nTop Negative News Articles:")
    for article in top_negative_news:
        risk, conf = NewsUtils.compute_risk_and_confidence(article)
        print(f"Title: {article['title']}")
        print(f"Risk Score: {risk:.2f}, Confidence: {conf:.2f}")
        print(f"Link: {article['link']}")
        print(f"Published: {article['published']}\n")
