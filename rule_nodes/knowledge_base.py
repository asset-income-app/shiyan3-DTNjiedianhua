from typing import List, Dict, Any
from framework.core import RuleNode

class KnowledgeBase(RuleNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '知识库')
        self.description = self.config.get('description', '存储和管理知识规则')
        self.rules_by_subject: Dict[str, List[int]] = {}
        self.rules_by_predicate: Dict[str, List[int]] = {}
        self.rules_by_obj: Dict[str, List[int]] = {}
    
    def add_rule(self, rule: Dict[str, Any]):
        super().add_rule(rule)
        
        rule_id = len(self.rules) - 1
        
        subject = rule.get('subject')
        if subject:
            if subject not in self.rules_by_subject:
                self.rules_by_subject[subject] = []
            self.rules_by_subject[subject].append(rule_id)
        
        predicate = rule.get('predicate')
        if predicate:
            if predicate not in self.rules_by_predicate:
                self.rules_by_predicate[predicate] = []
            self.rules_by_predicate[predicate].append(rule_id)
        
        obj = rule.get('obj')
        if obj:
            if obj not in self.rules_by_obj:
                self.rules_by_obj[obj] = []
            self.rules_by_obj[obj].append(rule_id)
    
    def query_by_subject(self, subject: str) -> List[Dict[str, Any]]:
        if subject not in self.rules_by_subject:
            return []
        return [self.rules[i] for i in self.rules_by_subject[subject]]
    
    def query_by_predicate(self, predicate: str) -> List[Dict[str, Any]]:
        if predicate not in self.rules_by_predicate:
            return []
        return [self.rules[i] for i in self.rules_by_predicate[predicate]]
    
    def query_by_obj(self, obj: str) -> List[Dict[str, Any]]:
        if obj not in self.rules_by_obj:
            return []
        return [self.rules[i] for i in self.rules_by_obj[obj]]
    
    def query(self, subject: str = None, predicate: str = None, obj: str = None) -> List[Dict[str, Any]]:
        results = []
        
        for rule in self.rules:
            match = True
            if subject and rule.get('subject') != subject:
                match = False
            if predicate and rule.get('predicate') != predicate:
                match = False
            if obj and rule.get('obj') != obj:
                match = False
            if match:
                results.append(rule)
        
        return results
    
    def get_subjects(self) -> List[str]:
        return list(self.rules_by_subject.keys())
    
    def get_predicates(self) -> List[str]:
        return list(self.rules_by_predicate.keys())
    
    def get_objects(self) -> List[str]:
        return list(self.rules_by_obj.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_rules': len(self.rules),
            'unique_subjects': len(self.rules_by_subject),
            'unique_predicates': len(self.rules_by_predicate),
            'unique_objects': len(self.rules_by_obj)
        }
    
    def execute(self, input_data: Any) -> Any:
        action = input_data.get('action', 'query')
        
        if action == 'add':
            rule = input_data.get('rule')
            if rule:
                self.add_rule(rule)
                return {'success': True, 'message': '规则已添加'}
            return {'success': False, 'message': '规则为空'}
        
        elif action == 'query':
            subject = input_data.get('subject')
            predicate = input_data.get('predicate')
            obj = input_data.get('obj')
            results = self.query(subject, predicate, obj)
            return {
                'success': True,
                'results': results,
                'count': len(results)
            }
        
        elif action == 'stats':
            return {
                'success': True,
                'stats': self.get_stats()
            }
        
        elif action == 'list':
            return {
                'success': True,
                'rules': self.rules,
                'count': len(self.rules)
            }
        
        return {'success': False, 'message': '未知操作'}
