# Simple AI Discord Bot

This discord bot provides a slash command for interfacing with any AI via and OpenAI compatable endpoint.

## How to use

Supply the needed environment variables in the `.env` file.
```
DISCORD_TOKEN=
OPENAI_API_URL=
OPENAI_API_KEY=
AI_MODEL=
```

After you've added the bot to your server you can invoke it with `/ai` and provide a prompt.

## About hosting

The provided Docker file allows you to host the bot on fly.io.
