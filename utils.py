import requests
from openrouter_client import ChatOpenRouter
from langchain_core.messages import SystemMessage
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
        system_content = f"""
You are a social media expert who specializes in transforming news articles into concise tweets that resonate with a specific **niche** audience. Your job is to craft a tweet that follows a particular **tone and style**, based on provided examples.

**STRICT RULES — you must follow every one of them:**

1. The tweet **must be under 250 characters**.  
2. It **must clearly include the niche keyword** and feel directly relevant to the niche.  
3. The **tone and style must reflect the examples provided**.  
4. **Do NOT** mention or tag any accounts.  
5. **Do NOT** promote sessions, meetings, or events.  
6. **Do NOT** use emojis, hashtags, quotation marks, or any kind of markdown or formatting.  
7. **The final output must be plain text only** — no extra characters, no symbols, no formatting.

You are given examples of tweets to guide tone and style:

**Tone/Style Examples:**  
{past_tweets}

Now write one tweet that summarizes the following article for the niche using the required tone.

**Niche:** {niche}  
**Article:**  
{article_text}

**Output:** Only the tweet in plain text, under 250 characters, following all the rules above. No formatting. No additional commentary.
        """

    # If tone is provided, include it in the instructions
    elif tone is not None:
        system_content = f"""
You are a social media expert skilled at summarizing news articles into tweets tailored for specific audiences. Your task is to create a single tweet under 250 characters that sounds highly relevant to the specified **niche** and uses the required **tone**.  

**IMPORTANT RULES — follow them STRICTLY:**

1. The tweet **must include the niche keyword** naturally and clearly.  
2. Use the specified **tone** for the tweet.  
3. **Do NOT** mention or tag any accounts.  
4. **Do NOT** promote sessions, events, or meetings.  
5. **Do NOT** use quotes, hashtags, emojis, or markdown formatting.  
6. **The output must be plain text only** — no symbols, no quotation marks, no code blocks, no extra formatting.

Now, write a tweet under 250 characters summarizing the article below. Make it relevant to the niche with the niche keyword included, and write in the specified tone.

**Niche:** {niche}  
**Tone:** {tone}  
**Article:**  
{article_text}

**Output:** A single tweet in plain text only, strictly following all rules above.
        """

    print("System Content: ", system_content, "\n")

    # Initialize the ChatOpenRouter model
    chat = ChatOpenRouter(
        model="google/gemini-2.0-flash-exp:free",
        # model="google/gemini-2.0-flash-001",
        temperature=1,
    )

    messages = [SystemMessage(content=system_content)]

    response = chat.invoke(messages)
    print("Response: ", response, "\n")
    return response.content


def format_tweet(article, summary):
    tweet = summary
    return tweet[:280]
