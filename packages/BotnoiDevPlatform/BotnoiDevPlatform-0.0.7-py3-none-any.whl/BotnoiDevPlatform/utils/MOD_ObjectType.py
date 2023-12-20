class ObjectType:
    """
    This class represents an object type.

    Supported types include:
        - ObjectType.api()
        - ObjectType.audio()
        - ObjectType.button()
        - ObjectType.carousel()
        - ObjectType.dialogue()
        - ObjectType.image()
        - ObjectType.customPayload()
    """
    def __init__(self, stringType:str) -> None:
        self.stringType = stringType

    @classmethod
    def api(cls) -> "ObjectType":
        """
        This class represents an api object type.
        """
        return ObjectType("api")
    
    @classmethod
    def audio(cls) -> "ObjectType":
        """
        This class represents an audio object type.
        """
        return ObjectType("audio")
    
    @classmethod
    def button(cls) -> "ObjectType":
        """
        This class represents a button object type.
        """
        return ObjectType("button")
    
    @classmethod
    def carousel(cls) -> "ObjectType":
        """
        This class represents a carousel object type.
        """
        return ObjectType("carousel")
    
    @classmethod
    def dialogue(cls) -> "ObjectType":
        """
        This class represents a dialogue object type.
        """
        return ObjectType("dialogue")
    
    @classmethod
    def image(cls) -> "ObjectType":
        """
        This class represents an image object type.
        """
        return ObjectType("image")
    
    @classmethod
    def customPayload(cls) -> "ObjectType":
        """
        This class represents a custom payload object type.
        """
        return ObjectType("custom_payload")
