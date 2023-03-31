from dataclasses import dataclass
from serde import serde, ExternalTagging
from sensitivity_analysis.general import Name, Comment


# This script represents the content of nodes and edges needed for constructions in LCAbyg json
@serde(tagging=ExternalTagging)
@dataclass
class Construction:
    id: str
    name: Name
    unit: str
    source: str
    comment: Comment
    layer: int
    locked: bool

    def __init__(self, construction_id: str, name: Name, unit: str,
                 source: str, comment: Comment, layer: int, locked: bool):
        self.id = construction_id
        self.name = name
        self.unit = unit
        self.source = source
        self.comment = comment
        self.layer = layer
        self.locked = locked


@serde
@dataclass
class ConstructionToProduct:
    id: str
    amount: float | int
    unit: str
    lifespan: int
    demolition: bool
    enabled: bool
    delayed_start: int

    def __init__(self, edge_id: str, amount: float, unit: str, lifespan: int,
                 demolition: bool, enabled: bool, delayed_start: int):
        self.id = edge_id
        self.amount = amount
        self.unit = unit
        self.lifespan = lifespan
        self.demolition = demolition
        self.enabled = enabled
        self.delayed_start = delayed_start
