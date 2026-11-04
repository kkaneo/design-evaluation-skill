# 端到端演示：电商结算页评审（示例数据）

> 本文件演示一次完整评审（M0–M5）的输出形态。**所有界面细节与评审结论均为示意**，用于校准格式与流程，不是对任何真实产品的实际评价。

---

## M0 · 设计任务卡（摘要）

```yaml
design_task: 首次购物用户核对订单（含优惠）并完成支付
design_object:
  figma_link: <demo.figma>
  screenshots: [S1 订单确认页, S2 优惠券选择, S3 支付方式, S4 支付错误提示]
target_users: 首次购物用户（含部分仅持有微信支付额度的用户——示意）
primary_goals: 减少核对错误、提高结算效率
key_constraints:
  - 不可隐藏真实总价
  - 保留必要交易信息
expected_feedback: 任务效率、优惠理解、支付顺畅
out_of_scope: 品牌调性、营销文案风格
```

（Flow Spec 从略，结构见 `../templates/task-card.md` §2）

## M1 · 视角配置清单

**检索命中**（示意）：C01（主任务可发现性*）、C04（优惠入口可发现性*）、C05（优惠信息干扰）、C06（最终费用透明度*）、C11（状态一致性*）、C17（意外成本）、C20（选择负担）
> \* 标注条目暂无独立 YAML（待补全字段），本示例引用 `knowledge/index.md` 总览定义；正式评审优先启用有 YAML 的可执行条目

**按 evaluation_goal 聚类 → 4 个候选视角**：

| 候选视角 | 条目 | 评价目标 |
|---|---|---|
| 结算任务效率 | C01 C11 | 主任务连续、状态保持 |
| 优惠发现与理解 | C04 C05 | 有需求者找得到、无需求者不被扰 |
| 费用透明 | C06 C17 | 金额全程可核对、无惊吓披露 |
| 决策负担 | C20 | 默认适配、切换低成本 |

覆盖检查：任务目标已被现有条目覆盖 → 无新维度候选。
过滤：`品牌调性` 按 out_of_scope 过滤（未进入清单）。
**设计师确认：4 个视角全部保留。**

**可验证映射（M1 步骤 6 · 防"只改视角名"）**

| 任务目标 | 关键界面状态 | 检查条目 | 入选/排除理由 |
|---|---|---|---|
| 减少核对错误 | S1 订单确认（默认态） | C06 C17 C22 C25 | 金额核对依赖透明度与层级/分组 |
| 提高结算效率 | S3 支付方式、S4 错误态 | C20 C11 C29 | 默认适配、状态保持、浮层侵入 |
| 优惠理解 | S1→S2 入口与选择态 | C04 C05 | 可发现性 vs 干扰（经典张力） |
| 品牌调性 | — | — | **排除**：任务卡 out_of_scope |

> 验收方式：同一原型换任务卡（如「降低支付失败后的放弃」），上表的条目集合与关键状态应明显改变；若只换视角名称而检查内容不变，任务自适应未生效。

## M2 · Issue 记录（节选 3 条）

```yaml
issue_id: C04-01
criterion: C04
evaluation_goal: 降低优惠查找成本（入口可发现）
outcome: 发现问题
ui_anchor: { frame: order_summary, region: 金额明细下方, element: 优惠入口（折叠态） }
observed_fact: 优惠入口为弱化文字链，位于金额明细下方，首屏需向下滚动才可见（已核对截图 S1；获取方式：截图估读，未做 Figma 属性实测）
evidence_basis: Baymard Grocery Benchmark——"找优惠码"是测试中持续出现的问题；持有优惠码的用户总能找到入口，但弱入口增加查找成本
judgment: 持有优惠券的用户可能需要更长时间定位优惠入口（E2）
proposed_change: 提升优惠入口视觉层级，与金额明细同组呈现
applies_to: 持有优惠券 / 有优惠预期的用户
evidence_type: E2
verification_status: 待核实
validation_needs: [优惠发现率, 优惠入口查找时间]
```

```yaml
issue_id: C05-01
criterion: C05
evaluation_goal: 保障结算主任务连续性
outcome: 发现问题
ui_anchor: { frame: order_summary, region: 金额明细下方, element: 优惠码输入框 }
observed_fact: 优惠码输入框在默认视图中展开，位于金额明细与提交按钮之间（已核对截图 S1；获取方式：截图估读）
evidence_basis: Baymard Checkout Usability——显露的优惠码输入框可能促使部分用户暂停结算去寻找优惠码
judgment: 对无优惠需求的用户，可能增加主任务路径上的注意力消耗（E2）
proposed_change: 折叠优惠码输入框为弱化入口，保持可发现性（由 C04 独立评价）
applies_to: 无优惠需求的用户
evidence_type: E2
verification_status: 待核实（界面事实已核实；干扰效应未验证）
validation_needs: [无优惠需求用户结算完成时间, 优惠发现率]
```

