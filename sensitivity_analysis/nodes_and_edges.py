from dataclasses import dataclass
from serde import serde, field, ExternalTagging
from typing import List, Tuple, TypeAlias, Union
from sensitivity_analysis.constructions import Construction, ConstructionToProduct


# The class Temp is a workaround to make the serializing and deserializing work correctly
# If anyone is interested in solving this you are welcome to give is a try or contact Lærke Vejsnæs (lhv@build.aau.dk)
@serde(tagging=ExternalTagging)
@dataclass
class Temp:
    pass


# This script contains the classes representing the overall nodes and edges and which types of content
# they can have in the LCAbyg json
@serde(tagging=ExternalTagging)
@dataclass
class Node:
    """
    All nodes in the LCAbyg json contain a dictionary with the possible node types
    """
    node: Union[Construction, Temp] = field(rename='Node')


@serde(tagging=ExternalTagging)
@dataclass
class Edge:
    """
    All edges in the LCAbyg json contain a list of a dictionary and two strings (uuids).
    the possible dictionaries are represented in the different classes.
    """
    edge: Tuple[ConstructionToProduct | Temp, str, str] = field(rename='Edge')


# This TypeAlias is needed to handle a json, which is a list of nodes and edges.
File: TypeAlias = List[Node | Edge]
