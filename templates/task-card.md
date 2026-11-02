# 设计任务卡与流程说明模板（P0 输入契约）v0.1

> 用途：定义设计师提交给 Skill 的标准化输入。任务卡约束评审范围，流程说明支撑动态评审（认知走查）
> 状态：字段结构已确认（2026-11-03），与设计师实际提供的输入习惯对齐

---

## 1. 设计任务卡

```yaml
design_task: 首次购物用户核对订单并完成支付        # 用户要完成什么
design_object:                                     # 评审对象
  figma_link: <Figma 文件链接>
  screenshots: [订单确认页, 优惠券选择状态, 支付方式选择, 错误提示状态]
target_users: 首次购物用户
primary_goals: 减少错误、提高核对效率               # 主要目标（期待改善什么）
key_constraints:                                   # 关键约束（不可违反的底线）
  - 不可隐藏真实总价
  - 保留必要交易信息
expected_feedback: 任务效率、优惠理解               # 期待反馈（希望聚焦的方向）
out_of_scope: 品牌调性、营销文案风格               # 暂不评审（直接过滤无关视角）
existing_evidence:                                 # 可选：已有证据
  - 暂无 / 或：既有用户测试、业务数据、既往评审记录
```

**这张卡驱动整个 Skill**：视角检索用 `design_task` + `target_users` 匹配条目的 `applicable_context`；`out_of_scope` 直接过滤无关维度（如品牌调性）；`key_constraints` 进入 QOC 的约束列；`expected_feedback` 影响优先级判断（第 2 条"核心任务优先"）。

## 2. 流程说明（Flow Spec）

**为什么需要**：静态截图只能支撑页面级评审；C10（错误恢复）、C11（状态一致性）等条目需要流程信息。Figma 原型的交互连线无法被 AI 直接可靠读取（REST API 的 `interactions` 字段有数据缺失报告），**用一页说明替代导出**——这正是"不需要导出"的可行方案。

### 2.1 Frames 清单

| Frame 名 | 用途 / 状态 | 截图编号 | 备注（滚动 / 弹层） |
|---|---|---|---|
| order_summary | 订单确认（默认） | S1 | 优惠入口在金额明细下方 |
| coupon_selection | 优惠券选择 | S2 | 弹层 |
| payment | 支付方式确认 | S3 | 底部固定提交按钮 |
| payment_error | 支付错误提示 | S4 | — |

### 2.2 关键交互

| 出发 Frame | 触发元素 | 触发方式 | 到达 Frame | 变量 / 状态变化 |
|---|---|---|---|---|
| order_summary | 优惠入口 | 点击 | coupon_selection | 打开优惠券列表 |
| coupon_selection | 应用某券 | 点击 | order_summary | total_amount 更新，入口显示已选券 |
| payment | 提交按钮 | 点击 | payment_error / 成功页 | 视支付校验结果分支 |

### 2.3 变量

| 变量名 | 类型 | 初始值 | 使用于 | 说明 |
|---|---|---|---|---|
| total_amount | number | 128.00 | order_summary, payment | 优惠应用后更新 |
| coupon_applied | boolean | false | order_summary | 控制优惠状态展示 |

### 2.4 分支与异常状态

- 正常路径：order_summary → coupon_selection（可选）→ payment → 成功
- 异常路径：payment → payment_error → 返回 payment 重新选择

### 2.5 已知断点

原型未覆盖、评审时需标记"待验证"的点：

- 真实支付失败后的重试逻辑未模拟（E2 判断，待 E3）
- 优惠券过期 / 不可用的状态未设计

## 3. 填写成本与演进路径

- **手工填写 10–15 分钟**，一次填写全程复用；AI 走查的输入 = 截图 + 本说明，评审质量不依赖导出
- **未来自动化**（不急）：小型 Figma 插件读取 `node.reactions` 遍历节点树，导出与本模板同结构的 JSON（插件 API 完整支持条件分支与变量；REST 的 `interactions` 字段不要依赖）
- **行为数据**（Study C 用）：Figma 原型接入 Maze 等测试平台采集，与本模板无关——原型本身不需要为记录数据做任何改动
