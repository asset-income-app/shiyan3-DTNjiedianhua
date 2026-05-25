from framework.core import Node, NodeType, SkillNode, RuleNode, DataNode, FuncNode
from framework.registry import NodeRegistry, NodeScheduler
from skill_nodes.core_skills import ReasoningSkill, GenerationSkill, AnalysisSkill

def demo_new_architecture():
    print("=" * 70)
    print("🎯 DTN 新架构演示 - 第一性原理 + 极简设计")
    print("=" * 70)
    print()
    
    print("【1. 创建节点】")
    print()
    
    reasoning = ReasoningSkill({
        'name': '推理引擎',
        'description': '强大的推理能力',
        'priority': 1.0,
        'confidence': 0.95
    })
    
    generation = GenerationSkill({
        'name': '生成引擎',
        'description': '创意生成能力',
        'priority': 0.9,
        'confidence': 0.85
    })
    
    analysis = AnalysisSkill({
        'name': '分析引擎',
        'description': '深度分析能力',
        'priority': 0.95,
        'confidence': 0.9
    })
    
    knowledge = RuleNode({
        'name': '知识库',
        'description': '存储规则和知识'
    })
    
    memory = DataNode({
        'name': '记忆库',
        'description': '存储状态和数据'
    })
    
    print(f"✓ 创建 {reasoning.get_name()} (类型: {reasoning.get_type().value})")
    print(f"✓ 创建 {generation.get_name()} (类型: {generation.get_type().value})")
    print(f"✓ 创建 {analysis.get_name()} (类型: {analysis.get_type().value})")
    print(f"✓ 创建 {knowledge.get_name()} (类型: {knowledge.get_type().value})")
    print(f"✓ 创建 {memory.get_name()} (类型: {memory.get_type().value})")
    print()
    
    print("【2. 注册节点】")
    print()
    
    registry = NodeRegistry()
    
    registry.register(reasoning)
    registry.register(generation)
    registry.register(analysis)
    registry.register(knowledge)
    registry.register(memory)
    
    registry.print_stats()
    print()
    
    print("【3. 调度器执行】")
    print()
    
    scheduler = NodeScheduler(registry)
    
    print("执行推理:")
    result = scheduler.execute_by_name('推理引擎', {
        'action': 'reason',
        'premises': ['所有人都会死', '苏格拉底是人']
    })
    print(f"  结果: {result}")
    print()
    
    print("执行生成:")
    result = scheduler.execute_by_name('生成引擎', {
        'action': 'generate',
        'type': 'poetry',
        'length': 2
    })
    print(f"  结果: {result}")
    print()
    
    print("执行分析:")
    result = scheduler.execute_by_name('分析引擎', {
        'action': 'analyze',
        'text': '今天天气真好，我很开心！'
    })
    print(f"  结果: {result}")
    print()
    
    print("【4. 数据节点操作】")
    print()
    
    memory.set('user_name', '张三')
    memory.set('user_age', 25)
    memory.set('last_login', '2024-01-01')
    
    print(f"设置数据:")
    print(f"  user_name = {memory.get('user_name')}")
    print(f"  user_age = {memory.get('user_age')}")
    print(f"  last_login = {memory.get('last_login')}")
    print()
    
    print(f"所有数据: {memory.get_all()}")
    print()
    
    print("【5. 规则节点操作】")
    print()
    
    knowledge.add_rule("如果A则B")
    knowledge.add_rule("如果B则C")
    knowledge.add_rule("如果C则D")
    
    print(f"添加规则:")
    print(f"  {knowledge.get_rules()}")
    print()
    
    print("【6. 执行历史】")
    print()
    
    history = scheduler.get_execution_history()
    print(f"执行记录 ({len(history)} 条):")
    for i, record in enumerate(history, 1):
        status = "✓" if record['success'] else "✗"
        print(f"  {i}. {status} {record['node_name']} ({record['node_type']})")
    print()
    
    print("【7. 节点查找】")
    print()
    
    node = registry.find_by_name('推理引擎')
    if node:
        print(f"找到节点: {node.get_name()}")
        print(f"  ID: {node.get_id()}")
        print(f"  类型: {node.get_type().value}")
        print(f"  优先级: {node.get_priority()}")
        print(f"  置信度: {node.get_confidence()}")
        print(f"  使用次数: {node.get_usage_count()}")
    print()
    
    print("【8. 按类型查询】")
    print()
    
    skill_nodes = registry.get_nodes_by_type(NodeType.SKILL)
    print(f"技能节点 ({len(skill_nodes)} 个):")
    for node in skill_nodes:
        print(f"  - {node.get_name()}")
    print()
    
    rule_nodes = registry.get_nodes_by_type(NodeType.RULE)
    print(f"规则节点 ({len(rule_nodes)} 个):")
    for node in rule_nodes:
        print(f"  - {node.get_name()}")
    print()
    
    data_nodes = registry.get_nodes_by_type(NodeType.DATA)
    print(f"数据节点 ({len(data_nodes)} 个):")
    for node in data_nodes:
        print(f"  - {node.get_name()}")
    print()
    
    print("【9. 节点启用/禁用】")
    print()
    
    print(f"禁用 {generation.get_name()}")
    registry.disable_node(generation.get_id())
    
    enabled_nodes = registry.get_enabled_nodes()
    print(f"启用节点 ({len(enabled_nodes)} 个):")
    for node in enabled_nodes:
        print(f"  - {node.get_name()}")
    print()
    
    print(f"重新启用 {generation.get_name()}")
    registry.enable_node(generation.get_id())
    
    enabled_nodes = registry.get_enabled_nodes()
    print(f"启用节点 ({len(enabled_nodes)} 个):")
    for node in enabled_nodes:
        print(f"  - {node.get_name()}")
    print()
    
    print("=" * 70)
    print("🎯 新架构演示完成！")
    print("=" * 70)
    print()
    print("核心优势：")
    print("  ✅ 清晰的节点类型区分")
    print("  ✅ 统一的注册和调度")
    print("  ✅ 简洁的接口设计")
    print("  ✅ 高效的执行机制")
    print("  ✅ 完整的历史记录")
    print()

