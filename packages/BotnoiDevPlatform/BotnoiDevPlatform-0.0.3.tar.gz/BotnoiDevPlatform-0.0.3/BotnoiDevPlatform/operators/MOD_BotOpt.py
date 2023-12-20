import json
import requests
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.elements import Bot
    from BotnoiDevPlatform.elements import Object
    from BotnoiDevPlatform.elements import Intent
    from BotnoiDevPlatform.utils import ObjectType

class BotOperator:
    """
    The operator of a bot.

    This is used for creating, updating, and deleting intents and objects of a bot.
    """

    def __init__(self, bot:'Bot') -> None:
        self._bot = bot

    @classmethod
    def of(cls, bot:'Bot') -> 'BotOperator':
        """
        Create a new bot operator from a bot.
        """
        return cls(bot)

    @property
    def _get_header(self):
        from BotnoiDevPlatform.cores import BotnoiClient
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BotnoiClient.key()}",
        }

    def create_intent(self, intent: 'Intent', derived:bool=False, source:Union['Intent',None] = None, mapping:dict={}) -> None:
        """
        Create a new intent for this bot.
        - {intent} is the intent that you want to create.
        - {derived} is a boolean that indicate whether you want to derive this intent from an existing intent. If this is true, {source} must also be provided.
        - {source} is the intent that you want to derive from. This is only required if {derived} is true.
        - {mapping} is used to replace placeholders in the keywords and reactions when deriving from an existing intent.

        notice that placeholders must be surrounded by curly braces.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            intent.belong_to_bot(self._bot)
            url = f"{BotnoiClient.endpoint()}/intent"
            response = requests.post(
                url,
                headers=self._get_header,
                data=json.dumps(intent.to_json()),
            )
            if response.status_code == 201:
                
                if derived:
                    if source is None:
                        raise Exception("[create_intent] : If derived is true, source must be provided")
                    if source.id is None:
                        raise Exception("[create_intent] : source intent must have an id")
                    newIntent = self.find_intent_with_name(intent.name)
                    if newIntent is None:
                        return
                    newIntent.opt.derive_from_intent(source=source, mapping=mapping)
                return
            raise Exception("[create_intent] : " + response.reason if response.reason else "ERROR")
        except Exception as e:
            raise Exception("[create_intent] : " + str(e))

    def find_intents(self) -> list['Intent']:
        """
        Find all intents of this bot.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        from BotnoiDevPlatform.elements import Intent
        try:
            url = f"{BotnoiClient.endpoint()}/intent?bot_id={self._bot.id}"
            response = requests.get(
                url,
                headers=self._get_header,
            )
            if response.status_code == 200:
                result = json.loads(response.content.decode("utf-8"))
                found = [Intent.from_json(e) for e in result["data"]]
                for intent in found:
                    intent.belong_to_bot(self._bot)
                return found
            raise Exception("[find_intents] : " + response.reason if response.reason else "ERROR")
        except Exception as e:
            raise Exception("[find_intents] : " + str(e))          

    def find_intent_with_name(self, name:str) -> 'Intent':
        """
        Find an intent in this bot with a specific name.
        - {name} is the name of the intent that you want to find.
        """
        allIntents = self.find_intents()
        try:
            found = next((element for element in allIntents if element.name == name), None)
            if found is None:
                raise Exception("[find_intent_with_name] : intent not found")
            return found
        except Exception as e:    
            raise Exception("[find_intent_with_name] : " + str(e))    

    def update_intent(self, intent:'Intent') -> None:
        """
        Update an intent of this bot.
        - {intent} is the updated version of the intent that you want to update (intent's id must not be changed).
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            if intent.id is None:
                raise Exception("[update_intent] : this intent has no id")
            intent.belong_to_bot(self._bot)
            url = f"{BotnoiClient.endpoint()}/intent"
            response = requests.put(
                url,
                headers=self._get_header,
                data=json.dumps(intent.to_json()),
            )
            if response.status_code == 200 or response.status_code == 204:
                return
            raise Exception("[update_intent] : " + response.reason if response.reason else "ERROR")
        except Exception as e:
            raise Exception("[update_intent] : " + str(e))

    def delete_intents(self, intents:list['Intent']) -> None:
        """
        Delete intents of this bot.
        - {intents} is the list of intents that you want to delete.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            url = f"{BotnoiClient.endpoint()}/intent"
            response = requests.delete(
                url,
                headers=self._get_header,
                data=json.dumps({
                    "bot_id": self._bot.id,
                    "ids": [e.id for e in intents],
                }),
            )
            if response.status_code == 200 or response.status_code == 204:
                return
            raise Exception("[delete_intents] : " + response.reason if response.reason else "ERROR")
        except Exception as e:
            raise Exception("[delete_intents] : " + str(e))

    def create_object(self, object: 'Object') -> None:
        """
        Create a new object for this bot.

        In Botnoi Chatbot, objects are anything that you want your bot to use that isn't text (eg. images, audio, flex message, buttons, api, etc.).
        - {object} is the object that you want to create.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            object.belong_to_bot(self._bot)
            url = f"{BotnoiClient.endpoint()}/object/{object.objectType.stringType}"
            response = requests.post(
                url,
                headers=self._get_header,
                data=json.dumps(object.to_json()),
            )
            if response.status_code == 201:
                return
            raise Exception("[create_object] : " + response.reason if response.reason else "ERROR")
        except Exception as e:
            raise Exception("[create_object] : " + str(e))

    def find_objects(self, type: 'ObjectType') -> list['Object']:
        """
        Find all objects of this bot with a specific type.
        - {type} is the type of object that you want to find.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        from BotnoiDevPlatform.elements import Object
        try:
            url = f"{BotnoiClient.endpoint()}/object/{type.stringType}?bot_id={self._bot.id}"
            response = requests.get(
                url,
                headers=self._get_header,
            )
            if response.status_code == 200:
                result = json.loads(response.content.decode("utf-8"))
                found = [Object.from_json(e, botId=self._bot.id) for e in result]
                for o in found:
                    o.belong_to_bot(self._bot)
                return found
            raise Exception("[find_objects] : " + response.reason if response.reason else "ERROR")
        except Exception as e:
            raise Exception("[find_objects] : " + str(e))
            
    def find_object_with_name(self, name:str, type: 'ObjectType') -> 'Object':
        """
        Find an object in this bot with a specific name and type.
        - {name} is the name of the object that you want to find.
        - {type} is the type of object that you want to find.
        """
        from BotnoiDevPlatform.utils import ObjectNamer
        allObjects = self.find_objects(type=type)
        try:
            found = next((element for element in allObjects if element.objectName == ObjectNamer.by_action(name, type)), None)
            if not found:
                raise Exception("[find_object_with_name] : object not found")
            return found
        except Exception as e: 
            raise Exception("[find_object_with_name] : " + str(e))           

    def update_object(self, object: 'Object') -> None:
        """
        Update an object of this bot.
        - {object} is the updated version of the object that you want to update (object's id must not be changed).
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            if object.id is None:
                raise Exception("[update_object] : this object has no id")
            object.belong_to_bot(self._bot)
            url = f"{BotnoiClient.endpoint()}/object/{object.objectType.stringType}"
            response = requests.put(
                url,
                headers=self._get_header,
                data=json.dumps(object.to_json()),
            )
            if response.status_code == 200 or response.status_code == 204 or response.status_code == 201:
                return
            raise Exception("[update_object] : " + response.reason if response.reason else "ERROR")
        except Exception as e:
            raise Exception("[update_object] : " + str(e))

    def delete_objects(self, objects: list['Object']) -> None:
        """
        Delete objects of this bot.
        - {objects} is the list of objects that you want to delete. All objects must be the same type.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            for object in objects:
                if object.id is None:
                    raise Exception("[delete_objects] : this object has no id")
                if object.objectType.stringType != objects[0].objectType.stringType:
                    raise Exception("[delete_objects] : all objects must be the same type")
                object.belong_to_bot(self._bot)
            url = f"{BotnoiClient.endpoint()}/object/{objects[0].objectType.stringType}"
            response = requests.delete(
                url,
                headers=self._get_header,
                data=json.dumps({
                    "_id": [e.id for e in objects],
                    "bot_id": self._bot.id,
                }),
            )
            if response.status_code == 200 or response.status_code == 204:
                return
            raise Exception("[delete_objects] : " + response.reason if response.reason else "ERROR")
        except Exception as e:
            raise Exception("[delete_objects] : " + str(e))

    def train_chitchat(self, keyword:str, reaction:str) -> None:
        """
        Train a chitchat for this bot. "Chitchat" is non-intent-based conversation that can be trained using a keyword-reaction pair.
        - {keyword} is the text recieved from the users.
        - {reaction} is the text that the bot will respond to the users.
        """
        from BotnoiDevPlatform.cores import BotnoiClient
        try:
            url = f"{BotnoiClient.endpoint()}/training/chitchat"
            response = requests.post(
                url,
                headers=self._get_header,
                data=json.dumps({
                    "bot_id": self._bot.id,
                    "keyword": keyword,
                    "response": reaction,
                }),
            )
            if response.status_code == 200:
                return
            raise Exception("[train_chitchat] : " + response.reason if response.reason else "ERROR")
        except Exception as e:
            raise Exception("[train_chitchat] : " + str(e))