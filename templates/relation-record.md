# 关系记录模板（M3 输出契约）

> 七种关系的完整操作化定义（必要条件、正反例、判定决策树）见 `../docs/02`；本文件是可直接填写的运行时模板

## 判定流程（五步决策树摘要）

```
Step 0 对象锚定：无共享 UI 对象且无共享任务步骤 → 无关系（independent），不进入分析
Step 1 事实层：observed_fact 直接冲突（无法同时为真）→ Contradiction（触发 E1 核查）
             事实一致且问题判断同向、指向同一问题 → Support
Step 2 策略层：建议互斥（一个移除另一个的作用对象）→ 转 Step 3
             建议存在先后 / 包含关系 → Dependency
             建议兼容 → 转 Step 3
Step 3 目标层：共享有限资源（注意力/空间/信息密度/步骤/时间）且此消彼长 → Trade-off
             共享改进目标且协同 → Complement
Step 4 条件层：applies_to 不同、各自条件内均成立 → Conditional
Step 5 兜底：→ Uncertain（必须附缺失证据清单，禁止作为偷懒出口）
```

## 模板

```yaml
relation_id: REL-___
record_pair: [C__-__, C__-__]
primary_relation:         # Support / Contradiction / Complement / Trade-off / Dependency / Conditional / Uncertain
analysis_layer:           # 事实 / 策略 / 目标
judgment_basis:           # 引用具体字段值，禁止只写语义相似
  - "共享资源："
  - "A evaluation_goal=…；B evaluation_goal=…"
resolution_path:          # 化解路径（如适用）
verification_status:
action:                   # 合并 / 核查 / QOC / 排序 / 条件化 / 生成验证任务
```

## 示例

```yaml
relation_id: REL-001
record_pair: [C04-01, C05-01]
primary_relation: Trade-off
analysis_layer: 目标层
judgment_basis:
  - "共享资源：注意力（order_summary 主任务路径）"
  - "C04 evaluation_goal=降低优惠查找成本；C05 evaluation_goal=保障结算连续性"
resolution_path: 条件化分层展示（默认折叠 + 有优惠需求用户可发现）
verification_status: 待核实
action: 转 QOC
```

## 防伪冲突四问（每条"冲突"必须回答）

① 两条意见是否指向同一设计对象或流程？② 是事实矛盾、策略互斥还是目标张力？③ 冲突在当前设计约束下是否真实存在？④ 能否通过重组界面同时满足两个目标？

两条意见兼容时，**不得为制造"多视角冲突"强行标注矛盾**。判例参照：`../knowledge/index.md` §3。