```yaml
issue_id: C20-01
criterion: C20
evaluation_goal: 降低选择负担与切换成本
outcome: 发现问题
ui_anchor: { frame: payment, region: 支付方式列表, element: 默认推荐项与切换入口 }
observed_fact: 支付方式列表首位为支付宝并默认选中；其他方式需点击"更多支付方式"展开（已核对截图 S3；获取方式：截图估读，切换入口路径需当前版本复核）
evidence_basis: C20 real_world_cases——默认项与用户持有资源不匹配时，切换入口可达性决定实际负担（E1 界面事实 + E2 负担推断）
judgment: 默认支付方式与自身资源不匹配的用户可能需要额外操作完成支付，可能提高该人群的支付放弃风险（E2）
proposed_change: 支付方式列表同屏展示 2–3 个常用项 + 记住用户上次选择
applies_to: 默认支付方式与自身条件不匹配的用户
evidence_type: E2
verification_status: 待核实（切换入口路径需以当前版本复核）
validation_needs: [非默认支付方式用户完成率, 支付方式切换耗时, 切换后放弃率]
```

（其余视角的"通过"记录从略——未发现问题的条目同样输出"通过 + 依据"）

## M3 · 关系记录（节选 2 条）

```yaml
relation_id: REL-001
record_pair: [C04-01, C05-01]
context_alignment: 同页同状态（order_summary 默认态）；适用人群不同（持券 vs 无券）——对齐后确认张力仍在目标层
primary_relation: Trade-off
analysis_layer: 目标层
damage_mechanism: 强化入口（C04-01 建议）通过提升优惠区视觉层级挤占主任务路径注意力，损害 C05 的结算连续性目标
judgment_basis:
  - "共享资源：注意力（order_summary 主任务路径）"
  - "C04 evaluation_goal=降低优惠查找成本；C05 evaluation_goal=保障结算连续性"
resolution_path: 条件化分层展示（默认折叠入口 + 与金额同组、持券用户可发现）
verification_status: 待核实
action: 转 QOC
```

```yaml
relation_id: REL-002
record_pair: [C20-01, C11-01]
context_alignment: 跨页面关系（payment → order_summary 返回链）；C11-01 记录从略——S4→S1 走查推断"返回后优惠状态未保留"（示意，outcome: 证据不足）
task_step_id: payment.switch_method → order_summary.return
primary_relation: Dependency
analysis_layer: 策略层
judgment_basis:
  - "C20-01 proposed_change（同屏展示常用项）先行；C11-01 需验证切换 / 返回后订单与优惠状态是否保留"
  - "顺序颠倒会导致状态保持验证无从开展（切换路径尚未优化）"
resolution_path: 先落地同屏切换，再验证状态保持
verification_status: 待核实
action: 排序（写入 QOC 实施约束）
```

防伪冲突检查：C04-01 与 C05-01 观察事实不冲突（一个说入口弱、一个说输入框展开）——不构成 Contradiction，张力在目标层（注意力资源）→ Trade-off 成立。

## M4 · QOC（优惠入口问题，由 REL-001 转化）

**Question**：如何让有优惠需求的用户快速发现优惠，同时避免优惠输入打断其他用户的结算流程？

**Options**

| 方案 | 可能收益 | 风险与取舍 | 证据状态 | 尚未满足的约束 | 决策 |
|---|---|---|---|---|---|
| A 当前（弱折叠入口） | 无干扰 | 持券用户查找成本高（C04-01） | E2 待验证 | — | 保留作对照 |
| B 强化入口（默认展开） | 优惠发现可能提升 | 干扰主任务（C05-01）、增加页面长度 | E2 待验证 | 与任务效率目标冲突 | 待比较 |
| C 金额区整合弱入口（重构） | 有望兼顾两类目标 | 信息密度增加；入口醒目度仍可能不足 | 需原型验证 | 与"不可隐藏真实总价"约束兼容 | **推荐验证** |

**Criteria**：任务连续性 / 优惠发现率 / 金额理解 / 修改成本 / 必要交易信息完整

**优先级输出**

| 问题 | 级别 | 依据 |
|---|---|---|
| 优惠入口整合（方案 C） | P2 优先验证 | 可能兼顾双目标，但存在信息密度风险、证据不足 |
| 支付方式同屏切换（C20-01） | P1 优先修改 | 主任务明显影响、修改可行；与 C11 状态保持联合验证 |
| 方案 B | P3 延后 | 与任务效率目标直接冲突，暂不推进 |

初步决策：优先制作 C 的原型验证；A 保留为对照组；B 暂缓。（以上均为示意判断）

## M5 · 迭代记录（设计师回填，示意）

| 轮次 | 修改 | 关联 Issue / 关系 | 取舍理由（设计师回填） | 保留的待验证问题 |
|---|---|---|---|---|
| R1 | 优惠入口移入金额明细区、保持折叠 | C04-01、C05-01、REL-001 | 采纳方案 C：入口与金额建立信息关系，同时保持默认折叠（示意回填） | 持券用户发现率是否足够 |
| R2 | 支付方式同屏展示前 3 项 + 记住上次选择 | C20-01、REL-002 | 默认不适配人群切换成本下降；不调整默认优先级（业务约束，示意） | 非默认方式完成率、切换返回后状态保持 |

---

**本演示的用途**：① 校准 M1–M5 各环节的输出格式；② 作为 `../docs/01` §1 组装用例之外的补充验收材料（任务卡 → 视角配置 → Issue → 关系 → QOC 的完整链条）；③ 未来平台页面（P1–P4）的数据结构参考。
