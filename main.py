import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt

def fetch_news(company):
    print(f"\n[+] Fetching news for: {company}...")
    query = company.replace(" ", "+")
    url = f"https://www.bing.com/news/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.select("a.title")
    news = [headline.text.strip() for headline in headlines[:10]]

    if not news:
        print("[!] No news found — structure may have changed.")
    else:
        print("[+] Found headlines:")
        for h in news:
            print("-", h)

    return news


def analyze_sentiment(news_list):
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}
    for headline in news_list:
        blob = TextBlob(headline)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiments["positive"] += 1
        elif polarity < -0.1:
            sentiments["negative"] += 1
        else:
            sentiments["neutral"] += 1
        print(f"{headline} --> ({polarity:.2f})")
    return sentiments

def plot_sentiment(sentiments):
    labels = list(sentiments.keys())
    values = list(sentiments.values())
    colors = ['green', 'gray', 'red']
    plt.bar(labels, values, color=colors)
    plt.title("Sentiment Analysis of News Headlines")
    plt.ylabel("Count")
    plt.savefig("sentiment_chart.png")
    plt.show()

if __name__ == "__main__":
    company = input("Enter a company or stock name: ")
    news_list = fetch_news(company)
    sentiments = analyze_sentiment(news_list)
    plot_sentiment(sentiments)
