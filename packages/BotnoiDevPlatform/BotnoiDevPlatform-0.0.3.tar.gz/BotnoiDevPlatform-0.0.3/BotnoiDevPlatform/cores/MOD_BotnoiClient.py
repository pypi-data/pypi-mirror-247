import os

class BotnoiClient:
    """
    This class represents the client interacting with the Botnoi Chatbot Server.
    """

    @classmethod
    def setup(cls, key: str, endpoint: str) -> None:
        """
        Initialize the client with the endpoint and the key.
        - {endpoint} is the endpoint of the botnoi chatbot server.
        - {key} is the API key you got from botnoi developer platform.
        """
        os.environ["BOTNOI_DEV_API_KEY"] = key
        os.environ["BOTNOI_DEV_API_ENDPOINT"] = endpoint

    @staticmethod
    def endpoint() -> str:
        """
        Get the endpoint registered with this client.
        """
        return str(os.environ["BOTNOI_DEV_API_ENDPOINT"])
    
    @staticmethod
    def key() -> str:
        """
        Get the API key registered with this client.
        """
        return str(os.environ["BOTNOI_DEV_API_KEY"])