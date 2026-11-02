# Issue 评价记录模板（M2 输出契约）

> 完整字段定义与录入规范见 `../docs/01` §3–4；本文件是可直接填写的运行时模板

## 字段速览

| 字段 | 说明 |
|---|---|
| `issue_id` | 条目号 + 序号（如 C05-01） |
| `criterion` | 来源条目 id |
| `ui_anchor` | Frame + 区域 + 元素——**关系分析第一聚类键** |
| `observed_fact` | 可观察事实，标注 E1、注明是否已核实 |
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
ui_anchor: { frame: , region: , element: }
observed_fact:            # E1；注明是否已核实
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

- **未发现问题的条目输出 `judgment: 通过` + `evidence_basis`**，同样计入记录集——防止只报忧不报安
- 四步执行顺序：界面感知 → 任务推演 → 准则匹配 → 问题论证（详见 `../SKILL.md` M2）
- 各视角独立执行、相互隔离，评审期间不可看到彼此输出
