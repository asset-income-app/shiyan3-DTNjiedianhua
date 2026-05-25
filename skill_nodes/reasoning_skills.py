from typing import List, Dict, Any
from framework.core import SkillNode

class TransitivitySkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '传递推理')
        self.description = self.config.get('description', '传递性推理：如果 A→B 且 B→C，则 A→C')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        rules = input_data.get('rules', [])
        
        if not rules:
            return {'success': False, 'message': '缺少规则', 'new_rules': []}
        
        new_rules = []
        
        for rule1 in rules:
            if rule1.get('predicate') != "是":
                continue
            
            for rule2 in rules:
                if rule2.get('subject') == rule1.get('obj') and rule2.get('predicate') == "有":
                    new_rule = {
                        'subject': rule1.get('subject'),
                        'predicate': "有",
                        'obj': rule2.get('obj'),
                        'confidence': min(rule1.get('confidence', 1.0), rule2.get('confidence', 1.0)) * 0.9,
                        'source': "传递性推理"
                    }
                    new_rules.append(new_rule)
        
        return {
            'success': True,
            'input_rules': len(rules),
            'new_rules': new_rules,
            'new_rules_count': len(new_rules)
        }

class InductionSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '归纳推理')
        self.description = self.config.get('description', '归纳推理：从具体案例中总结规律')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        cases = input_data.get('cases', [])
        
        if not cases:
            return {'success': False, 'message': '缺少案例', 'patterns': []}
        
        patterns = {}
        
        for case in cases:
            subject = case.get('subject')
            predicate = case.get('predicate')
            obj = case.get('obj')
            
            key = f"{predicate}→{obj}"
            if key not in patterns:
                patterns[key] = {'subjects': [], 'count': 0}
            
            patterns[key]['subjects'].append(subject)
            patterns[key]['count'] += 1
        
        results = []
        for key, data in patterns.items():
            if data['count'] >= 2:
                predicate, obj = key.split('→')
                results.append({
                    'predicate': predicate,
                    'obj': obj,
                    'subjects': data['subjects'],
                    'count': data['count'],
                    'confidence': min(data['count'] / 10.0, 1.0)
                })
        
        return {
            'success': True,
            'input_cases': len(cases),
            'patterns': results,
            'patterns_count': len(results)
        }

class DeductionSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '演绎推理')
        self.description = self.config.get('description', '演绎推理：从一般规则推导具体结论')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        rules = input_data.get('rules', [])
        facts = input_data.get('facts', [])
        
        if not rules or not facts:
            return {'success': False, 'message': '缺少规则或事实', 'conclusions': []}
        
        conclusions = []
        
        for fact in facts:
            for rule in rules:
                if fact.get('subject') == rule.get('subject') and fact.get('predicate') == rule.get('predicate'):
                    conclusion = {
                        'subject': fact.get('subject'),
                        'predicate': rule.get('conclusion_predicate', '是'),
                        'obj': rule.get('conclusion_obj', rule.get('obj')),
                        'confidence': fact.get('confidence', 1.0) * rule.get('confidence', 1.0),
                        'source': "演绎推理"
                    }
                    conclusions.append(conclusion)
        
        return {
            'success': True,
            'input_rules': len(rules),
            'input_facts': len(facts),
            'conclusions': conclusions,
            'conclusions_count': len(conclusions)
        }

class AbductionSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '溯因推理')
        self.description = self.config.get('description', '溯因推理：从结果推断最可能的原因')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        rules = input_data.get('rules', [])
        observation = input_data.get('observation')
        
        if not rules or not observation:
            return {'success': False, 'message': '缺少规则或观察', 'causes': []}
        
        causes = []
        
        for rule in rules:
            if rule.get('obj') == observation.get('obj') and rule.get('predicate') == observation.get('predicate'):
                cause = {
                    'subject': rule.get('subject'),
                    'predicate': rule.get('predicate'),
                    'obj': rule.get('obj'),
                    'confidence': rule.get('confidence', 1.0) * 0.8,
                    'source': "溯因推理"
                }
                causes.append(cause)
        
        causes.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'success': True,
            'observation': observation,
            'causes': causes[:5],
            'causes_count': len(causes)
        }

class AnalogySkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '类比推理')
        self.description = self.config.get('description', '类比推理：基于相似性进行推理')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        source = input_data.get('source')
        target = input_data.get('target')
        
        if not source or not target:
            return {'success': False, 'message': '缺少源或目标', 'analogies': []}
        
        analogies = []
        
        source_attrs = source.get('attributes', {})
        target_attrs = target.get('attributes', {})
        
        for attr, value in source_attrs.items():
            if attr not in target_attrs:
                analogy = {
                    'attribute': attr,
                    'source_value': value,
                    'confidence': 0.7,
                    'source': "类比推理"
                }
                analogies.append(analogy)
        
        return {
            'success': True,
            'source': source,
            'target': target,
            'analogies': analogies,
            'analogies_count': len(analogies)
        }
