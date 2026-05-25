from typing import List, Dict, Any
from framework.core import FuncNode
import time

class PerformanceFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '性能监控')
        self.description = self.config.get('description', '监控系统性能')
        self.metrics: Dict[str, List[Dict[str, Any]]] = {}
    
    def _execute(self, input_data: Any) -> Any:
        action = input_data.get('action', 'record')
        
        if action == 'record':
            metric_name = input_data.get('metric')
            value = input_data.get('value')
            
            if not metric_name or value is None:
                return {'success': False, 'message': '缺少指标名或值'}
            
            if metric_name not in self.metrics:
                self.metrics[metric_name] = []
            
            self.metrics[metric_name].append({
                'value': value,
                'timestamp': time.time()
            })
            
            return {
                'success': True,
                'metric': metric_name,
                'value': value,
                'count': len(self.metrics[metric_name])
            }
        
        elif action == 'stats':
            metric_name = input_data.get('metric')
            
            if not metric_name or metric_name not in self.metrics:
                return {'success': False, 'message': '指标不存在'}
            
            values = [m['value'] for m in self.metrics[metric_name]]
            
            if not values:
                return {'success': True, 'count': 0}
            
            return {
                'success': True,
                'metric': metric_name,
                'count': len(values),
                'mean': round(sum(values) / len(values), 2),
                'min': min(values),
                'max': max(values),
                'latest': values[-1]
            }
        
        elif action == 'list':
            return {
                'success': True,
                'metrics': list(self.metrics.keys()),
                'count': len(self.metrics)
            }
        
        return {'success': False, 'message': '未知操作'}

class LoggerFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '日志记录')
        self.description = self.config.get('description', '记录系统日志')
        self.logs: List[Dict[str, Any]] = []
        self.max_logs = self.config.get('max_logs', 1000)
        self.levels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}
        self.min_level = self.config.get('min_level', 'INFO')
    
    def _execute(self, input_data: Any) -> Any:
        action = input_data.get('action', 'log')
        
        if action == 'log':
            level = input_data.get('level', 'INFO')
            message = input_data.get('message')
            
            if not message:
                return {'success': False, 'message': '日志消息为空'}
            
            if self.levels.get(level, 1) < self.levels.get(self.min_level, 1):
                return {'success': True, 'message': '日志级别过低，已忽略'}
            
            log_entry = {
                'level': level,
                'message': message,
                'timestamp': time.time(),
                'source': input_data.get('source', 'unknown')
            }
            
            self.logs.append(log_entry)
            
            if len(self.logs) > self.max_logs:
                self.logs = self.logs[-self.max_logs:]
            
            return {
                'success': True,
                'log_id': len(self.logs) - 1
            }
        
        elif action == 'get':
            level = input_data.get('level')
            limit = input_data.get('limit', 100)
            
            logs = self.logs
            if level:
                logs = [l for l in logs if l['level'] == level]
            
            return {
                'success': True,
                'logs': logs[-limit:],
                'count': len(logs[-limit:])
            }
        
        elif action == 'clear':
            count = len(self.logs)
            self.logs.clear()
            return {
                'success': True,
                'cleared': count
            }
        
        return {'success': False, 'message': '未知操作'}

class CacheFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '缓存管理')
        self.description = self.config.get('description', '数据缓存')
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = self.config.get('default_ttl', 3600)
    
    def _execute(self, input_data: Any) -> Any:
        action = input_data.get('action', 'get')
        
        if action == 'set':
            key = input_data.get('key')
            value = input_data.get('value')
            ttl = input_data.get('ttl', self.default_ttl)
            
            if not key:
                return {'success': False, 'message': '缺少键'}
            
            self.cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl
            }
            
            return {
                'success': True,
                'key': key,
                'ttl': ttl
            }
        
        elif action == 'get':
            key = input_data.get('key')
            
            if not key:
                return {'success': False, 'message': '缺少键'}
            
            if key not in self.cache:
                return {
                    'success': True,
                    'found': False,
                    'key': key
                }
            
            entry = self.cache[key]
            
            if time.time() > entry['expires_at']:
                del self.cache[key]
                return {
                    'success': True,
                    'found': False,
                    'key': key,
                    'message': '缓存已过期'
                }
            
            return {
                'success': True,
                'found': True,
                'key': key,
                'value': entry['value']
            }
        
        elif action == 'delete':
            key = input_data.get('key')
            
            if key in self.cache:
                del self.cache[key]
                return {'success': True, 'message': f'已删除 {key}'}
            
            return {'success': True, 'message': '键不存在'}
        
        elif action == 'clear':
            count = len(self.cache)
            self.cache.clear()
            return {
                'success': True,
                'cleared': count
            }
        
        elif action == 'stats':
            now = time.time()
            valid = sum(1 for e in self.cache.values() if e['expires_at'] > now)
            expired = len(self.cache) - valid
            
            return {
                'success': True,
                'total': len(self.cache),
                'valid': valid,
                'expired': expired
            }
        
        return {'success': False, 'message': '未知操作'}

class TransformFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '数据转换')
        self.description = self.config.get('description', '数据格式转换')
    
    def _execute(self, input_data: Any) -> Any:
        action = input_data.get('action', 'transform')
        data = input_data.get('data')
        
        if data is None:
            return {'success': False, 'message': '数据为空'}
        
        if action == 'to_list':
            if isinstance(data, list):
                result = data
            elif isinstance(data, dict):
                result = list(data.items())
            else:
                result = [data]
            
            return {'success': True, 'result': result}
        
        elif action == 'to_dict':
            if isinstance(data, dict):
                result = data
            elif isinstance(data, list):
                result = {str(i): v for i, v in enumerate(data)}
            else:
                result = {'value': data}
            
            return {'success': True, 'result': result}
        
        elif action == 'flatten':
            def flatten(obj):
                if isinstance(obj, list):
                    return [item for sublist in obj for item in flatten(sublist)]
                elif isinstance(obj, dict):
                    return list(obj.values())
                return [obj]
            
            result = flatten(data)
            return {'success': True, 'result': result}
        
        elif action == 'unique':
            if isinstance(data, list):
                seen = set()
                result = []
                for item in data:
                    key = str(item) if not isinstance(item, (int, float, str)) else item
                    if key not in seen:
                        seen.add(key)
                        result.append(item)
                return {'success': True, 'result': result}
            
            return {'success': True, 'result': data}
        
        elif action == 'filter':
            condition = input_data.get('condition', {})
            
            if isinstance(data, list):
                result = []
                for item in data:
                    match = True
                    for key, value in condition.items():
                        if isinstance(item, dict):
                            if item.get(key) != value:
                                match = False
                                break
                    if match:
                        result.append(item)
                return {'success': True, 'result': result}
            
            return {'success': True, 'result': data}
        
        return {'success': False, 'message': '未知操作'}

class SchedulerFunc(FuncNode):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = self.config.get('name', '任务调度')
        self.description = self.config.get('description', '管理定时任务')
        self.tasks: Dict[str, Dict[str, Any]] = {}
    
    def _execute(self, input_data: Any) -> Any:
        action = input_data.get('action', 'list')
        
        if action == 'add':
            task_id = input_data.get('task_id')
            task_type = input_data.get('type', 'once')
            interval = input_data.get('interval', 60)
            
            if not task_id:
                return {'success': False, 'message': '缺少任务ID'}
            
            self.tasks[task_id] = {
                'type': task_type,
                'interval': interval,
                'created_at': time.time(),
                'next_run': time.time() + interval,
                'runs': 0,
                'status': 'active'
            }
            
            return {
                'success': True,
                'task_id': task_id,
                'next_run': self.tasks[task_id]['next_run']
            }
        
        elif action == 'remove':
            task_id = input_data.get('task_id')
            
            if task_id in self.tasks:
                del self.tasks[task_id]
                return {'success': True, 'message': f'任务 {task_id} 已删除'}
            
            return {'success': False, 'message': '任务不存在'}
        
        elif action == 'pause':
            task_id = input_data.get('task_id')
            
            if task_id in self.tasks:
                self.tasks[task_id]['status'] = 'paused'
                return {'success': True, 'message': f'任务 {task_id} 已暂停'}
            
            return {'success': False, 'message': '任务不存在'}
        
        elif action == 'resume':
            task_id = input_data.get('task_id')
            
            if task_id in self.tasks:
                self.tasks[task_id]['status'] = 'active'
                self.tasks[task_id]['next_run'] = time.time() + self.tasks[task_id]['interval']
                return {'success': True, 'message': f'任务 {task_id} 已恢复'}
            
            return {'success': False, 'message': '任务不存在'}
        
        elif action == 'list':
            return {
                'success': True,
                'tasks': self.tasks,
                'count': len(self.tasks)
            }
        
        elif action == 'check':
            now = time.time()
            ready = []
            
            for task_id, task in self.tasks.items():
                if task['status'] == 'active' and now >= task['next_run']:
                    ready.append(task_id)
                    task['runs'] += 1
                    task['next_run'] = now + task['interval']
            
            return {
                'success': True,
                'ready_tasks': ready,
                'count': len(ready)
            }
        
        return {'success': False, 'message': '未知操作'}
