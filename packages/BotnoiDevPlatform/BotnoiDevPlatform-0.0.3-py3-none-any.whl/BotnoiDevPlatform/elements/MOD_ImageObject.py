class ImageObject:
    """
    A class representing an image object.
    """
    def __init__(self, original_url:str, preview_image_url:str) -> None:
        from BotnoiDevPlatform.utils import ObjectType
        self.original_url = original_url
        self.preview_image_url = preview_image_url
        self.objectType = ObjectType.image()

    @classmethod
    def from_json(cls, json:dict) -> "ImageObject":
        """
        Create a new image object from json representation.
        """
        return cls(
            original_url=json["original_url"],
            preview_image_url=json["preview_image_url"]
        )

    def to_json(self) -> dict:
        """
        Convert this image object to json representation.
        """
        return {
            "original_url": self.original_url,
            "preview_image_url": self.preview_image_url
        }
