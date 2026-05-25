from typing import List, Dict, Any
from framework.core import SkillNode

class CausalSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '因果推理')
        self.description = self.config.get('description', '分析因果关系')
        self.causal_rules: List[Dict[str, Any]] = []
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        action = input_data.get('action', 'analyze')
        
        if action == 'add_rule':
            cause = input_data.get('cause')
            effect = input_data.get('effect')
            strength = input_data.get('strength', 0.8)
            
            if cause and effect:
                self.causal_rules.append({
                    'cause': cause,
                    'effect': effect,
                    'strength': strength
                })
                return {'success': True, 'message': '因果规则已添加'}
            return {'success': False, 'message': '缺少原因或结果'}
        
        elif action == 'analyze':
            event = input_data.get('event')
            
            if not event:
                return {'success': False, 'message': '缺少事件'}
            
            causes = []
            effects = []
            
            for rule in self.causal_rules:
                if rule['effect'] == event:
                    causes.append({
                        'cause': rule['cause'],
                        'strength': rule['strength']
                    })
                if rule['cause'] == event:
                    effects.append({
                        'effect': rule['effect'],
                        'strength': rule['strength']
                    })
            
            return {
                'success': True,
                'event': event,
                'possible_causes': causes,
                'possible_effects': effects
            }
        
        elif action == 'predict':
            cause = input_data.get('cause')
            
            if not cause:
                return {'success': False, 'message': '缺少原因'}
            
            predictions = []
            for rule in self.causal_rules:
                if rule['cause'] == cause:
                    predictions.append({
                        'effect': rule['effect'],
                        'probability': rule['strength']
                    })
            
            return {
                'success': True,
                'cause': cause,
                'predictions': predictions
            }
        
        return {'success': False, 'message': '未知操作'}

class TimeSeriesSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '时间序列')
        self.description = self.config.get('description', '时间序列分析')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        action = input_data.get('action', 'analyze')
        data = input_data.get('data', [])
        
        if not data:
            return {'success': False, 'message': '数据为空'}
        
        if action == 'analyze':
            if not all(isinstance(x, (int, float)) for x in data):
                return {'success': False, 'message': '数据必须为数值'}
            
            n = len(data)
            mean = sum(data) / n
            variance = sum((x - mean) ** 2 for x in data) / n
            std_dev = variance ** 0.5
            
            trend = 'stable'
            if n >= 2:
                if data[-1] > data[0] * 1.1:
                    trend = 'increasing'
                elif data[-1] < data[0] * 0.9:
                    trend = 'decreasing'
            
            return {
                'success': True,
                'count': n,
                'mean': round(mean, 2),
                'variance': round(variance, 2),
                'std_dev': round(std_dev, 2),
                'trend': trend,
                'min': min(data),
                'max': max(data)
            }
        
        elif action == 'predict':
            window = input_data.get('window', 3)
            
            if len(data) < window:
                return {'success': False, 'message': '数据不足'}
            
            recent = data[-window:]
            prediction = sum(recent) / window
            
            return {
                'success': True,
                'prediction': round(prediction, 2),
                'method': 'moving_average',
                'window': window
            }
        
        return {'success': False, 'message': '未知操作'}

class ProbabilitySkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '概率推理')
        self.description = self.config.get('description', '概率计算和推理')
        self.distributions: Dict[str, Dict[str, float]] = {}
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        action = input_data.get('action', 'calculate')
        
        if action == 'set_distribution':
            name = input_data.get('name')
            distribution = input_data.get('distribution', {})
            
            if name and distribution:
                total = sum(distribution.values())
                if total > 0:
                    normalized = {k: v / total for k, v in distribution.items()}
                    self.distributions[name] = normalized
                    return {'success': True, 'message': f'分布 {name} 已设置'}
            return {'success': False, 'message': '参数不完整'}
        
        elif action == 'calculate':
            dist_name = input_data.get('distribution')
            event = input_data.get('event')
            
            if dist_name and dist_name in self.distributions:
                dist = self.distributions[dist_name]
                if event in dist:
                    return {
                        'success': True,
                        'event': event,
                        'probability': dist[event]
                    }
                return {
                    'success': True,
                    'event': event,
                    'probability': 0.0,
                    'message': '事件不在分布中'
                }
            
            prob = input_data.get('probability', 0.5)
            trials = input_data.get('trials', 1)
            
            results = {
                'probability': prob,
                'trials': trials,
                'expected': round(prob * trials, 2),
                'variance': round(prob * (1 - prob) * trials, 2)
            }
            
            return {'success': True, 'results': results}
        
        elif action == 'bayes':
            prior = input_data.get('prior', 0.5)
            likelihood = input_data.get('likelihood', 0.8)
            evidence = input_data.get('evidence', 0.6)
            
            if evidence == 0:
                return {'success': False, 'message': '证据概率不能为0'}
            
            posterior = (likelihood * prior) / evidence
            
            return {
                'success': True,
                'prior': prior,
                'likelihood': likelihood,
                'evidence': evidence,
                'posterior': round(posterior, 4)
            }
        
        return {'success': False, 'message': '未知操作'}

class AttentionSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '注意力机制')
        self.description = self.config.get('description', '计算注意力权重')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        query = input_data.get('query', [])
        keys = input_data.get('keys', [])
        values = input_data.get('values', [])
        
        if not query or not keys:
            return {'success': False, 'message': '缺少查询或键'}
        
        if not values:
            values = keys
        
        scores = []
        for key in keys:
            score = sum(q * k for q, k in zip(query, key)) if isinstance(key, list) else query[0] * key
            scores.append(score)
        
        max_score = max(scores) if scores else 0
        exp_scores = [pow(2.718, s - max_score) for s in scores]
        sum_exp = sum(exp_scores)
        attention_weights = [e / sum_exp for e in exp_scores]
        
        output = [0] * len(values[0]) if values and isinstance(values[0], list) else 0
        
        for i, weight in enumerate(attention_weights):
            if isinstance(values[i], list):
                for j, v in enumerate(values[i]):
                    if j < len(output):
                        output[j] += weight * v
            else:
                output += weight * values[i]
        
        return {
            'success': True,
            'attention_weights': [round(w, 4) for w in attention_weights],
            'output': output if isinstance(output, list) else round(output, 4)
        }

class ContextSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '上下文管理')
        self.description = self.config.get('description', '管理对话上下文')
        self.contexts: Dict[str, List[Dict[str, Any]]] = {}
        self.max_context_length = self.config.get('max_length', 10)
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        action = input_data.get('action', 'get')
        context_id = input_data.get('context_id', 'default')
        
        if action == 'add':
            message = input_data.get('message')
            role = input_data.get('role', 'user')
            
            if not message:
                return {'success': False, 'message': '消息为空'}
            
            if context_id not in self.contexts:
                self.contexts[context_id] = []
            
            self.contexts[context_id].append({
                'role': role,
                'message': message,
                'timestamp': input_data.get('timestamp')
            })
            
            if len(self.contexts[context_id]) > self.max_context_length:
                self.contexts[context_id] = self.contexts[context_id][-self.max_context_length:]
            
            return {
                'success': True,
                'context_id': context_id,
                'message_count': len(self.contexts[context_id])
            }
        
        elif action == 'get':
            if context_id not in self.contexts:
                return {
                    'success': True,
                    'context_id': context_id,
                    'messages': [],
                    'count': 0
                }
            
            return {
                'success': True,
                'context_id': context_id,
                'messages': self.contexts[context_id],
                'count': len(self.contexts[context_id])
            }
        
        elif action == 'clear':
            if context_id in self.contexts:
                del self.contexts[context_id]
            
            return {
                'success': True,
                'message': f'上下文 {context_id} 已清空'
            }
        
        elif action == 'summary':
            if context_id not in self.contexts:
                return {
                    'success': True,
                    'context_id': context_id,
                    'summary': '无上下文'
                }
            
            messages = self.contexts[context_id]
            roles = {}
            for msg in messages:
                role = msg['role']
                roles[role] = roles.get(role, 0) + 1
            
            return {
                'success': True,
                'context_id': context_id,
                'total_messages': len(messages),
                'role_distribution': roles
            }
        
        return {'success': False, 'message': '未知操作'}
