from typing import Union

class FacebookPage:
    def __init__(self, 
                pageId:str,
                isUsed:bool,
                name:str, 
                picturUrl:str, 
                botId:Union[str,None]=None, 
                ownerId:Union[str,None]=None):
        self.pageId = pageId
        self.isUsed = isUsed
        self.name = name
        self.picturUrl = picturUrl
        self.botId = botId
        self.ownerId = ownerId

    @classmethod
    def from_json(cls, json:dict) -> "FacebookPage":
        """
        Create a new facebook page from json representation.
        """
        return cls(
            pageId=json["page_id"],
            isUsed=json["is_used"],
            name=json["name"],
            picturUrl=json["page_pic"],
            botId=json["bot_id"] if json["is_used"] else None,
            ownerId=json["owner_id"] if json["is_used"] else None
        )

    def to_json(self) -> dict:
        """
        Convert this facebook page to json representation.
        """
        return {
            "page_id": self.pageId,
            "is_used": self.isUsed,
            "name": self.name,
            "page_pic": self.picturUrl,
            "bot_id": self.botId,
            "owner_id": self.ownerId
        }
