from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.elements import Intent
    from BotnoiDevPlatform.elements import Bot

class IntentReaction:
    """
    This class represents a reaction in an intent.
    """
    def __init__(self, actions:list[str], intentName:Union[str,None] = None, id:Union[str,None] = None, objects:Union[list[dict],None]=None, selected:Union[bool,None]=None) -> None:
        self.actions = actions
        self.intentName = intentName
        self.id = id
        self.objects = objects
        self.selected = selected

    @classmethod
    def from_json(cls, json: dict) -> "IntentReaction":
        """
        Create a new reaction from json representation.
        """
        return cls(
            id=json["_id"],
            intentName=json["intent"],
            actions=str(json["message"]).split("|||"),
            objects=[{k: v for k, v in e.items()} for e in json["objects"]],
            selected=json["selected"] == "true"
        )

    def to_json(self) -> dict:
        """
        Convert this reaction to json representation.
        """
        json = {
            "_id": self.id,
            "message": "|||".join(self.actions),
            "intent": self.intentName
        }
        if self.objects:
            json["objects"] = self.objects
        if self.selected is not None:
            json["selected"] = self.selected
        if self.bot is not None and self.bot.id is not None:
            json["bot_id"] = self.bot.id
        return json

    def belong_to_intent(self, intent: 'Intent') -> None:
        """
        Set the intent that this reaction belongs to.
        """
        self.intentName = intent.name

    def belong_to_bot(self, bot: 'Bot') -> None:
        """
        Set the bot that this reaction belongs to.
        """
        self.bot = bot
