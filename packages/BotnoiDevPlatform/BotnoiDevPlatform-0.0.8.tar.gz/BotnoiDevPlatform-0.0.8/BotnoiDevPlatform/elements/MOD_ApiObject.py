class ApiObject:
    """
    A class representing an api object.
    """
    def __init__(self, url:str, method:str, header:dict, body:str) -> None:
        from BotnoiDevPlatform.utils import ObjectType
        self.url = url
        self.method = method
        self.header = header
        self.body = body
        self.objectType = ObjectType.api()

    @classmethod
    def from_json(cls, json:dict) -> "ApiObject":
        """
        Create a new api object from json representation.
        """
        return cls(
            url=json["api_url"],
            method=json["method"],
            header={str(key): value for key, value in json["api_header"].items()},
            body=json["api_body"]
        )

    def to_json(self) -> dict:
        """
        Convert this api object to json representation.
        """
        return {
            "api_url": self.url,
            "method": self.method.lower(),
            "api_header": self.header,
            "api_body": self.body
        }
