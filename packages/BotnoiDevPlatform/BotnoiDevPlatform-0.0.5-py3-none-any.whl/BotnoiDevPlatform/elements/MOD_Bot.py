from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.operators import BotOperator
    from BotnoiDevPlatform.channels import BotChannel

class Bot:
    """
    This class represents a bot in the botnoi chatbot server
    """

    def __init__(self, 
                 botName:str, 
                 sex:str, 
                 age:int, 
                 botAvatar:str, 
                 businessType:str, 
                 owner:str = "", 
                 channelActiveStatus:Union[dict,None] = None, 
                 accessChannel:Union[dict,None]=None, 
                 id:Union[str,None]=None) -> None:
        self.botName = botName
        self.owner = owner
        self.sex = sex
        self.age = age
        self.botAvatar = botAvatar
        self.businessType = businessType
        self.channelActiveStatus = channelActiveStatus
        self.accessChannel = accessChannel
        self.id = id

    @classmethod
    def from_json(cls, json:dict) -> "Bot":
        """
        Create a bot from a json representation.
        """
        return cls(
            id=json["_id"],
            botName=json["bot_name"],
            owner=json["owner"],
            sex=json["sex"],
            age=json["age"],
            botAvatar=json["bot_avatar"],
            businessType=json["business_type"],
            channelActiveStatus={key: str(value).lower() == "true" for key, value in json["channel_active_status"].items()},
            accessChannel=json["access_channel"],
        )

    def to_json(self) -> dict:
        """
        Convert this bot to a json representation.
        """
        json = {
            "bot_name": self.botName,
            "owner": self.owner,
            "sex": self.sex,
            "age": self.age,
            "bot_avatar": self.botAvatar,
            "business_type": self.businessType,
            "channel_active_status": self.channelActiveStatus,
            "access_channel": self.accessChannel,
        }
        if self.id is not None:
            json["_id"] = self.id
        return json

    @property
    def opt(self) -> 'BotOperator':
        """
        The operator of this bot
        """
        from BotnoiDevPlatform.operators import BotOperator
        return BotOperator.of(self)

    @property
    def channel(self) -> 'BotChannel':
        """
        The connection of this bot
        """
        from BotnoiDevPlatform.channels import BotChannel
        return BotChannel.of(self)

    def reload(self) -> None:
        """
        Reload this bot from the server, keeping it up to date
        """
        from BotnoiDevPlatform.cores import BotnoiChatbotServer
        loadedBot = BotnoiChatbotServer().find_bot_with_name(self.botName)
        if loadedBot is not None:
            self.id = loadedBot.id
            self.owner = loadedBot.owner
            self.botName = loadedBot.botName
            self.sex = loadedBot.sex
            self.age = loadedBot.age
            self.botAvatar = loadedBot.botAvatar
            self.businessType = loadedBot.businessType
            self.channelActiveStatus = loadedBot.channelActiveStatus
            self.accessChannel = loadedBot.accessChannel
        else:
            raise Exception(f"bot '{self.botName}' can't be found or no longer exists")

