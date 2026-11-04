# -*- coding: utf-8 -*-
"""知识库最小校验：ID 一致性 / 必填字段 / 引用有效性
不依赖 PyYAML（文本级检查），供每次知识库变更后运行。
用法: python scripts/validate_knowledge.py  （在仓库根目录执行）
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRIT = ROOT / 'knowledge' / 'criteria'
INDEX = ROOT / 'knowledge' / 'index.md'
EVID = ROOT / 'knowledge' / 'evidence' / 'wiserui-checkout-cases.yaml'

REQUIRED_FIELDS = [
    'id:', 'name:', 'version:', 'domain:', 'perspective:',
    'applicable_context:', 'evaluation_goal:', 'check_questions:',
    'judgment_rules:', 'sources:', 'evidence_requirements:',
    'boundaries:', 'output_contract:',
]
# 待补全条目（无独立 YAML，但在 index 总览中登记）
KNOWN_STUBS = {f'C{i:02d}' for i in list(range(1, 15))} - {'C05'}

errors, warnings = [], []

# 1. 条目文件检查
yaml_ids = {}
for f in sorted(CRIT.glob('C*.yaml')):
    text = f.read_text(encoding='utf-8')
    m = re.search(r'^id:\s*(C\d+)\s*$', text, re.M)
    if not m:
        errors.append(f'{f.name}: 缺 id 字段')
        continue
    cid = m.group(1)
    yaml_ids[cid] = f.name
    if f.stem != cid:
        errors.append(f'{f.name}: 文件名与 id({cid})不一致')
    for field in REQUIRED_FIELDS:
        if field not in text:
            errors.append(f'{f.name}: 缺必填字段 {field}')
    if 'machine_check: true' in text and 'E1' not in text:
        errors.append(f'{f.name}: 机检条目来源中未标注 E1')

# 2. index.md 同步检查
index_text = INDEX.read_text(encoding='utf-8')
for cid in yaml_ids:
    if cid not in index_text:
        errors.append(f'index.md: 全字段条目 {cid} 未在总览登记')
for cid in sorted(KNOWN_STUBS):
    if cid not in index_text:
        warnings.append(f'index.md: 待补全条目 {cid} 未出现（是否已删除？）')

# 3. 文档/模板/示例中的条目引用检查
valid_refs = set(yaml_ids) | KNOWN_STUBS
for target in [ROOT / 'SKILL.md', *sorted((ROOT / 'templates').glob('*.md')),
               *sorted((ROOT / 'examples').glob('*.md')), ROOT / 'README.md']:
    text = target.read_text(encoding='utf-8')
    for ref in set(re.findall(r'\bC(\d{2})\b', text)):
        cid = 'C' + ref
        if cid not in valid_refs:
            errors.append(f'{target.name}: 引用了未登记条目 {cid}')

# 4. 证据登记册引用检查
if EVID.exists():
    evid_text = EVID.read_text(encoding='utf-8')
    case_ids = set(re.findall(r'case_id: (WUI-\d+)', evid_text))
    for target in [ROOT / 'SKILL.md', *sorted((ROOT / 'knowledge' / 'criteria').glob('*.yaml'))]:
        text = target.read_text(encoding='utf-8')
        for ref in set(re.findall(r'(WUI-\d+)', text)):
            if ref not in case_ids:
                errors.append(f'{target.name}: 引用了不存在的证据案例 {ref}')
else:
    warnings.append('knowledge/evidence/wiserui-checkout-cases.yaml 不存在')

print(f'检查条目 YAML: {len(yaml_ids)} 个（另 {len(KNOWN_STUBS)} 个待补全条目）')
print(f'错误 {len(errors)} 项:')
for e in errors:
    print(f'  ✗ {e}')
print(f'提醒 {len(warnings)} 项:')
for w in warnings:
    print(f'  ! {w}')
sys.exit(1 if errors else 0)
