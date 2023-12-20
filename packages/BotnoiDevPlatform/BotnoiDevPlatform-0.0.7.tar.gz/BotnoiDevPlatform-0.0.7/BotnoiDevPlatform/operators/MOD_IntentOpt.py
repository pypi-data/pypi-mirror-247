import json
import requests
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from BotnoiDevPlatform.elements import Bot
    from BotnoiDevPlatform.elements import IntentKeyword
    from BotnoiDevPlatform.elements import IntentReaction
    from BotnoiDevPlatform.elements import Intent

class IntentOperator:
    """
    The operator of an intent in a bot.

    This is used for training, updating, deleting, or finding keywords and reactions of an intent.
    """
    def __init__(self, intent: 'Intent', bot: 'Bot') -> None:
        self._intent = intent
        self._bot = bot

    @classmethod
    def of(cls, intent: 'Intent', bot: 'Bot') -> "IntentOperator":
        """
        Create an operator of an intent in a bot.
        - {intent} is the intent that you want to operate.
        - {bot} is the bot that the intent belongs to.
        """
        return cls(intent, bot)

    @property
    def _get_header(self):
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BotnoiClient.key()}",
        }

    def train_keyword(self, keyword: 'IntentKeyword') -> None:
        """
        Train the intent with a keyword.
        - {keyword} is the text that users can use to trigger this intent.
        
        training a keyword doesn't delete the previous keywords. Instead, it will add the new keyword to the list.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            keyword.belong_to_bot(self._bot)
            keyword.belong_to_intent(self._intent)
            url = f"{BotnoiClient.endpoint()}/training/record"
            response = requests.post(
                url,
                headers=self._get_header,
                data=json.dumps(keyword.to_json()),
            )
            if response.status_code in [201, 200, 204]:
                return
            raise Exception(f"[train_keyword] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[train_keyword] : {e}")

    def train_multi_keyword(self, keywords:Union[list['IntentKeyword'],None] = None, strings:Union[list[str],None] = None) -> None:
        """
        Train the intent with multiple keywords.
        -{keywords} is the list of texts that users can use to trigger this intent.
        
        training a keyword doesn't delete the previous keywords. Instead, it will add the new keywords to the list.
        """
        from BotnoiDevPlatform.elements.MOD_IntentKeyword import IntentKeyword
        if keywords is None and strings is None:
            raise Exception("[train_multi_keyword] : either keywords or strings must be provided")
        if keywords is None and strings is not None:
            keywords = [IntentKeyword(keyword=e) for e in strings]
        for keyword in (keywords or []):
            self.train_keyword(keyword)

    def train_reaction(self, reaction: 'IntentReaction') -> None:
        """
        Train the intent with a reaction.
        - {reaction} is a set of texts or actions that the bot will respond to the users.
        
        training a reaction doesn't delete the previous reactions. Instead, it will add the new reaction to the list.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            reaction.belong_to_bot(self._bot)
            reaction.belong_to_intent(self._intent)
            url = f"{BotnoiClient.endpoint()}/training/mapping"
            response = requests.post(
                url,
                headers=self._get_header,
                data=json.dumps(reaction.to_json()),
            )
            if response.status_code in [201, 200, 204]:
                return
            raise Exception(f"[train_reaction] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[train_reaction] : {e}")

    def train_multi_reaction(self, reactions:Union[list['IntentReaction'],None] = None, reactionStrings:Union[list[str],None] = None):
        """
        Train the intent with multiple reactions.
        - {reactions} is a set of texts or actions that the bot will respond to the users.
        - {reactionStrings} can be used instead of {reactions} if you don't want to create BotIntentReaction objects. This is ignored if {reactions} is provided.

        training a reaction doesn't delete the previous reactions. Instead, it will add the new reaction to the list.
        """
        from BotnoiDevPlatform.elements.MOD_IntentReaction import IntentReaction
        if reactions is None and reactionStrings is None:
            raise Exception("[train_multi_reaction] : either reactions or strings must be provided")
        if reactions is None and reactionStrings is not None:
            reactions = [IntentReaction(actions=[e]) for e in reactionStrings]
        for reaction in (reactions or []):
            self.train_reaction(reaction)

    def find_keywords(self) -> list['IntentKeyword']:
        """
        Find all keywords that the intent has been trained with.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        from BotnoiDevPlatform.elements.MOD_IntentKeyword import IntentKeyword
        try:
            url = f"{BotnoiClient.endpoint()}/training/record?bot_id={self._bot.id}&intent={self._intent.name}"
            response = requests.get(
                url,
                headers=self._get_header,
            )
            if response.status_code == 200:
                result = json.loads(response.content.decode("utf-8"))
                found = [IntentKeyword.from_json(e) for e in result]
                for e in found:
                    e.belong_to_bot(self._bot)
                    e.belong_to_intent(self._intent)
                return found
            raise Exception(f"[find_keywords] : {response.reason or 'ERROR'}")
        except Exception as e: 
            raise Exception(f"[find_keywords] : {e}")

    def find_keyword_with_index(self, index:int) -> 'IntentKeyword':
        """
        Find a keyword that the intent has been trained with by its index.
        - {index} is the index of the keyword you want to find starting from 0.
        """
        allKeywords = self.find_keywords()
        try:
            return allKeywords[index]
        except Exception as e:
            raise Exception(f"[find_keyword_with_index] : {e}")

    def find_primary_keyword(self) -> 'IntentKeyword':
        """
        Find the first keyword in this intent.
        
        This is equivalent to find_keyword_with_index(index: 0).
        """
        return self.find_keyword_with_index(0)

    def find_reaction(self) -> list['IntentReaction']:
        """
        Find all reactions that the intent has been trained with.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        from BotnoiDevPlatform.elements.MOD_IntentReaction import IntentReaction
        try:
            url = f"{BotnoiClient.endpoint()}/training/mapping?bot_id={self._bot.id}&intent={self._intent.name}"
            response = requests.get(
                url,
                headers=self._get_header,
            )
            if response.status_code == 200:
                result = json.loads(response.content.decode("utf-8"))
                found = [IntentReaction.from_json(e) for e in result]
                for e in found:
                    e.belong_to_bot(self._bot)
                    e.belong_to_intent(self._intent)
                return found
            raise Exception(f"[find_reaction] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[find_reaction] : {e}")

    def find_reaction_with_index(self, index:int) -> 'IntentReaction':
        """
        Find a reaction that the intent has been trained with by its index.
        - {index} is the index of the reaction you want to find starting from 0.
        """
        allReactions = self.find_reaction()
        try:
            return allReactions[index]
        except Exception as e:
            raise Exception(f"[find_reaction_with_index] : {e}")

    def find_primary_reaction(self) -> 'IntentReaction':
        """
        Find the first reaction in this intent.

        This is equivalent to find_reaction_with_index(index: 0).
        """
        return self.find_reaction_with_index(0)

    def update_keyword(self, keyword: 'IntentKeyword') -> None:
        """
        Update a keyword that the intent has been trained with.
        - {keyword} is the keyword you want to update. The keyword must have already been trained with this intent.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            keyword.belong_to_bot(self._bot)
            keyword.belong_to_intent(self._intent)
            url = f"{BotnoiClient.endpoint()}/training/record"
            response = requests.put(
                url,
                headers=self._get_header,
                data=json.dumps(keyword.to_json()),
            )
            if response.status_code in [200, 204]:
                return
            raise Exception(f"[update_keyword] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[update_keyword] : {e}")

    def update_reaction(self, reaction: 'IntentReaction') -> None:
        """
        Update a reaction that the intent has been trained with.
        - {reaction} is the reaction you want to update. The reaction must have already been trained with this intent.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            reaction.belong_to_bot(self._bot)
            reaction.belong_to_intent(self._intent)
            url = f"{BotnoiClient.endpoint()}/training/mapping"
            response = requests.put(
                url,
                headers=self._get_header,
                data=json.dumps(reaction.to_json()),
            )
            if response.status_code in [200, 204]:
                return
            raise Exception(f"[update_reaction] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[update_reaction] : {e}")

    def delete_keywords(self, keywords: list['IntentKeyword']) -> None:
        """
        Delete keywords that the intent has been trained with.
        - {keywords} is the list of keywords to be deleted. Every keyword in the list must have already been trained with this intent.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            for keyword in keywords:
                keyword.belong_to_bot(self._bot)
                keyword.belong_to_intent(self._intent)
            url = f"{BotnoiClient.endpoint()}/training/record"
            response = requests.delete(
                url,
                headers=self._get_header,
                data=json.dumps({
                    "_id": [e.id for e in keywords],
                    "bot_id": self._bot.id,
                }),
            )
            if response.status_code in [200, 204]:
                return
            raise Exception(f"[delete_keywords] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[delete_keywords] : {e}")

    def delete_all_keywords(self) -> None:
        """
        Delete all keywords that the intent has been trained with.
        """
        keywords = self.find_keywords()
        if keywords:
            self.delete_keywords(keywords)

    def delete_reactions(self, reactions: list['IntentReaction']) -> None:
        """
        Delete reactions that the intent has been trained with.
        - {reactions} is the list of reactions to be deleted. Every reaction in the list must have already been trained with this intent.
        """
        from BotnoiDevPlatform.cores.MOD_BotnoiClient import BotnoiClient
        try:
            for reaction in reactions:
                reaction.belong_to_bot(self._bot)
                reaction.belong_to_intent(self._intent)
            url = f"{BotnoiClient.endpoint()}/training/mapping"
            response = requests.delete(
                url,
                headers=self._get_header,
                data=json.dumps({
                    "_id": [e.id for e in reactions],
                    "bot_id": self._bot.id,
                }),
            )
            if response.status_code in [200, 204]:
                return
            raise Exception(f"[delete_reactions] : {response.reason or 'ERROR'}")
        except Exception as e:
            raise Exception(f"[delete_reactions] : {e}")

    def delete_all_reactions(self) -> None:
        """
        Delete all reactions that the intent has been trained with.
        """
        reactions = self.find_reaction()
        if reactions:
            self.delete_reactions(reactions)

    def derive_from_intent(self, source:'Intent', mapping:dict={}, overwrite:bool=True):
        """
        Derive this intent from another intent. This will copy all the keywords and reactions from the source intent to this intent.
        - {source} is the intent you want to derive from.
        - {mapping} is used to replace placeholders in the keywords and reactions. For example, if you have a keyword "I want to go to {place}" and you want to replace {place} with "Bangkok", you can do this:   
        
        ```python
        intent.derive_from_intent(source, mapping = {"place": "Bangkok"});
        ```
        notice that placeholders must be surrounded by curly braces.

        - {overwrite} is used to determine whether you want to clear all prior keywords and reactions in this intent.
        """
        if overwrite:
            self.delete_all_keywords()
            self.delete_all_reactions()
        sourceKeywords = source.opt.find_keywords()
        sourceReactions = source.opt.find_reaction()
        if sourceKeywords:
            for k in sourceKeywords:
                for key in mapping.keys():
                    k.keyword = k.keyword.replace(f"{{{key}}}", mapping[key])
            self.train_multi_keyword(keywords=sourceKeywords)
        if sourceReactions:
            for m in sourceReactions:
                for key in mapping.keys():
                    m.actions = [e.replace(f"{{{key}}}", mapping[key]) for e in m.actions]
            self.train_multi_reaction(reactions=sourceReactions)
