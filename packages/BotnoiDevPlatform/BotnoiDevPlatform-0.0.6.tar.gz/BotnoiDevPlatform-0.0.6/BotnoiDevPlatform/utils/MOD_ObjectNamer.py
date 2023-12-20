from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.utils.MOD_ObjectType import ObjectType

class ObjectNamer:
    """
    A helper for naming objects appropriately according to their type.

    This is crucial if you want to use Action to refer to objects.
    """
    
    @staticmethod
    def by_action(name:str, type:'ObjectType') -> str:
        """
        Name an object by how it is referenced in an action.
        """
        from BotnoiDevPlatform.utils.MOD_ObjectType import ObjectType
        from BotnoiDevPlatform.utils.MOD_Action import Action
        if type.stringType == ObjectType.image().stringType:
            return Action.image(name)
        elif type.stringType == ObjectType.api().stringType:
            return Action.api(name)
        elif type.stringType == ObjectType.button().stringType:
            return Action.button(name)
        elif type.stringType == ObjectType.dialogue().stringType:
            return Action.dialogue(name)
        elif type.stringType == ObjectType.carousel().stringType:
            return Action.carousel(name)
        else:
            return name
