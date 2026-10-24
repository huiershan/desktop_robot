# 硬件设计目录

本目录保存桌面机器人的硬件框架、机械布局、电源架构、接口规划和 PCB 设计约束。

## 文档
- [硬件框架与布局概念设计](HARDWARE_FRAMEWORK.md)
- [模块尺寸与规格核对表](MODULE_DIMENSIONS.md)
- [商品链接、原厂资料与尺寸图证据](SOURCES.md)
- [原理图连接与供电网络](SCHEMATIC_NOTES.md)
- [连接器针脚与线序](CONNECTOR_PINOUT.md)
- [BOM 与拟新增器件](BOM.md)
- [机械布局与 PCB 分区](MECHANICAL_LAYOUT.md)
- [PCB 与首板放行清单](PCB_CHECKLIST.md)
- [硬件变更记录](CHANGELOG.md)

2026-10-24 已读取桌面清单的 11 个商品页面，并保存匹配尺寸图与版本冲突证据。OLED、GY-521、DHT11、BH1750、车轮和钢珠轮已有部分商家标注；ESP8266 排针几何、5V 电源、ASR02 整板、6V 电机及 GY-530 孔位等缺项仍未闭环，不能据此生产 PCB。

## 规划图与数据

- [PCB 分区 SVG](diagrams/pcb_partition.svg) / [PNG](diagrams/pcb_partition.png)
- [机械布局 SVG](diagrams/mechanical_layout.svg) / [PNG](diagrams/mechanical_layout.png)
- [连接规划 SVG](diagrams/schematic_connections.svg) / [PNG](diagrams/schematic_connections.png)
- [布线路径走廊 SVG](diagrams/routing_plan.svg) / [PNG](diagrams/routing_plan.png)
- [单一配置源](layout/plan.json)、[逻辑网络 CSV](layout/logical_nets.csv)、[区域 CSV](layout/placement_zones.csv)、[接口参考点 CSV](layout/connector_positions.csv)、[GPIO CSV](layout/gpio_plan.csv)

这些文件可编辑、可复核，但不包含已验证封装或真实 PCB 铜线。SVG 走线粗细不代表铜宽。

## 重新生成与检查

```text
python hardware/tools/render_concepts.py
python hardware/tools/check_design.py
```

第一条用 Python 标准库重新生成 SVG/CSV，第二条检查证据哈希、相对链接、GPIO/地址、逻辑网及区域一致性。PNG 是从对应 SVG 用 sharp 渲染的预览；更新 SVG 后可用支持 SVG 的渲染器重新导出。检查不等于 ERC/DRC 或硬件认证。

## 后续工作

- 关闭尺寸/电气缺项，选定真实连接器、封装与保护器件。
- 在 EDA 中绘制完整原理图、布局布线并保存 ERC/DRC 报告。
- 增加 test/ 下的电源、传感器、电机与整机实测记录。

## 设计原则
1. 未确认的尺寸、引脚和电气参数必须标记为待确认。
2. 每个模块记录准确型号、供电范围、逻辑电平、峰值电流和连接器针脚。
3. 原理图完成 ERC，PCB 完成 DRC 后再输出生产文件。
4. 电源/电机功率路径与敏感信号路径分区布线。
5. 接口丝印必须标明信号名、供电电压、极性和 1 脚方向。

> 当前为概念设计阶段，不应直接据此生产 PCB；必须先核对实物和数据手册。
