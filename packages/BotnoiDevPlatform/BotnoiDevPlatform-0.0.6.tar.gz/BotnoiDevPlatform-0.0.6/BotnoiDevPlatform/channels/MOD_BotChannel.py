import json
import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
    from BotnoiDevPlatform.channels import FacebookPage
    from BotnoiDevPlatform.elements.MOD_Bot import Bot

class BotChannel:
    """
    The channel operator of a bot.
    """
    def __init__(self, bot:'Bot') -> None:
        self._bot = bot

    @classmethod
    def of(cls, bot:'Bot') -> "BotChannel":
        """
        Create a new bot channel operator.
        """
        return cls(bot)

    @property
    def _get_header(self):
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BotnoiClient.key()}",
        }

    def set_channel_activeStatus(self, channel:str, status:bool) -> None:
        """
        Set the status of a channel for this bot.
        - {channelName} is the name of the channel that you want to set the status. (eg. "line", "facebook")
        - {status} is the status of the channel that you want to set.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            if self._bot.id is None:
                raise Exception(
                    f"[set_channel_activeStatus] : bot '{self._bot.botName}' doesn't have an id, try reloading it")
                return
            url = f"{BotnoiClient.endpoint()}/bot/channel-active-status"
            response = requests.put(
                url,
                headers=self._get_header,
                json={
                    "bot_id": self._bot.id,
                    "channel": channel,
                    "status": status,
                },
            )
            if response.status_code in [200, 204, 201]:
                return
            raise Exception(f"[set_channel_activeStatus] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[set_channel_activeStatus] : {e}")

    def connect_to_line_modular(self, callbackUrl:str) -> str:
        """
        Connect this bot to a line channel with the "modular" approach.
        This will return a url that you can redirect the users to in order to connect this bot to their line channel.
        - {callbackUrl} is the url that will be called after the connection is completed, either successfully or not.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            if self._bot.id is None:
                raise Exception(
                    f"[connect_to_line_modular] : bot '{self._bot.botName}' doesn't have an id, try reloading it")
            url = f"{BotnoiClient.endpoint()}/connect/line-modular?bot_id={self._bot.id}&callback={callbackUrl}"
            response = requests.get(
                url,
                headers=self._get_header,
            )
            if response.status_code == 200:
                result = json.loads(response.content)
                return result["redirect_url"]
            raise Exception(f"[connect_to_line_modular] : {response.reason or 'ERROR'}")
            
        except Exception as e:
            raise Exception(f"[connect_to_line_modular] : {e}")

    def connect_to_line_manual(self, accessToken:str, secret:str) -> None:
        """
        Connect this bot to a line channel with the "manual" approach.
        - {accessToken} is the access token of the line channel.
        - {secret} is the secret of the line channel.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            if self._bot.id is None:
                raise Exception(
                    f"[connect_to_line_manual] : bot '{self._bot.botName}' doesn't have an id, try reloading it")
            url = f"{BotnoiClient.endpoint()}/connect/line-manual"
            assert isinstance(self._bot.channelActiveStatus, dict), "[connect_to_line_manual] : cannot access channelActiveStatus of the bot"
            response = requests.put(
                url,
                headers=self._get_header,
                json={
                    "bot_id": self._bot.id,
                    "first_token": accessToken,
                    "second_token": secret,
                    "active": len(list(self._bot.channelActiveStatus["line"])) > 0
                },
            )
            if response.status_code in [200, 204, 201]:
                return
            raise Exception(f"[connect_to_line_manual] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[connect_to_line_manual] : {e}")

    def disconnect_from_line(self) -> None:
        """
        Disconnect this bot from a connected line channel.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            if self._bot.id is None or self._bot.accessChannel is None:
                raise Exception(
                    f"[connect_to_line_manual] : bot '{self._bot.botName}' doesn't have an id, try reloading it")
                
            response = None
            if self._bot.accessChannel["line"]["first_token"]:
                url = f"{BotnoiClient.endpoint()}/connect/line-manual"
                response = requests.put(
                    url,
                    headers=self._get_header,
                    json={
                        "bot_id": self._bot.id,
                        "first_token": "",
                        "second_token": "",
                        "active": False,
                    },
                )
            elif self._bot.accessChannel["line_modular"]["bot_id"]:
                url = f"{BotnoiClient.endpoint()}/connect/line-modular/detach?bot_id={self._bot.id}"
                response = requests.delete(
                    url,
                    headers=self._get_header,
                )
            else:
                raise Exception(f"[disconnect_from_line] : bot '{self._bot.botName}' doesn't have a connected line channel")
            if response.status_code in [200, 204, 201]:
                return
            raise Exception(f"[disconnect_from_line] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[disconnect_from_line] : {e}")

    def connect_to_facebook(self, callbackUrl:str) -> str:
        """
        Connect this bot to a facebook channel. You will have to manually store the access token and the facebook user id that you get from the facebook login page using callbackUrl.
        - {callbackUrl} is the url that will be called after the connection is completed, either successfully or not. This url will have the access token and the facebook user id that you will have to save for later use.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            if self._bot.id is None:
                raise Exception(f"[connect_to_facebook] : bot '{self._bot.botName}' doesn't have an id, try reloading it")
            url = f"{BotnoiClient.endpoint()}/connect/facebook?callback={callbackUrl}"
            response = requests.post(
                url,
                headers=self._get_header,
            )
            if response.status_code in [200, 204, 201]:
                result = json.loads(response.content)
                return result["redirect_url"]
            raise Exception(f"[connect_to_facebook] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[connect_to_facebook] : {e}")

    def get_facebook_pages(self, fuid:str, accessToken:str) -> list['FacebookPage']:
        """
        Get the facebook pages that are connected to this bot.
        - {fuid} is the facebook user id that you get from the facebook login page using callbackUrl.
        - {accessToken} is the access token that you get from the facebook login page using callbackUrl.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        from BotnoiDevPlatform.channels.MOD_FacebookPage import FacebookPage
        try:
            if self._bot.id is None:
                raise Exception(
                    f"[get_facebook_pages] : bot '{self._bot.botName}' doesn't have an id, try reloading it")
            url = f"{BotnoiClient.endpoint()}/connect/facebook/page?uid={fuid}"
            response = requests.get(
                url,
                headers={**self._get_header, "X-Fb-User-Token": accessToken},
            )
            if response.status_code in [200, 204, 201]:
                result = json.loads(response.content)
                allPages = result["my_page"]["resource"]
                usedPages = result["used_page"]["resource"]
                found = []
                for e in allPages:
                    isUsed = any(element["page_id"] == e["page_id"] for element in usedPages)
                    page = {
                        **e,
                        "is_used": isUsed,
                    }
                    if isUsed:
                        page["bot_id"] = next(element["bot_id"] for element in usedPages if element["page_id"] == e["page_id"])
                        page["owner_id"] = next(element["owner_id"] for element in usedPages if element["page_id"] == e["page_id"])
                    found.append(FacebookPage.from_json(page))
                return found
            raise Exception(f"[get_facebook_pages] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[get_facebook_pages] : {e}")

    def subscribe_facebook_page(self, page:'FacebookPage', fuid:str, accessToken:str) -> None:
        """
        Subscribe this bot to a facebook page.
        - {page} is the page that you want to subscribe to.
        - {fuid} is the facebook user id that you get from the facebook login page using callbackUrl.
        - {accessToken} is the access token that you get from the facebook login page using callbackUrl.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            if self._bot.id is None:
                raise Exception(f"[subscribe_facebook_page] : bot '{self._bot.botName}' doesn't have an id, try reloading it")
            url = f"{BotnoiClient.endpoint()}/connect/facebook/page/subscribe?uid={fuid}&page_detail_id={page.pageId}?bot_id={self._bot.id}"
            response = requests.post(
                url,
                headers={**self._get_header, "X-Fb-User-Token": accessToken},
            )
            if response.status_code in [200, 204, 201]:
                return 
            raise Exception(f"[subscribe_facebook_page] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[subscribe_facebook_page] : {e}")

    def unsubscribe_facebook_page(self, page:'FacebookPage', fuid:str, accessToken:str) -> None:
        """
        Unsubscribe this bot from a facebook page.
        - {page} is the page that you want to unsubscribe from.
        - {fuid} is the facebook user id that you get from the facebook login page using callbackUrl.
        - {accessToken} is the access token that you get from the facebook login page using callbackUrl.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            if self._bot.id is None:
                raise Exception(
                    f"[unsubscribe_facebook_page] : bot '{self._bot.botName}' doesn't have an id, try reloading it")
                
            url = f"{BotnoiClient.endpoint()}/connect/facebook/page/subscribe?uid={fuid}&page_detail_id={page.pageId}?bot_id={self._bot.id}"
            response = requests.delete(
                url,
                headers={**self._get_header, "X-Fb-User-Token": accessToken},
            )
            if response.status_code in [200, 204, 201]:
                return 
            raise Exception(f"[unsubscribe_facebook_page] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[unsubscribe_facebook_page] : {e}")

    def disconnect_facbook(self, fuid:str, accessToken:str) -> None:
        """
        Disconnect facebook from this bot.
        - {fuid} is the facebook user id that you get from the facebook login page using callbackUrl.
        - {accessToken} is the access token that you get from the facebook login page using callbackUrl.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            if self._bot.id is None:
                raise Exception(f"[disconnect_facbook] : bot '{self._bot.botName}' doesn't have an id, try reloading it")
            url = f"{BotnoiClient.endpoint()}/connect/facebook/logout?uid={fuid}"
            response = requests.get(
                url,
                headers={**self._get_header, "X-Fb-User-Token": accessToken},
            )
            if response.status_code in [200, 204, 201]:
                return
            raise Exception(f"[disconnect_facbook] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[disconnect_facbook] : {e}")
