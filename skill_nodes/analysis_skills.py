from typing import List, Dict, Any
from framework.core import SkillNode

class SentimentSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '情感分析')
        self.description = self.config.get('description', '分析文本情感倾向')
        self.positive_words = {'好', '棒', '优秀', '喜欢', '爱', '开心', '快乐', '幸福'}
        self.negative_words = {'坏', '差', '糟糕', '讨厌', '恨', '伤心', '难过', '痛苦'}
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        text = input_data.get('text', '')
        
        if not text:
            return {'success': False, 'message': '文本为空'}
        
        positive_count = sum(1 for word in self.positive_words if word in text)
        negative_count = sum(1 for word in self.negative_words if word in text)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            label = '积极'
        elif negative_count > positive_count:
            sentiment = 'negative'
            label = '消极'
        else:
            sentiment = 'neutral'
            label = '中性'
        
        return {
            'success': True,
            'text': text,
            'sentiment': sentiment,
            'label': label,
            'positive_count': positive_count,
            'negative_count': negative_count
        }

class KnowledgeGraphSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '知识图谱')
        self.description = self.config.get('description', '构建和查询知识图谱')
        self.triples: List[Dict[str, str]] = []
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        action = input_data.get('action', 'add')
        
        if action == 'add':
            subject = input_data.get('subject')
            relation = input_data.get('relation')
            obj = input_data.get('obj')
            
            if subject and relation and obj:
                self.triples.append({
                    'subject': subject,
                    'relation': relation,
                    'obj': obj
                })
                return {
                    'success': True,
                    'message': '三元组已添加',
                    'triple': {'subject': subject, 'relation': relation, 'obj': obj}
                }
            return {'success': False, 'message': '三元组不完整'}
        
        elif action == 'query':
            subject = input_data.get('subject')
            results = [t for t in self.triples if t['subject'] == subject]
            return {
                'success': True,
                'subject': subject,
                'results': results
            }
        
        elif action == 'list':
            return {
                'success': True,
                'triples': self.triples,
                'count': len(self.triples)
            }
        
        return {'success': False, 'message': '未知操作'}

class ClusteringSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '聚类分析')
        self.description = self.config.get('description', '对数据进行聚类分析')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        data = input_data.get('data', [])
        k = input_data.get('k', 3)
        
        if not data:
            return {'success': False, 'message': '数据为空'}
        
        clusters = {}
        for i, item in enumerate(data):
            cluster_id = i % k
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(item)
        
        return {
            'success': True,
            'data_count': len(data),
            'k': k,
            'clusters': clusters,
            'cluster_sizes': {k: len(v) for k, v in clusters.items()}
        }

class StatisticalSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '统计分析')
        self.description = self.config.get('description', '进行统计分析')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        data = input_data.get('data', [])
        
        if not data:
            return {'success': False, 'message': '数据为空'}
        
        if all(isinstance(x, (int, float)) for x in data):
            mean = sum(data) / len(data)
            sorted_data = sorted(data)
            median = sorted_data[len(sorted_data) // 2]
            min_val = min(data)
            max_val = max(data)
            
            return {
                'success': True,
                'count': len(data),
                'mean': mean,
                'median': median,
                'min': min_val,
                'max': max_val
            }
        
        return {
            'success': True,
            'count': len(data),
            'message': '非数值数据，仅统计数量'
        }
