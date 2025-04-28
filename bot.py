import time
import json
from requests_oauthlib import OAuth1Session
import os
from utils import (
    fetch_news,
    summarize_article,
    format_tweet,
    fetch_config_from_appwrite,
)


NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def post_tweet(tweet_text):
    """Post a tweet using Twitter API v2"""
    # Set up OAuth1Session
    oauth = OAuth1Session(
        X_API_KEY,
        client_secret=X_API_SECRET,
        resource_owner_key=X_ACCESS_TOKEN,
        resource_owner_secret=X_ACCESS_SECRET,
    )

    # Create payload with tweet text
    payload = {"text": tweet_text}

    # Make the API request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    # Check if the request was successful
    if response.status_code != 201:
        print(f"Error posting tweet: {response.status_code} {response.text}")
        return False

    # Print success message
    print("Tweet posted successfully!")
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))
    return True


def is_niche_related(article, summary, niche_keywords):
    """Check if the article is genuinely about the given niche"""
    summary = summary or ""

    # Combine title, description, and summary text for checking
    text_to_check = (
        article.get("title", "") + " " + article.get("description", "") + " " + summary
    ).lower()

    # Convert text to a proper format for word boundary checking
    text_to_check = " " + text_to_check + " "

    # Check if any niche keyword is present (with word boundaries)
    for keyword in niche_keywords:
        search_term = f" {keyword} "
        if search_term in text_to_check:
            print(f"Niche keyword found: '{keyword}' in article")
            return True

    print("No niche keywords found in article")
    return False


def run_bot():
    # Fetch configuration from Appwrite
    configs = fetch_config_from_appwrite()

    if not configs:
        print("No configurations found.")
        return

    for config in configs:
        print(f"Running bot for config: {config.get('X_API_KEY')}")
        # Populate variables
        global X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET, tone, past_tweets
        X_API_KEY = config["X_API_KEY"]
        X_API_SECRET = config["X_API_SECRET"]
        X_ACCESS_TOKEN = config["X_ACCESS_TOKEN"]
        X_ACCESS_SECRET = config["X_ACCESS_SECRET"]
        tone = config["Tone"]
        past_tweets = config["Past_tweets"]

        # Convert the comma-separated topics string into a list
        topics = [topic.strip() for topic in config["Topics"].split(",")]

        # Fetch the news for the first topic in the list
        primary_topic = topics[0]
        news = fetch_news(NEWS_API_KEY, primary_topic)

        articles_posted = 0
        candidate_tweets = []
        # For each article, summarize and collect candidates with a keyword score
        for article in news:
            print("Processing article:", article.get("title", "No title"))
            summary = summarize_article(
                article["content"],
                primary_topic,
                tone,
                past_tweets,
            )

            # Check if the article is related to any topic in the list
            niche_keywords = [t.lower() for t in topics]
            if not is_niche_related(article, summary, niche_keywords):
                print(f"Skipping article: {article.get('title', 'No title')}")
                continue

            tweet = format_tweet(article, summary)
            print("Tweet candidate:", tweet)

            # Prepare text for keyword counting (using title, description, and summary)
            text_to_check = (
                article.get("title", "")
                + " "
                + article.get("description", "")
                + " "
                + summary
            ).lower()
            text_to_check = " " + text_to_check + " "
            # Count how many distinct keywords appear
            keyword_count = sum(
                1 for keyword in niche_keywords if f" {keyword} " in text_to_check
            )
            candidate_tweets.append((keyword_count, tweet))

        # Select the candidate tweet with the highest keyword count
        if candidate_tweets:
            best_candidate = max(candidate_tweets, key=lambda x: x[0])
            best_tweet = best_candidate[1]
            print("Best tweet selected based on keywords:")
            print("Tweet:", best_tweet)

            retries = 3
            while retries > 0:
                success = post_tweet(best_tweet)
                # success = True
                if success:
                    articles_posted += 1
                    break
                retries -= 1
                print("Retrying to post the tweet...")
                time.sleep(15)  # Wait before retrying

        print(
            f"Bot run complete for config {config.get('X_API_KEY')}. Posted {articles_posted} articles for topics: {', '.join(topics)}.\n"
        )


# Call the run_bot function directly when the script is executed
if __name__ == "__main__":
    print("Running the bot...")
    run_bot()
