class ButtonObject:
    """
    This class represents a Button object in the bot.
    """
    def __init__(self, data:str, label:str, type:"ButtonType") -> None:
        from BotnoiDevPlatform.utils import ObjectType
        self.data = data
        self.label = label
        self.type = type
        self.objectType = ObjectType.button()


    @classmethod
    def from_json(cls, json:dict) -> "ButtonObject":
        """
        Create a new button from json representation.
        """
        return cls(
            data=json["data"],
            label=json["label"],
            type=ButtonType(json["type"])
        )

    def to_json(self) -> dict:
        """
        Convert this button to json representation.
        """
        return {
            "data": self.data,
            "label": self.label,
            "type": self.type.string_type
        }


class ButtonType:
    def __init__(self, string_type:str) -> None:
        self.string_type = string_type

    @classmethod
    def message(cls) -> "ButtonType":
        return ButtonType("postback")

    @classmethod
    def url(cls) -> "ButtonType":
        return ButtonType("url")
    
    @classmethod
    def phone(cls) -> "ButtonType":
        return ButtonType("phone")
