from typing import Dict, List, Optional, Any
from core import Node, NodeType, SkillNode, RuleNode, DataNode, FuncNode

class NodeRegistry:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.nodes_by_type: Dict[NodeType, List[str]] = {
            NodeType.NODE: [],
            NodeType.SKILL: [],
            NodeType.RULE: [],
            NodeType.DATA: [],
            NodeType.FUNC: []
        }
    
    def register(self, node: Node) -> bool:
        if not isinstance(node, Node):
            return False
        
        node_id = node.get_id()
        
        if node_id in self.nodes:
            return False
        
        self.nodes[node_id] = node
        
        node_type = node.get_type()
        if node_type in self.nodes_by_type:
            self.nodes_by_type[node_type].append(node_id)
        
        return True
    
    def unregister(self, node_id: str) -> bool:
        if node_id not in self.nodes:
            return False
        
        node = self.nodes[node_id]
        node_type = node.get_type()
        
        if node_type in self.nodes_by_type and node_id in self.nodes_by_type[node_type]:
            self.nodes_by_type[node_type].remove(node_id)
        
        del self.nodes[node_id]
        return True
    
    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)
    
    def get_all_nodes(self) -> List[Node]:
        return list(self.nodes.values())
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[Node]:
        node_ids = self.nodes_by_type.get(node_type, [])
        return [self.nodes[nid] for nid in node_ids if nid in self.nodes]
    
    def get_enabled_nodes(self) -> List[Node]:
        return [node for node in self.nodes.values() if node.is_enabled()]
    
    def get_enabled_nodes_by_type(self, node_type: NodeType) -> List[Node]:
        nodes = self.get_nodes_by_type(node_type)
        return [node for node in nodes if node.is_enabled()]
    
    def enable_node(self, node_id: str) -> bool:
        node = self.get_node(node_id)
        if node:
            node.enable()
            return True
        return False
    
    def disable_node(self, node_id: str) -> bool:
        node = self.get_node(node_id)
        if node:
            node.disable()
            return True
        return False
    
    def find_by_name(self, name: str) -> Optional[Node]:
        for node in self.nodes.values():
            if node.get_name() == name:
                return node
        return None
    
    def find_by_type_and_name(self, node_type: NodeType, name: str) -> Optional[Node]:
        nodes = self.get_nodes_by_type(node_type)
        for node in nodes:
            if node.get_name() == name:
                return node
        return None
    
    def clear(self):
        self.nodes.clear()
        for node_type in self.nodes_by_type:
            self.nodes_by_type[node_type].clear()
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_nodes': len(self.nodes),
            'enabled_nodes': len(self.get_enabled_nodes()),
            'skill_nodes': len(self.get_nodes_by_type(NodeType.SKILL)),
            'rule_nodes': len(self.get_nodes_by_type(NodeType.RULE)),
            'data_nodes': len(self.get_nodes_by_type(NodeType.DATA)),
            'func_nodes': len(self.get_nodes_by_type(NodeType.FUNC))
        }
    
    def print_stats(self):
        stats = self.get_stats()
        print("=" * 50)
        print("节点注册表统计")
        print("=" * 50)
        print(f"总节点数: {stats['total_nodes']}")
        print(f"启用节点数: {stats['enabled_nodes']}")
        print(f"技能节点: {stats['skill_nodes']}")
        print(f"规则节点: {stats['rule_nodes']}")
        print(f"数据节点: {stats['data_nodes']}")
        print(f"功能节点: {stats['func_nodes']}")
        print("=" * 50)

class NodeScheduler:
    def __init__(self, registry: NodeRegistry):
        self.registry = registry
        self.execution_history: List[Dict[str, Any]] = []
    
    def execute_node(self, node_id: str, input_data: Any) -> Any:
        node = self.registry.get_node(node_id)
        if not node:
            raise ValueError(f"节点不存在: {node_id}")
        
        if not node.is_enabled():
            raise ValueError(f"节点已禁用: {node_id}")
        
        result = node.execute(input_data)
        
        self.execution_history.append({
            'node_id': node_id,
            'node_name': node.get_name(),
            'node_type': node.get_type().value,
            'timestamp': node.updated_at,
            'success': True
        })
        
        return result
    
    def execute_by_name(self, node_name: str, input_data: Any) -> Any:
        node = self.registry.find_by_name(node_name)
        if not node:
            raise ValueError(f"节点不存在: {node_name}")
        
        return self.execute_node(node.get_id(), input_data)
    
    def execute_by_type(self, node_type: NodeType, input_data: Any) -> List[Any]:
        nodes = self.registry.get_enabled_nodes_by_type(node_type)
        results = []
        
        for node in nodes:
            try:
                result = self.execute_node(node.get_id(), input_data)
                results.append(result)
            except Exception as e:
                self.execution_history.append({
                    'node_id': node.get_id(),
                    'node_name': node.get_name(),
                    'node_type': node.get_type().value,
                    'error': str(e),
                    'success': False
                })
        
        return results
    
    def get_execution_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.execution_history[-limit:]
    
    def clear_history(self):
        self.execution_history.clear()
