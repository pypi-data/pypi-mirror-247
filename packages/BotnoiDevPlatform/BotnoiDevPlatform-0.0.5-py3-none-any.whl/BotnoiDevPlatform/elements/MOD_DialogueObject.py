class DialogueObject:
    """
    This class represents a dialogue object.
    """
    def __init__(self, startNode:"DialogueNode", nodeList:list["DialogueNode"], edgeList: list["DialogueEdge"], position:str) -> None:
        from BotnoiDevPlatform.utils import ObjectType
        self.startNode = startNode
        self.nodeList = nodeList
        self.edgeList = edgeList
        self.position = position
        self.objectType = ObjectType.dialogue()

    @classmethod
    def from_json(cls, json:dict) -> "DialogueObject":
        """
        Create a new dialogue from json representation.
        """
        return cls(
            startNode=json["start_node"],
            nodeList=[DialogueNode.from_json(node) for node in json["node_list"]],
            edgeList=[DialogueEdge.from_json(edge) for edge in json["edge_list"]],
            position=json["position"]
        )

    def to_json(self) -> dict:
        """
        Convert this dialogue to json representation.
        """
        return {
            "start_node": self.startNode,
            "node_list": [node.to_json() for node in self.nodeList],
            "edge_list": [edge.to_json() for edge in self.edgeList],
            "position": self.position
        }
    
class DialogueNode:
    def __init__(self, nid:str, name:str, actions:list[str], timeoutActions:list[dict]=[]):
        self.nid = nid
        self.name = name
        self.actions = actions
        self.timeoutActions = timeoutActions

    @classmethod
    def from_json(cls, json:dict) -> "DialogueNode":
        return cls(
            nid=json["_nid"],
            name=json["name"],
            actions=json["questionList"],
            timeoutActions=json["timeout_actions"]
        )

    def to_json(self) -> dict:
        return {
            "_nid": self.nid,
            "name": self.name,
            "questionList": self.actions,
            "timeout_actions": self.timeoutActions,
            "error": ""
        }


class DialogueEdge:
    """
    This class represents an edge in a dialogue.
    """
    def __init__(self, eid:str, name:str, fromNode:str, toNode:str, conditions:list["DialogueCondition"], param:str="") -> None:
        self.eid = eid
        self.name = name
        self.fromNode = fromNode
        self.toNode = toNode
        self.conditions = conditions
        self.param = param

    @classmethod
    def from_json(cls, json:dict) -> "DialogueEdge":
        """
        Create a new edge from json representation.
        """
        return cls(
            eid=json["_eid"],
            name=json["lineName"],
            param=json["param"],
            fromNode=json["fromNode"],
            toNode=json["toNode"],
            conditions=[DialogueCondition.from_json(condition) for condition in json["conditions"]]
        )

    def to_json(self) -> dict:
        """
        Convert this edge to json representation.
        """
        return {
            "_eid": self.eid,
            "lineName": self.name,
            "param": self.param,
            "fromNode": self.fromNode,
            "toNode": self.toNode,
            "conditions": [condition.to_json() for condition in self.conditions]
        }


class DialogueCondition:
    """
    This class represents a condition in a dialogue.
    """
    def __init__(self, type:str, data:str) -> None:
        self.type = type
        self.data = data

    @classmethod
    def from_json(cls, json:dict) -> "DialogueCondition":
        """
        Create a new condition from json representation.
        """
        return cls(
            type=json["type"],
            data=json["data"]
        )

    def to_json(self) -> dict:
        """
        Convert this condition to json representation.
        """
        return {
            "type": self.type,
            "data": self.data
        }


