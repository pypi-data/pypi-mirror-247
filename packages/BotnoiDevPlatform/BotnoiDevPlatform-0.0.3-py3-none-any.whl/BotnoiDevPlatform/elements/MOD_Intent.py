from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.operators import IntentOperator
    from BotnoiDevPlatform.elements import Bot

class Intent:
    """
    This class represents an intent in the bot
    """
    def __init__(self, name:str, id:Union[str,None] = None) -> None:
        self.name = name
        self.id = id

    @classmethod
    def from_json(cls, json:dict) -> "Intent":
        """
        Create a new intent from json representation.
        """
        return cls(
            id=json["_id"],
            name=json["name"]
        )

    def to_json(self) -> dict:
        """
        Convert this intent to json representation.
        """
        json = {
            "name": self.name
        }
        if self.id is not None:
            json["_id"] = self.id
        if self.bot is not None and self.bot.id is not None:
            json["bot_id"] = self.bot.id
        return json

    def belong_to_bot(self, bot:'Bot') -> None:
        """
        Set the bot that this intent belongs to.
        """
        self.bot = bot

    @property
    def opt(self) -> 'IntentOperator':
        """
        The operator of this intent.
        """
        from BotnoiDevPlatform.operators import IntentOperator
        if self.bot is not None:
            return IntentOperator.of(self, self.bot)
        else:
            raise Exception("bot is not specified for this intent")

    def reload(self) -> None:
        """
        Reload this intent from the server, keeping it up to date.
        """
        if self.bot is None:
            raise Exception("bot is not specified for this intent")
        loaded_intent = self.bot.opt.find_intent_with_name(self.name)
        if loaded_intent is not None:
            self.id = loaded_intent.id
            self.name = loaded_intent.name
            self.bot = loaded_intent.bot
        else:
            raise Exception("intent not found")