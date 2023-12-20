import json
import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.elements import Bot

class BotnoiChatbotServer:
    """
    This class represents the botnoi chatbot server.
    """

    @staticmethod
    def setup_client(key:str, endpoint:str="https://api-gateway.botnoi.ai/developer/platform-api"):
        from BotnoiDevPlatform.cores import BotnoiClient
        BotnoiClient.setup(key=key, endpoint=endpoint)

    @property
    def _get_header(self):
        from BotnoiDevPlatform.cores import BotnoiClient
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BotnoiClient.key()}",
        }
    
    def create_bot(self, bot: 'Bot') -> None:
        """
        Create a new bot for this botnoi chatbot server.
        - {bot} is the bot that you want to create.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            url = f"{BotnoiClient.endpoint()}/bot"
            response = requests.post(
                url,
                headers=self._get_header,
                data=json.dumps(bot.to_json()),
            )
            if response.status_code in [201, 200, 204]:
                return
            raise Exception(f"[create_bot] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[create_bot] : {e}")

    def update_bot(self, bot: 'Bot') -> None:
        """
        Update a bot in this botnoi chatbot server.
        - {bot} is the updated version of the bot that you want to update (bot's id must not be changed).
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            if bot.id is None:
                raise Exception(f"[update_bot] : bot {bot.botName} doesn't have an id, try reloading it")
            url = f"{BotnoiClient.endpoint()}/bot"
            response = requests.put(
                url,
                headers=self._get_header,
                data=json.dumps(bot.to_json()),
            )
            if response.status_code in [200, 204]:
                return
            raise Exception(f"[update_bot] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[update_bot] : {e}")

    def find_bots(self) -> list['Bot']:
        """
        Find all bots in this botnoi chatbot server.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        from BotnoiDevPlatform.elements import Bot
        try:
            url = f"{BotnoiClient.endpoint()}/bot"
            response = requests.get(
                url,
                headers=self._get_header,
            )
            if response.status_code == 200:
                result = json.loads(response.content.decode())
                return [Bot.from_json(e) for e in result["data"]]         
            raise Exception(f"[find_bots] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[find_bots] : {e}")
        
    def find_bot_with_name(self, name:str) -> 'Bot':
        """
        Find a bot in this botnoi chatbot server with a specific name.
        - {name} is the name of the bot that you want to find.
        """
        all_bots = self.find_bots()
        try:
            found = next((bot for bot in all_bots if bot.botName == name), None)
            if not found:
                raise Exception(f"[find_bot_with_name] : bot with name '{name}' not found")
            return found
        except Exception as e:
            raise Exception(f"[find_bot_with_name] : {e}")

    def delete_bot(self, bot:'Bot') -> None:
        """
        Delete a bot in this botnoi chatbot server.
        - {bot} is the bot that you want to delete.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            if bot.id is None:
                raise Exception(f"[delete_bot] : bot {bot.botName} doesn't have an id, try reloading it")
            url = f"{BotnoiClient.endpoint()}/bot"
            response = requests.delete(
                url,
                headers=self._get_header,
                data=json.dumps(bot.to_json()),
            )
            if response.status_code in [200, 204]:
                return
            raise Exception(f"[delete_bot] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[delete_bot] : {e}")
