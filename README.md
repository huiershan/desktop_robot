# 桌面机器人（Desktop Robot）

基于 ESP8266 的模块化两轮桌面机器人项目。采用模块化硬件、定制 PCB 与分层软件设计，减少洞洞板复杂焊接，便于装配、调试和扩展。

## 当前进度

已完成工作区核对，并于 2026-10-24 读取清单中的 11 个商品页面，保存关键尺寸证据，建立硬件连接、GPIO 和机械/PCB 分区规划。两路普通单颗指示 LED 拟分配 GPIO13、GPIO16，各串联 1kΩ。部分关键尺寸与电气规格尚未闭环，目前没有固件工程或可生产 PCB 文件。

可先查看[PCB 分区图](hardware/diagrams/pcb_partition.png)、[机械布局图](hardware/diagrams/mechanical_layout.png)、[原理图连接规划](hardware/diagrams/schematic_connections.png)和[布线路径走廊图](hardware/diagrams/routing_plan.png)。这些图均为概念评审文件；尺寸证据及缺项见[模块核对表](hardware/MODULE_DIMENSIONS.md)。

## 当前规划的硬件
- ESP8266 NodeMCU V3 / CH340 成品开发板（实物几何待测）
- TB6612FNG 驱动板、6V N20 电机和 43mm 车轮
- 清单标为 3000mAh / 5V 的受保护输出电源（能力待核实）；早期 12V 方案暂不采用
- DHT11 温湿度传感器
- MPU6050 六轴传感器（请以实物丝印确认）
- GY-302 / BH1750 光照度模块
- GY-530 / VL53L0X 测距模块
- ASR02 语音主板及喇叭（整板尺寸、电平与供电待核实）
- 红外传感器（循迹/检测用途待确认）
- 新款四脚蓝色 0.96 英寸 OLED，商家标为 SSD1315
- 两路普通单颗指示 LED；拟新增 SC16IS750 以扩展语音 UART 与电机方向 GPIO

以上为规划清单，最终规格以实际模块型号、数据手册和测试结果为准。

## 文档导航
- [项目交接与工作区检查记录](PROJECT_STATUS.md)
- [硬件目录说明](hardware/README.md)
- [硬件框架与布局概念设计](hardware/HARDWARE_FRAMEWORK.md)
- [模块尺寸与版本核对](hardware/MODULE_DIMENSIONS.md)
- [硬件连接与供电规划](hardware/SCHEMATIC_NOTES.md)
- [连接器针序](hardware/CONNECTOR_PINOUT.md)
- [物料清单](hardware/BOM.md)
- [机械布局与设计候选坐标](hardware/MECHANICAL_LAYOUT.md)
- [PCB 放行检查清单](hardware/PCB_CHECKLIST.md)
- [GPIO 分配规划](software/PIN_MAPPING.md)
- [软件目录说明](software/README.md)
- [软件框架与系统分层设计](software/SOFTWARE_ARCHITECTURE.md)

## 开发顺序
1. 核对模块型号、尺寸、接口、供电范围和引脚顺序。
2. 确认电池串数、满电电压、电机堵转电流及驱动器额定值。
3. 完成底盘布局、系统框图、原理图与 PCB 分区。
4. 先验证电源，再逐个验证主控、OLED、传感器和电机。
5. 根据测试结果更新 BOM、PCB、接线图和固件。

## 安全提示
- ESP8266 GPIO 为 3.3V 逻辑，不能直接承受 5V 输入。
- 本版输入只规划为经确认的受保护 5V 输出，不能接入旧方案的 12V 或电池电芯原始端。
- 电机启动/堵转电流影响驱动器、线宽、连接器和保险丝选型。
- 首次上电先断开电机，确认电源极性与电压后再逐步接入负载。
