import asyncio

from application.app import running_bot

if __name__ == "__main__":
    asyncio.run(running_bot.run_server())
