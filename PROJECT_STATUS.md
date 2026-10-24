# 项目交接与工作区检查记录

主体为P0历史记录；2026-10-24后续硬件推进见第7节，当前交付索引见[项目README](README.md)。

- 检查日期：2026-10-24（Asia/Shanghai）
- 本次范围：熟悉既有设计，完成 P0，记录 P1–P4 的执行前提。
- 项目阶段：硬件与软件架构概念设计；尚未进入实物验证或生产交付。

## 1. P0 检查结果

### 检查前

- 当前桌面工作区为 `D:\dessktop_robot`。
- 目录为空，包含隐藏文件在内的项目数量为 0；不存在 `.git`。
- 因此检查前没有本地分支、remote、提交记录，也没有需要保护的未提交修改。
- 未假定此前的同步状态有效；通过 GitHub 连接读取仓库信息后，重新克隆已有远端仓库到当前空目录，没有新建另一套项目结构。

### 克隆后的基线（本次文档更新前）

| 项目 | 实际结果 |
|---|---|
| 仓库 | <https://github.com/huiershan/desktop_robot> |
| 本地目录 | `D:\dessktop_robot` |
| 分支 | `main`，跟踪 `origin/main` |
| origin（fetch / push） | `https://github.com/huiershan/desktop_robot.git` |
| HEAD 与 origin/main | `7dfeb9eb3e939d97c7aabfea9f85282654373f85` |
| 在线远端 HEAD | 同上；默认分支为 `main` |
| 基线提交时间 | 2026-10-22 13:42:52 +08:00 |
| 最新提交说明 | `docs: add software framework and system layers` |
| 本地领先 / 落后 | `0 / 0` |
| 相对 origin/main 的文件差异 | 无 |
| 已暂存、未暂存及未跟踪文件 | 无 |
| 适用的 AGENTS.md | 工作区及 `D:\AGENTS.md` 中未发现 |

最近提交：

| 提交 | 说明 |
|---|---|
| `7dfeb9e` | 软件框架与系统分层 |
| `64d241f` | 软件文档索引 |
| `9bae65d` | 硬件框架与 PCB 布局概念 |
| `5db9b8f` | 硬件文档索引 |
| `ff26a4e` | 项目概述 |
| `5ca4980` | 初始提交 |

以上记录是检查时的历史基线；本次文档提交的 ID 以 Git 提交记录和交付报告为准。

## 2. 实际文件与实现状态

基线共包含 6 个跟踪文件，已完整阅读其中 5 份 Markdown 文档：

| 文件 | 实际内容 |
|---|---|
| [README.md](README.md) | 项目概述、硬件规划、文档导航与安全提示 |
| [hardware/README.md](hardware/README.md) | 硬件设计原则与待建文档清单 |
| [hardware/HARDWARE_FRAMEWORK.md](hardware/HARDWARE_FRAMEWORK.md) | 机械分层、电源架构、功能分区及暂定接口 |
| [software/README.md](software/README.md) | 软件文档索引与开发原则 |
| [software/SOFTWARE_ARCHITECTURE.md](software/SOFTWARE_ARCHITECTURE.md) | 分层架构、状态机、调度、故障处理与测试规划 |
| [LICENSE](LICENSE) | 项目许可证 |

- 基线没有 `software/esp8266/`、`platformio.ini` 或固件源代码。
- 基线没有原理图、PCB、封装库、机械 CAD、Gerber、钻孔文件或实物测试记录。
- 底盘约 160 × 120 mm、主 PCB 约 110 × 80 mm 仍是摆放概念尺寸。
- 既有文档中的 GPIO 策略、I²C 地址示例、调度周期及电源举例不代表实物型号已经核实。

## 3. 后续必须延续的设计约束

1. 沿用 `hardware/` 与 `software/`，在现有文档基础上补齐设计。
2. 第一阶段保留 ESP8266 成品开发板，使用可拆卸连接方式接入主 PCB。
3. 先记录真实模块的尺寸、孔位和针序，再冻结板框、安装孔及连接器坐标。
4. OLED 面向机器人正面；同时核对窗口、固定、USB 插拔、线束、天线净空及螺丝避让。
5. 未核实的型号、尺寸、电气参数及连接器针序统一标记“待确认”。
6. 电机在启动、自检、复位和故障时保持安全停止；同时检查驱动器硬件默认状态。
7. 没有电池电压采样电路时，不提供电量或电压的虚假读数。
8. 编译通过、ERC/DRC 通过和实物验证分别记录，不相互替代。

## 4. P1 的实物信息缺口

下表来自交接要求及已有文档；本次未获得新的实物证据，以下各项均待确认。

