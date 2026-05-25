from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from enum import Enum
import uuid
import time

class NodeType(Enum):
    NODE = "node"
    SKILL = "skill"
    RULE = "rule"
    DATA = "data"
    FUNC = "func"

class Node(ABC):
    def __init__(self, config: Dict[str, Any] = None):
        self.id = str(uuid.uuid4())[:8]
        self.config = config or {}
        self.name = self.config.get('name', self.__class__.__name__)
        self.description = self.config.get('description', '')
        self.enabled = self.config.get('enabled', True)
        self.created_at = time.time()
        self.updated_at = time.time()
        self.metadata = {}
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        raise NotImplementedError
    
    def is_enabled(self) -> bool:
        return self.enabled
    
    def enable(self):
        self.enabled = True
        self.updated_at = time.time()
    
    def disable(self):
        self.enabled = False
        self.updated_at = time.time()
    
    def get_name(self) -> str:
        return self.name
    
    def get_id(self) -> str:
        return self.id
    
    def get_type(self) -> NodeType:
        return NodeType.NODE
    
    def set_metadata(self, key: str, value: Any):
        self.metadata[key] = value
        self.updated_at = time.time()
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)
    
    def __str__(self):
        return f"{self.name}[{self.id}]"
    
    def __repr__(self):
        return self.__str__()

class SkillNode(Node):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.priority = self.config.get('priority', 1.0)
        self.confidence = self.config.get('confidence', 1.0)
        self.usage_count = 0
    
    def get_type(self) -> NodeType:
        return NodeType.SKILL
    
    def get_priority(self) -> float:
        return self.priority
    
    def get_confidence(self) -> float:
        return self.confidence
    
    def get_usage_count(self) -> int:
        return self.usage_count
    
    def increment_usage(self):
        self.usage_count += 1
        self.updated_at = time.time()
    
    def reset_usage(self):
        self.usage_count = 0
        self.updated_at = time.time()

class RuleNode(Node):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.rules: List[Any] = []
    
    def get_type(self) -> NodeType:
        return NodeType.RULE
    
    def add_rule(self, rule: Any):
        self.rules.append(rule)
        self.updated_at = time.time()
    
    def remove_rule(self, rule: Any):
        if rule in self.rules:
            self.rules.remove(rule)
            self.updated_at = time.time()
    
    def get_rules(self) -> List[Any]:
        return self.rules.copy()
    
    def clear_rules(self):
        self.rules.clear()
        self.updated_at = time.time()

class DataNode(Node):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.data: Dict[str, Any] = {}
    
    def get_type(self) -> NodeType:
        return NodeType.DATA
    
    def set(self, key: str, value: Any):
        self.data[key] = value
        self.updated_at = time.time()
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
    
    def delete(self, key: str):
        if key in self.data:
            del self.data[key]
            self.updated_at = time.time()
    
    def has(self, key: str) -> bool:
        return key in self.data
    
    def clear(self):
        self.data.clear()
        self.updated_at = time.time()
    
    def get_all(self) -> Dict[str, Any]:
        return self.data.copy()

class FuncNode(Node):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.performance_metrics = {
            'executions': 0,
            'total_time': 0.0,
            'errors': 0
        }
    
    def get_type(self) -> NodeType:
        return NodeType.FUNC
    
    def execute(self, input_data: Any) -> Any:
        start_time = time.time()
        
        try:
            result = self._execute(input_data)
            elapsed = time.time() - start_time
            
            self.performance_metrics['executions'] += 1
            self.performance_metrics['total_time'] += elapsed
            self.updated_at = time.time()
            
            return result
        except Exception as e:
            self.performance_metrics['errors'] += 1
            self.updated_at = time.time()
            raise e
    
    @abstractmethod
    def _execute(self, input_data: Any) -> Any:
        raise NotImplementedError
    
    def get_performance(self) -> Dict[str, Any]:
        metrics = self.performance_metrics.copy()
        if metrics['executions'] > 0:
            metrics['avg_time'] = metrics['total_time'] / metrics['executions']
        return metrics
    
    def reset_performance(self):
        self.performance_metrics = {
            'executions': 0,
            'total_time': 0.0,
            'errors': 0
        }
        self.updated_at = time.time()
