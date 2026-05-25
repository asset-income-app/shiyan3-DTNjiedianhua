from typing import List, Dict, Any
from framework.core import FuncNode

class MemoryFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '记忆功能')
        self.description = self.config.get('description', '存储和管理数据')
        self.storage: Dict[str, Any] = {}
    
    def _execute(self, input_data: Any) -> Any:
        action = input_data.get('action', 'get')
        
        if action == 'set':
            key = input_data.get('key')
            value = input_data.get('value')
            if key:
                self.storage[key] = value
                return {'success': True, 'message': f'已设置 {key}'}
            return {'success': False, 'message': '缺少键'}
        
        elif action == 'get':
            key = input_data.get('key')
            if key:
                return {
                    'success': True,
                    'key': key,
                    'value': self.storage.get(key)
                }
            return {'success': True, 'storage': self.storage}
        
        elif action == 'delete':
            key = input_data.get('key')
            if key and key in self.storage:
                del self.storage[key]
                return {'success': True, 'message': f'已删除 {key}'}
            return {'success': False, 'message': '键不存在'}
        
        elif action == 'clear':
            self.storage.clear()
            return {'success': True, 'message': '已清空'}
        
        return {'success': False, 'message': '未知操作'}

class ValidationFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '验证功能')
        self.description = self.config.get('description', '验证数据和规则')
    
    def _execute(self, input_data: Any) -> Any:
        data = input_data.get('data')
        rules = input_data.get('rules', [])
        
        if data is None:
            return {'success': False, 'message': '缺少数据'}
        
        violations = []
        
        for rule in rules:
            rule_type = rule.get('type')
            
            if rule_type == 'required':
                field = rule.get('field')
                if field and not data.get(field):
                    violations.append({
                        'rule': rule_type,
                        'field': field,
                        'message': f'{field} 是必填项'
                    })
            
            elif rule_type == 'min_length':
                field = rule.get('field')
                min_len = rule.get('value', 0)
                if field and len(str(data.get(field, ''))) < min_len:
                    violations.append({
                        'rule': rule_type,
                        'field': field,
                        'message': f'{field} 长度不足 {min_len}'
                    })
        
        return {
            'success': True,
            'valid': len(violations) == 0,
            'violations': violations
        }

class ConflictFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '冲突检测')
        self.description = self.config.get('description', '检测规则和数据冲突')
    
    def _execute(self, input_data: Any) -> Any:
        rules = input_data.get('rules', [])
        
        conflicts = []
        
        for i, rule1 in enumerate(rules):
            for j, rule2 in enumerate(rules):
                if i >= j:
                    continue
                
                if (rule1.get('subject') == rule2.get('subject') and
                    rule1.get('predicate') == rule2.get('predicate') and
                    rule1.get('obj') != rule2.get('obj')):
                    conflicts.append({
                        'rule1': rule1,
                        'rule2': rule2,
                        'type': 'contradiction'
                    })
        
        return {
            'success': True,
            'has_conflicts': len(conflicts) > 0,
            'conflicts': conflicts,
            'conflicts_count': len(conflicts)
        }

class VisualizeFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '可视化功能')
        self.description = self.config.get('description', '生成可视化数据')
    
    def _execute(self, input_data: Any) -> Any:
        data = input_data.get('data', [])
        chart_type = input_data.get('type', 'bar')
        
        if not data:
            return {'success': False, 'message': '数据为空'}
        
        visualization = {
            'type': chart_type,
            'data': data,
            'config': {
                'title': input_data.get('title', '图表'),
                'x_label': input_data.get('x_label', 'X'),
                'y_label': input_data.get('y_label', 'Y')
            }
        }
        
        return {
            'success': True,
            'visualization': visualization
        }

class FeedbackFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '反馈功能')
        self.description = self.config.get('description', '收集和处理反馈')
        self.feedback_list: List[Dict[str, Any]] = []
    
    def _execute(self, input_data: Any) -> Any:
        action = input_data.get('action', 'add')
        
        if action == 'add':
            feedback = {
                'content': input_data.get('content'),
                'rating': input_data.get('rating'),
                'timestamp': input_data.get('timestamp')
            }
            self.feedback_list.append(feedback)
            return {
                'success': True,
                'message': '反馈已添加',
                'total': len(self.feedback_list)
            }
        
        elif action == 'list':
            return {
                'success': True,
                'feedbacks': self.feedback_list,
                'count': len(self.feedback_list)
            }
        
        elif action == 'stats':
            if not self.feedback_list:
                return {
                    'success': True,
                    'count': 0,
                    'avg_rating': 0
                }
            
            ratings = [f['rating'] for f in self.feedback_list if f.get('rating')]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            
            return {
                'success': True,
                'count': len(self.feedback_list),
                'avg_rating': avg_rating
            }
        
        return {'success': False, 'message': '未知操作'}
