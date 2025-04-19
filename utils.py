import requests
from litellm import completion
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
import os


def fetch_config_from_appwrite():
    """Fetch configuration from Appwrite database using the provided API key."""

    endpoint = os.environ.get("APPWRITE_ENDPOINT")
    project = os.environ.get("APPWRITE_PROJECT")
    appwrite_key = os.environ.get("APPWRITE_API_KEY")
    database_id = os.environ.get("APPWRITE_DATABASE_ID")
    collection_id = os.environ.get("APPWRITE_CONFIG_COLLECTION_ID")

    client = Client()
    client.set_endpoint(endpoint)
    client.set_project(project)
    client.set_key(appwrite_key)

    # Initialize Appwrite database service
    databases = Databases(client)

    # Query the database for the document with the matching API key
    response = databases.list_documents(
        database_id=database_id,
        collection_id=collection_id,
    )

    # Return the first matching document
    if response["total"] > 0:
        print("Fetched configuration from Appwrite: ", response["documents"], "\n")
        return response["documents"]
    else:
        raise ValueError("No configuration found for the provided API key.")


def fetch_news(api_key, niche):
    """Fetch news articles for the given niche"""
    query = niche
    NEWS_URL = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(NEWS_URL)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return articles[:4]  # Get top 4 articles
    return []


def summarize_article(article_text, niche, tone=None, past_tweets=None):

    # Use past_tweets if provided
    if past_tweets is not None:
        system_content = f"You are a social media expert summarizing news articles into tweets. Make the tweets sound relevant to {niche}. Also do not tag any other accounts in tweets, or like do not even add about joining sessions or meetings.\n\n Here are some examples of tweets for tone and style:\n{past_tweets}\n\nNow, summarize the following news article into a tweet under 250 characters and it should have the niche part clearly with the niche keyword present in the tweet. Do not include any additional text such as 'here is the summary' nor quotations nor emojis nor anything else.\n\nArticle:\n{article_text}"

    # If tone is provided, include it in the instructions
    elif tone is not None:
        system_content = f"You are a social media expert summarizing news articles into tweets. Make the tweets sound relevant to {niche}. Also do not tag any other accounts in tweets, or like do not even add about joining sessions or meetings.\n\n The tone of the tweet should be {tone} tone.\n\nNow, summarize the following news article into a tweet under 250 characters with a {tone} tone and it should have the niche part clearly with the niche keyword present in the tweet. Do not include any additional text such as 'here is the summary' nor quotations nor emojis nor anything else.\n\nArticle:\n{article_text}"

    print("System Content: ", system_content, "\n")

    messages = [
        {
            "role": "system",
            "content": system_content,
        }
    ]

    response = completion(
        # model="openrouter/mistralai/mistral-small-3.1-24b-instruct-2503",
        model="openrouter/qwen/qwen-2.5-72b-instruct:free",
        messages=messages,
        temperature = 1
    )
    return response.choices[0].message.content


def format_tweet(article, summary):
    # tweet = f"{summary} \n\nRead more: {article['url']}"
    tweet = summary
    return tweet[:280]  # Ensure it doesn't exceed 280 characters
