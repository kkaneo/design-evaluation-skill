# Issue 评价记录模板（M2 输出契约）

> 完整字段定义与录入规范见 `../docs/01` §3–4；本文件是可直接填写的运行时模板

## 字段速览

| 字段 | 说明 |
|---|---|
| `issue_id` | 条目号 + 序号（如 C05-01） |
| `criterion` | 来源条目 id |
| `evaluation_goal` | 条目评价目标（M2 从条目 YAML 带入；M3 聚类回查用，不再读库） |
| `outcome` | **四态**：发现问题 / 已检查通过 / 证据不足 / 不适用 |
| `ui_anchor` | Frame + 区域 + 元素——**关系分析第一聚类键** |
| `observed_fact` | 可观察事实，标注 E1、是否已核实、获取方式（实测属性 / 截图估读） |
| `evidence_basis` | 引用条目来源的具体主张 |
| `judgment` | 问题判断，按 E 级动词规范措辞 |
| `proposed_change` | 修改建议 |
| `applies_to` | 适用条件（用户状态 / 意图）——Conditional 判定依赖 |
| `evidence_type` | E1 / E2 / E3 |
| `verification_status` | 已核实 / 待核实 / 证据矛盾 / 无法判断 |
| `validation_needs` | 待验证指标（进入 E3 队列） |

## 模板

```yaml
issue_id: C__-__
criterion:
evaluation_goal:          # 从条目 YAML 带入（M3 聚类回查用）
outcome:                  # 发现问题 / 已检查通过 / 证据不足 / 不适用
ui_anchor: { frame: , region: , element: }
observed_fact:            # E1；注明是否已核实 + 获取方式（实测属性 / 截图估读）
evidence_basis:           # 引用条目来源的具体主张，禁止泛泛"可用性原则"
judgment:                 # E1:「未呈现/违反××」；E2:「可能增加××」；E3 未经实测禁止效果结论
proposed_change:
applies_to:               # 哪些用户状态/意图下成立
evidence_type:
verification_status:
validation_needs:
```

## 示例

```yaml
issue_id: C05-01
criterion: C05
ui_anchor: { frame: order_summary, region: 金额明细下方, element: 优惠码输入框 }
observed_fact: 优惠码输入框在默认视图中展开，位于金额明细与提交按钮之间（已核对截图 S1）
evidence_basis: Baymard Checkout Usability——显露的优惠码输入框可能促使部分用户暂停结算去寻找优惠码
judgment: 对无优惠需求的用户，可能增加主任务路径上的注意力消耗（E2）
proposed_change: 折叠优惠码输入框为弱化入口，保持可发现性（由 C04 独立评价）
applies_to: 无优惠需求的用户
evidence_type: E2
verification_status: 待核实（界面事实已核实；干扰效应未验证）
validation_needs: [无优惠需求用户结算完成时间, 优惠发现率]
```

## 规则提醒

- **四态结论**（2026-11-03 起）：每条目必为 发现问题 / 已检查通过 / 证据不足 / 不适用 之一。「已检查通过」须核查了相关界面状态且依据充分；看不到证据（缺状态截图、机检不可用）记「证据不足」，**禁止默认通过**——防止"缺证据 = 通过"的隐性乐观
- 历史证据（条目 `evidence_cases` 中的外部 A/B 案例）标注为历史依据；本方案的效果另行验证，不得混写
- 四步执行顺序：界面感知 → 任务推演 → 准则匹配 → 问题论证（详见 `../SKILL.md` M2）
- 各视角独立执行、相互隔离，评审期间不可看到彼此输出
