class CustomPayloadObject:
    """
    This class represents a custom payload object.
    """
    def __init__(self, payloadChannel:str, payload:dict) -> None:
        from BotnoiDevPlatform.utils import ObjectType
        self.payloadChannel = payloadChannel
        self.payload = payload
        self.objectType = ObjectType.customPayload()

    @classmethod
    def from_json(cls, json:dict) -> "CustomPayloadObject":
        """
        Create a new custom payload from json representation.
        """
        return cls(
            payloadChannel=json["payload_channel"],
            payload=json["payload"]
        )

    def to_json(self) -> dict:
        """
        Convert this custom payload to json representation.
        """
        return {
            "payload_channel": self.payloadChannel,
            "payload": self.payload
        }