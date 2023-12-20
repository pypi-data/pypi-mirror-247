class AudioObject:
    """
    A class representing an audio object.
    """
    def __init__(self, url:str, duration:int) -> None:
        from BotnoiDevPlatform.utils import ObjectType
        self.url = url
        self.duration = duration
        self.objectType = ObjectType.audio()


    @classmethod
    def from_json(cls, json:dict) -> "AudioObject":
        """
        Create a new audio object from json representation.
        """
        return cls(
            url=json["audio_url"],
            duration=json["audio_duration"]
        )

    def to_json(self) -> dict:
        """
        Convert this audio object to json representation.
        """
        return {
            "audio_url": self.url,
            "audio_duration": self.duration
        }