| 对象 | 需要核实并记录的信息 |
|---|---|
| ESP8266 开发板 | 正反面照片、板型、尺寸、排针间距与针序、供电入口、启动绑带脚、USB 及天线位置 |
| 电池与充电器 | 化学体系、串数、满电电压、容量、BMS、充电规格、极性与连接器 |
| 电源转换模块 | 实际转换用途、型号、输入范围、输出电压、连续电流、散热与外形尺寸 |
| 双电机驱动板 | 芯片、VM 范围、逻辑电压、控制接口、连续/峰值电流、停止及使能状态 |
| 两个电机与车轮 | 额定电压、启动/堵转电流依据、减速比、轮径、轴及安装尺寸 |
| OLED | 控制器、分辨率、I²C/SPI、供电、上拉/逻辑电平、针序、尺寸、孔位与可视区域 |
| MPU6050 | 实物丝印是否为 MPU6050、模块型号、供电、上拉电压、地址、尺寸、固定及坐标方向 |
| DHT11 | 裸器件或模块、供电、数据上拉、针序与尺寸 |
| 红外模块 | 数量、用途、型号、数字/模拟输出、输出电平、尺寸与安装方向 |
| 线束与连接器 | 现有端子、针距、额定电流、防反插、配对端及逐针导通关系 |

每个模块的记录应附正反面照片、尺寸测量、准确型号对应的数据手册来源及测试条件。不能只依据购买标题或相似模块图片确定引脚与供电。

## 5. 分阶段交付顺序

| 阶段 | 下一步工作 | 可核验的完成条件 |
|---|---|---|
| P0 | 克隆与核对现有仓库；形成此次检查记录 | 本地与远端基线一致、已识别全部文件、差异检查通过 |
| P1 | 建立模块尺寸表、电气规格表及证据记录 | 关键型号、供电、尺寸、针序可追溯；缺项明确标记 |
| P2 | 补齐硬件连接、BOM、机械布局与检查清单 | 原理图网络、连接器线序、公共地回流与机械约束可互相核对 |
| P3 | 在 `software/esp8266/` 建立 PlatformIO + Arduino Core 工程 | 记录板型与依赖版本、真实构建结果；安全停止及故障路径有验证记录 |
| P4 | 完成正式 EDA、生产输出与实物测试 | 可编辑设计、ERC/DRC 报告、生产文件与逐阶段测试记录齐全 |

P2 对应文件继续放在 `hardware/`：`SCHEMATIC_NOTES.md`、`CONNECTOR_PINOUT.md`、`BOM.md`、`MECHANICAL_LAYOUT.md`、`PCB_CHECKLIST.md`。

P3 的 GPIO 配置集中在 `include/config/board_config.h`，参数集中在 `robot_config.h`，按 HAL、Drivers、Services、Application 分层。同步完善 `software/` 中的 GPIO、状态机、构建烧录、测试和变更文档。实物信息不足时可先建立可编译骨架，但不得将占位驱动、引脚或编译结果写成硬件验证通过。

正式生产设计依赖实物信息闭环；在此之前仅能输出标明用途和缺项的概念设计。上电验证遵循电源、显示与传感器、电机、整机的顺序。

## 6. 本机工具与本次验证范围

| 项目 | 本次检查结果 |
|---|---|
| Git | `2.41.0.windows.1`，成功克隆并读取远端 HEAD |
| PlatformIO | `pio`、`platformio` 未在当前 PATH 中找到 |
| KiCad CLI | `kicad-cli` 未在当前 PATH 中找到 |
| Python | PATH 解析到 WindowsApps 的 `python.exe`；未验证实际解释器是否可用 |
| GitHub CLI | `gh` 未在当前 PATH 中找到；GitHub 连接可读取仓库 |

“PATH 中未找到”不等于确认整台电脑没有安装；进入相应开发阶段时再核对实际安装位置及版本。

P0 已执行 `git status`、`git remote -v`、`git log`、`git ls-files`、`git rev-list --left-right --count HEAD...origin/main`、`git diff origin/main`、`git diff --check` 和 `git ls-remote --symref origin HEAD`，基线核对通过。

本次仅涉及交接与文档检查，没有固件构建、烧录、ERC/DRC 或实物上电结果。文档变更另行检查相对链接、空白错误及最终 Git 状态，并在提交后核验远端提交 ID。

## 7. 2026-10-24：器件资料与硬件规划推进

- 读取桌面清单的11个商品页面，保存17张关键图及来源/哈希；建立[模块尺寸表](hardware/MODULE_DIMENSIONS.md)与[来源索引](hardware/SOURCES.md)。
- 按新资料将首版候选改为受保护5V电源、6V N20和TB6612，补充光照、ToF与语音模块；旧12V方案不直接沿用。
- 用户确认两路是普通单颗指示LED，规划GPIO13/16各串联1kΩ。
- 提出新增SC16IS750，保留主控直接PWM与停止；形成[硬件连接](hardware/SCHEMATIC_NOTES.md)、[针序](hardware/CONNECTOR_PINOUT.md)、[BOM](hardware/BOM.md)、[机械布局](hardware/MECHANICAL_LAYOUT.md)及[放行清单](hardware/PCB_CHECKLIST.md)。
- 交付4张可编辑SVG及对应PNG、JSON配置和4份CSV，并检查证据、链接、GPIO/地址和区域一致性。
- **未完成**：关键实物几何/电源资格、正式EDA原理图与铜线、ERC/DRC、生产输出和固件工程。P1是部分闭环、P2是可审核概念规划，不标记为可生产设计。
