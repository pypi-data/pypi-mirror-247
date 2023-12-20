from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.elements import Intent
    from BotnoiDevPlatform.elements import Bot

class IntentKeyword:
    """
    This class represents a keyword in an intent.
    """
    def __init__(self, keyword:str, intentName:Union[str,None] = None, id:Union[str,None] = None) -> None:
        self.keyword = keyword
        self.intentName = intentName
        self.id = id

    @classmethod
    def from_json(cls, json:dict) -> "IntentKeyword":
        """
        Create a new keyword from json representation.
        """
        return cls(
            id=json["_id"],
            intentName=json["intent"],
            keyword=json["keyword"],
        )

    def to_json(self) -> dict:
        """
        Convert this keyword to json representation.
        """
        json = {
            "keyword": self.keyword,
        }
        if self.id is not None:
            json["_id"] = self.id
        if self.intentName is not None:
            json["intent"] = self.intentName
        if self.bot is not None and self.bot.id is not None:
            json["bot_id"] = self.bot.id
        return json

    def belong_to_intent(self, intent: 'Intent') -> None:
        """
        Set the intent that this keyword belongs to.
        """
        self.intentName = intent.name

    def belong_to_bot(self, bot:'Bot') -> None:
        """
        Set the bot that this keyword belongs to.
        """
        self.bot = bot
