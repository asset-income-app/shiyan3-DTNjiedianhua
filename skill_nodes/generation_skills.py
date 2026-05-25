from typing import List, Dict, Any
from framework.core import SkillNode

class PoetrySkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '写诗')
        self.description = self.config.get('description', '诗歌创作能力')
        self.templates = {
            '五言': ['春', '夏', '秋', '冬', '山', '水', '云', '月'],
            '七言': ['春风', '夏雨', '秋叶', '冬雪', '青山', '绿水', '白云', '明月']
        }
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        theme = input_data.get('theme', '自然')
        style = input_data.get('style', '五言')
        lines = input_data.get('lines', 4)
        
        if style not in self.templates:
            style = '五言'
        
        words = self.templates[style]
        
        poem = []
        for i in range(lines):
            line = words[i % len(words)] * (5 if style == '五言' else 7)
            poem.append(line)
        
        return {
            'success': True,
            'theme': theme,
            'style': style,
            'poem': poem,
            'lines': lines
        }

class ArticleSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '写文章')
        self.description = self.config.get('description', '文章创作能力')
        self.structure = ['引言', '正文', '结论']
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        topic = input_data.get('topic', '未指定主题')
        length = input_data.get('length', 3)
        
        article = {
            'title': f"关于{topic}的思考",
            'sections': []
        }
        
        for i, section in enumerate(self.structure[:length]):
            article['sections'].append({
                'name': section,
                'content': f"{section}部分：关于{topic}的讨论..."
            })
        
        return {
            'success': True,
            'topic': topic,
            'article': article,
            'length': length
        }

class DialogueSkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '对话')
        self.description = self.config.get('description', '对话生成能力')
        self.responses = {
            '你好': '你好！有什么可以帮助你的吗？',
            '再见': '再见！祝你愉快！',
            '谢谢': '不客气！',
            '怎么样': '我很好，谢谢关心！'
        }
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        message = input_data.get('message', '')
        context = input_data.get('context', [])
        
        response = self.responses.get(message, f"我理解你说的是：{message}")
        
        return {
            'success': True,
            'input': message,
            'response': response,
            'context': context
        }

class CreativitySkill(SkillNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '创意')
        self.description = self.config.get('description', '创意生成能力')
        self.ideas = [
            '将两个不相关的概念结合起来',
            '从相反的角度思考问题',
            '借鉴其他领域的解决方案',
            '简化复杂的问题',
            '增加新的维度'
        ]
    
    def execute(self, input_data: Any) -> Any:
        self.increment_usage()
        
        problem = input_data.get('problem', '')
        count = input_data.get('count', 3)
        
        ideas = self.ideas[:count]
        
        return {
            'success': True,
            'problem': problem,
            'ideas': ideas,
            'count': len(ideas)
        }
