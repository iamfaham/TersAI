# TersAI

## Description

TersAI is an AI-powered Twitter bot that automates the process of gathering and sharing news updates in a specific niche. It fetches the latest articles from the web, summarizes them into concise, tweet-sized content using a language model, adapts the writing tone to match a target Twitter profile's style, and then posts the result to Twitter automatically. The goal is to consistently deliver relevant updates (especially AI news) in the desired tone to an audience on Twitter.

## Features

- **Automated Article Fetching:** Retrieves the latest news articles via the NewsAPI based on configured topics.
- **AI Summarization:** Uses a language model to condense each article into a tweetable summary using LangChain and OpenRouter.
- **Tone Adaptation:** Matches the tweet's tone to a target persona using example tweets or provided tone descriptions.
- **Automated Tweet Posting:** Posts the generated tweets automatically using Twitter's API.
- **Multi-Profile Support:** Supports multiple Twitter accounts and configurations using Appwrite as a config store.

## Installation

1. **Clone the Repository & Install Dependencies**
   ```bash
   git clone https://github.com/iamfaham/TersAI.git
   cd TersAI
   pip install -r requirements.txt
   ```

2. **Obtain API Keys**
   - Twitter API Key, Secret, Access Token, and Access Secret
   - NewsAPI Key
   - OpenRouter API Key
   - Appwrite API Key (if using Appwrite)

3. **Configure Environment Variables**
   Create a `.env` file or export variables:
   ```bash
   APPWRITE_ENDPOINT=<your-appwrite-endpoint>
   APPWRITE_PROJECT=<your-appwrite-project-id>
   APPWRITE_API_KEY=<your-appwrite-api-key>
   APPWRITE_DATABASE_ID=<your-appwrite-database-id>
   APPWRITE_CONFIG_COLLECTION_ID=<your-config-collection-id>

   NEWS_API_KEY=<your-newsapi-key>
   OPENROUTER_API_KEY=<your-openrouter-key>
   ```

4. **Set Up Appwrite Configuration**
   In Appwrite, create a collection with documents having fields:
   - `X_API_KEY`
   - `X_API_SECRET`
   - `X_ACCESS_TOKEN`
   - `X_ACCESS_SECRET`
   - `Topics`
   - `Tone`
   - `Past_tweets` (optional)

## Usage

- **Local**
   ```bash
   python bot.py
   ```

- **GitHub Actions**
   - Add your secrets to GitHub repository settings.
   - Enable the included GitHub Actions workflow in `.github/workflows/run-bot.yml`.

## Folder Structure

```
TersAI/
├── bot.py                   # Main script
├── utils.py                 # Helper functions
├── openrouter_client.py     # OpenRouter wrapper for LangChain
├── requirements.txt         # Dependencies
└── .github/
    └── workflows/
        └── run-bot.yml      # GitHub Actions workflow
```

## Contributing

Contributions are welcome! Open an issue to discuss improvements or bugs. Submit pull requests for enhancements.

## License

No license file provided. Use is considered proprietary by default.

## Contact

Created by **Syed Mohammed Faham**  
GitHub: [@iamfaham](https://github.com/iamfaham)  
Bot live at: [@TersXAI on Twitter](https://x.com/TersXAI)
