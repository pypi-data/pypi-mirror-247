from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.elements import Bot
    from BotnoiDevPlatform.elements import ImageObject
    from BotnoiDevPlatform.elements import AudioObject
    from BotnoiDevPlatform.elements import ApiObject
    from BotnoiDevPlatform.elements import ButtonObject
    from BotnoiDevPlatform.elements import CustomPayloadObject
    from BotnoiDevPlatform.elements import DialogueObject
    from BotnoiDevPlatform.elements import CarouselObject
    from BotnoiDevPlatform.utils import ObjectType

class Object:
    """
    This class represents an object in the bot
    """
    def __init__(self,
        objectName:str, 
        objects:list[Union['ImageObject','AudioObject','ApiObject','ButtonObject','CustomPayloadObject','DialogueObject','CarouselObject']], 
        objectType:Union['ObjectType',None] = None,
        bypassNamer:bool = False,
        ) -> None:
        from BotnoiDevPlatform.utils import ObjectNamer
        if not objects:
            raise Exception("Objects list cannot be empty")
        self.objects = objects
        if not bypassNamer:
            self.objectName = ObjectNamer.by_action(objectName, objectType or objects[0].objectType)
        else:
            self.objectName = objectName
        if not objectType:
            self.objectType = objects[0].objectType
        else:
            self.objectType = objectType

    @classmethod
    def from_json(cls, json:dict, botId:Union[str,None]=None) -> "Object":
        """
        Create a new object from json representation.
        """
        from BotnoiDevPlatform.elements import ImageObject
        from BotnoiDevPlatform.elements import AudioObject
        from BotnoiDevPlatform.elements import ApiObject
        from BotnoiDevPlatform.elements import ButtonObject
        from BotnoiDevPlatform.elements import CustomPayloadObject
        from BotnoiDevPlatform.elements import DialogueObject
        from BotnoiDevPlatform.elements import CarouselObject

        _objectFromJson = {
            "image": lambda json: ImageObject.from_json(json),
            "audio": lambda json: AudioObject.from_json(json),
            "api": lambda json: ApiObject.from_json(json),
            "button": lambda json: ButtonObject.from_json(json),
            "customPayload": lambda json: CustomPayloadObject.from_json(json),
            "dialogue": lambda json: DialogueObject.from_json(json),
            "carousel": lambda json: CarouselObject.from_json(json),
        }
        
        return cls(
            objectName=json["object_name"],
            objects=[_objectFromJson[str(json["type"])]({**e,"bot_id": botId}) for e in json["list_object"]],
            bypassNamer=True,
        )

    def to_json(self) -> dict:
        """
        Convert this object to json representation.
        """
        json = {
            "object_name": self.objectName,
            "type": self.objectType.stringType,
            "list_object": [e.to_json() for e in self.objects],
        }
        if self.bot and self.bot.id:
            json["bot_id"] = self.bot.id
        return json

    def belong_to_bot(self, bot: 'Bot') -> None:
        """
        Set the bot that this object belongs to.
        """
        self.bot = bot

    def reload(self) -> None:
        """
        Reload this object from the server, keeping it up to date.
        """
        if not self.bot:
            raise Exception("bot is not specified for this object")
        loadedObject = self.bot.opt.find_object_with_name(name=self.objectName, type=self.objectType)
        if loadedObject:
            self.id = loadedObject.id
            self.bot = loadedObject.bot
            self.objectType = loadedObject.objectType
            self.objectName = loadedObject.objectName
            self.objects = loadedObject.objects
        else:
            raise Exception("object not found")
