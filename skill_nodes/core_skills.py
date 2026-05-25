from typing import List, Dict, Any
from core import SkillNode

class ReasoningSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = config.get('name', '推理技能')
        self.description = config.get('description', '基础推理能力')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        action = input_data.get('action', 'reason')
        
        if action == 'reason':
            return self._reason(input_data)
        elif action == 'validate':
            return self._validate(input_data)
        else:
            return {'success': False, 'message': '未知操作'}
    
    def _reason(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        premises = input_data.get('premises', [])
        
        if not premises:
            return {'success': False, 'message': '缺少前提'}
        
        result = {
            'success': True,
            'premises': premises,
            'conclusion': f"基于 {len(premises)} 个前提进行推理",
            'confidence': self.confidence
        }
        
        return result
    
    def _validate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        premise = input_data.get('premise')
        conclusion = input_data.get('conclusion')
        
        if not premise or not conclusion:
            return {'success': False, 'message': '缺少前提或结论'}
        
        return {
            'success': True,
            'valid': True,
            'premise': premise,
            'conclusion': conclusion
        }

class GenerationSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = config.get('name', '生成技能')
        self.description = config.get('description', '基础生成能力')
        self.templates = {
            'poetry': ['春', '夏', '秋', '冬'],
            'article': ['引言', '正文', '结论'],
            'dialogue': ['你好', '再见']
        }
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        action = input_data.get('action', 'generate')
        
        if action == 'generate':
            return self._generate(input_data)
        elif action == 'get_templates':
            return self._get_templates()
        else:
            return {'success': False, 'message': '未知操作'}
    
    def _generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content_type = input_data.get('type', 'article')
        length = input_data.get('length', 3)
        
        if content_type not in self.templates:
            return {'success': False, 'message': f'不支持的类型: {content_type}'}
        
        template = self.templates[content_type]
        generated = template[:length]
        
        return {
            'success': True,
            'type': content_type,
            'content': generated,
            'length': len(generated)
        }
    
    def _get_templates(self) -> Dict[str, Any]:
        return {
            'success': True,
            'templates': list(self.templates.keys())
        }

class AnalysisSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = config.get('name', '分析技能')
        self.description = config.get('description', '基础分析能力')
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        action = input_data.get('action', 'analyze')
        
        if action == 'analyze':
            return self._analyze(input_data)
        elif action == 'summarize':
            return self._summarize(input_data)
        else:
            return {'success': False, 'message': '未知操作'}
    
    def _analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        text = input_data.get('text', '')
        
        if not text:
            return {'success': False, 'message': '文本为空'}
        
        analysis = {
            'success': True,
            'text': text,
            'length': len(text),
            'words': len(text.split()),
            'sentences': text.count('。') + text.count('！') + text.count('？')
        }
        
        return analysis
    
    def _summarize(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        text = input_data.get('text', '')
        
        if not text:
            return {'success': False, 'message': '文本为空'}
        
        summary = text[:50] + '...' if len(text) > 50 else text
        
        return {
            'success': True,
            'original_length': len(text),
            'summary': summary,
            'summary_length': len(summary)
        }
