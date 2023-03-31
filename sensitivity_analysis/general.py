from dataclasses import dataclass
from serde import serde, field, ExternalTagging
from typing import Optional


# This script contains all the classes that represent general content in the LCAbyg json
@serde(tagging=ExternalTagging)
@dataclass
class Name:
    """
    Represents the names used in all nodes.
    Names in all three languages are not needed for deserialization to work.
    When serializing and deserializing, names in all three languages will be created as default empty str.
    """
    danish: Optional[str] = field(default='', skip_if_default=True, rename='Danish')
    english: Optional[str] = field(default='', skip_if_default=True, rename='English')
    german: Optional[str] = field(default='', skip_if_default=True, rename='German')

    def __init__(self, danish_name: str = None, english_name: str = None, german_name: str = None):
        self.danish = danish_name
        self.english = english_name
        self.german = german_name


@serde
@dataclass
class Comment:
    """
    Represents the comments used in all nodes
    """
    danish: Optional[str] = field(default='', skip_if_default=True, rename='Danish')
    english: Optional[str] = field(default='', skip_if_default=True, rename='English')
    german: Optional[str] = field(default='', skip_if_default=True, rename='German')

    def __init__(self, danish_name: str = None, english_name: str = None, german_name: str = None):
        self.danish = danish_name
        self.english = english_name
        self.german = german_name
