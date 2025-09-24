from dataclasses import dataclass, field, asdict
from typing import List, Any, Optional
from enum import Enum

class FactType(Enum):
    """Enum to differentiate between types of facts."""
    QUANTITATIVE = "QUANTITATIVE"
    NARRATIVE = "NARRATIVE"
    def __str__(self): return self.value

@dataclass
class Fact:
    """Represents a single fact, which can be quantitative or narrative."""
    description: str
    value: Any
    type: FactType = FactType.QUANTITATIVE
    is_income: bool = False
    is_deduction: bool = False
    condition_for: Optional[str] = None
    def to_dict(self):
        data = asdict(self)
        data['type'] = str(self.type)
        return data

@dataclass
class ReasoningTreeNode:
    """Represents a node in the symbolic reasoning tree."""
    description: str
    facts: List[Fact] = field(default_factory=list)
    children: List['ReasoningTreeNode'] = field(default_factory=list)
    result: Optional[float] = None
    def to_dict(self):
        return {
            "description": self.description,
            "facts": [fact.to_dict() for fact in self.facts],
            "children": [child.to_dict() for child in self.children],
            "result": self.result
        }

@dataclass
class ReasoningTree:
    """Represents the complete reasoning tree for a tax case."""
    root: ReasoningTreeNode
    def to_dict(self):
        return {"root": self.root.to_dict()}