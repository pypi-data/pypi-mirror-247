from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.elements import ButtonObject

class CarouselObject:
    """
    This class represents a carousel object.
    """
    def __init__(self, imageUrl:str, title:str, subtitle:str, buttons:list['ButtonObject'], botId:str) -> None:
        from BotnoiDevPlatform.utils import ObjectType
        self.imageUrl = imageUrl
        self.title = title
        self.subtitle = subtitle
        self.buttons = buttons
        self.botId = botId
        self.objectType = ObjectType.carousel()

    @classmethod
    def from_json(cls, json:dict) -> "CarouselObject":
        """
        Create a new carousel from json representation.
        """
        from BotnoiDevPlatform.elements import ButtonObject
        buttons = [ButtonObject.from_json(button) for button in json["buttons"]]
        return cls(
            imageUrl=json["image_url"],
            title=json["title"],
            subtitle=json["subtitle"],
            buttons=buttons,
            botId=json["bot_id"] if "bot_id" in json else ""
        )

    def to_json(self) -> dict:
        """
        Convert this carousel to json representation.
        """
        return {
            "image_url": self.imageUrl,
            "title": self.title,
            "subtitle": self.subtitle,
            "buttons": [button.to_json() for button in self.buttons],
            "bot_id": self.botId
        }