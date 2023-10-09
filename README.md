# About

Uses X's v2 API, Tweepy, Pandas, and Regex to extract tweets based on a user provided query. Data is written to an excel file as tweets are pulled.

The main python file uses the v2 Recent Search endpoint (https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent) to collect tweet text, post date, author information, mentions, and more.

# Prerequisites

Create a X Developer account: https://developer.twitter.com/en/products/twitter-api and create a v2 app. Generate appropriate tokens. This code uses App Only authentication: https://developer.twitter.com/en/docs/authentication/oauth-2-0/application-only

Install Tweepy in your python environment: https://docs.tweepy.org/en/stable/index.html

# Notes

The get_users_followers and get_users_following functions were degraded by X in June 2023: https://developer.twitter.com/en/updates/changelog. They are still included in the code with hopes the functionality will one day return!