def demo_comparison():
    print("=" * 70)
    print("📊 旧架构 vs 新架构对比")
    print("=" * 70)
    print()
    
    print("【旧架构】")
    print("  ❌ 所有节点都叫 SkillNode")
    print("  ❌ 命名混乱（技能、规则、数据混在一起）")
    print("  ❌ 概念不清（节点 vs 技能）")
    print("  ❌ 基类单一（只有 SkillNode）")
    print()
    
    print("【新架构】")
    print("  ✅ 清晰的节点类型（SkillNode, RuleNode, DataNode, FuncNode）")
    print("  ✅ 明确的职责分工")
    print("  ✅ 清晰的概念层次（Node → 具体类型）")
    print("  ✅ 统一的注册表和调度器")
    print("  ✅ 完整的执行历史")
    print()
    
    print("【对比表】")
    print()
    print("特性              旧架构    新架构")
    print("-" * 50)
    print("节点类型区分      ❌        ✅")
    print("命名清晰度        ❌        ✅")
    print("概念层次          ❌        ✅")
    print("统一管理          ❌        ✅")
    print("执行历史          ❌        ✅")
    print("类型查询          ❌        ✅")
    print("启用/禁用         ✅        ✅")
    print("性能监控          ❌        ✅")
    print()

def demo_health_check():
    print("=" * 70)
    print("🏥 系统健康度检查")
    print("=" * 70)
    print()
    
    registry = NodeRegistry()
    
    reasoning = ReasoningSkill({'name': '推理'})
    generation = GenerationSkill({'name': '生成'})
    analysis = AnalysisSkill({'name': '分析'})
    knowledge = RuleNode({'name': '知识库'})
    memory = DataNode({'name': '记忆库'})
    
    for node in [reasoning, generation, analysis, knowledge, memory]:
        registry.register(node)
    
    stats = registry.get_stats()
    
    print("【节点统计】")
    print(f"  总节点数: {stats['total_nodes']}")
    print(f"  启用节点: {stats['enabled_nodes']}")
    print(f"  技能节点: {stats['skill_nodes']}")
    print(f"  规则节点: {stats['rule_nodes']}")
    print(f"  数据节点: {stats['data_nodes']}")
    print(f"  功能节点: {stats['func_nodes']}")
    print()
    
    print("【健康度评估】")
    health_score = 0
    
    if stats['skill_nodes'] >= 3:
        health_score += 30
        print("  ✓ 技能节点充足 (+30)")
    else:
        print("  ✗ 技能节点不足")
    
    if stats['rule_nodes'] >= 1:
        health_score += 20
        print("  ✓ 规则节点存在 (+20)")
    else:
        print("  ✗ 缺少规则节点")
    
    if stats['data_nodes'] >= 1:
        health_score += 20
        print("  ✓ 数据节点存在 (+20)")
    else:
        print("  ✗ 缺少数据节点")
    
    if stats['total_nodes'] >= 5:
        health_score += 15
        print("  ✓ 节点数量充足 (+15)")
    else:
        print("  ✗ 节点数量不足")
    
    if stats['enabled_nodes'] == stats['total_nodes']:
        health_score += 15
        print("  ✓ 所有节点启用 (+15)")
    else:
        print("  ✗ 部分节点禁用")
    
    print()
    print(f"健康分数: {health_score}/100")
    
    if health_score >= 90:
        print("评级: 优秀 ⭐⭐⭐⭐⭐")
    elif health_score >= 70:
        print("评级: 良好 ⭐⭐⭐")
    elif health_score >= 50:
        print("评级: 及格 ⭐⭐")
    else:
        print("评级: 需改进 ⭐")
    print()

if __name__ == "__main__":
    demo_new_architecture()
    print()
    demo_comparison()
    print()
    demo_health_check()
