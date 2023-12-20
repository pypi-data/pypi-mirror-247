from typing import Union

class Action:
    """
    This class helps define the action of nodes or messages.
    
    It returns a string that represents the action.
    """

    @staticmethod
    def text(text:str) -> str:
        """
        A string representing the action of sending a text.
        """
        return text

    @staticmethod
    def api(apiName:str) -> str:
        """
        A string representing the action of calling an API object.
        
        It will also automatically store the API response in a parameter.
        For example, if the API name is "getWeather", you can call the api by using BotAction.api("getWeather").
        After that, you can refer to the response by using BotAction.parameter(BotAction.api("getWeather")).

        This doesn't create a new API object nor check if the API exists. If the API doesn't exist, this action will be ignored in runtime.
        """
        return "API_" + apiName

    @staticmethod
    def image(imageName:str) -> str:
        """
        A string representing the action of calling an image object.
        
        This doesn't create a new image object nor check if the image exists. If the image doesn't exist, this action will be ignored in runtime.
        """
        return "IMG_" + imageName

    @staticmethod
    def button(buttonName:str) -> str:
        """
        A string representing the action of calling a button object.
        
        This doesn't create a new button object nor check if the button exists. If the button doesn't exist, this action will be ignored in runtime.
        """
        return "BTN_" + buttonName

    @staticmethod
    def carousel(carouselName:str) -> str:
        """
        A string representing the action of calling a carousel object.
        
        This doesn't create a new carousel object nor check if the carousel exists. If the carousel doesn't exist, this action will be ignored in runtime.
        """
        return "CRS_" + carouselName

    @staticmethod
    def dialogue(dialogueName:str) -> str:
        """
        A string representing the action of calling a dialogue object.
        
        This doesn't create a new dialogue object nor check if the dialogue exists. If the dialogue doesn't exist, this action will be ignored in runtime.
        """
        return "DL_" + dialogueName

    @staticmethod
    def intent(intentName:str) -> str:
        """
        A string representing the action of calling an intent.
        
        This doesn't create a new intent nor check if the intent exists. If the intent doesn't exist, this action will be ignored in runtime.
        """
        return "{{" + intentName + "}}"

    @staticmethod
    def createParameter(parameterName:str, parameterValue:Union[str,int,float]) -> str:
        """
        A string representing the action of creating a new parameter.
        
        Parameters are variables that can be referred to anywhere in the bot.
        They can be either a string or a number.
        """
        return "<!" + parameterName + "|" + str(parameterValue) + "!>"

    @staticmethod
    def parameter(parameterName:str) -> str:
        """
        A referrence to a parameter.
        
        Parameters are variables that can be referred to anywhere in the bot.
        They can be either a string or a number.
        
        This doesn't create a new parameter nor check if the parameter exists. If the parameter doesn't exist, this action will be ignored in runtime.
        """
        return "<<" + parameterName + ">>"

    @staticmethod
    def get_keyword() -> str:
        """
        A referrence to the latest respond from the user.
        
        Since every respond from the user is stored in a keyword parameter,
        This is equivalent to Action.parameter("keyword").
        """
        return "<<keyword>>"
