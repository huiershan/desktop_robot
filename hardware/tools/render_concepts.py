"""Generate editable planning SVG/CSV files; these are not EDA fabrication files."""
import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HW = ROOT / 'hardware'
PLAN = json.loads((HW / 'layout/plan.json').read_text(encoding='utf-8'))
OUT = HW / 'diagrams'
OUT.mkdir(exist_ok=True)
INK, MUTED, BLUE, RED, ORANGE = '#17324d', '#52687b', '#236bb2', '#c6423c', '#b86c16'
COLORS = {'controller':'#dbeafe','logic':'#d7f0e5','sensor':'#e4f3db','power':'#fff0cd','motor':'#fce0db'}


class SVG:
    def __init__(self, width, height, title, subtitle):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                      '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC","Segoe UI",sans-serif}</style>',
                      f'<rect width="{width}" height="{height}" fill="#f5f8fc"/>']
        self.text(40, 48, title, size=26, weight=700)
        self.text(40, 77, subtitle, size=14, color=MUTED)
        self.rect(40, 96, width-80, 36, '#fff0d9', '#e4c394', radius=6)
        self.text(55, 120, '概念规划 / NOT FOR FABRICATION — 封装、孔位与电源资格尚未闭环', size=15, color=ORANGE, weight=600)

    def text(self, x, y, value, size=14, color=INK, weight=400, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{html.escape(str(value))}</text>')

    def lines(self, x, y, lines, step=23, **kwargs):
        for i, line in enumerate(lines):
            self.text(x, y+i*step, line, **kwargs)

    def rect(self, x, y, w, h, fill='white', stroke='#b8c8d8', dash=False, radius=4):
        d = ' stroke-dasharray="7 5"' if dash else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{d}/>')

    def circle(self, x, y, r, fill='white', stroke=INK):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

    def path(self, points, color=BLUE, width=2, dash=False):
        p = ' '.join(f'{x},{y}' for x,y in points)
        d = ' stroke-dasharray="7 5"' if dash else ''
        self.parts.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"{d}/>')

    def block(self, x,y,w,h,title,lines=(),fill='white'):
        self.rect(x,y,w,h,fill)
        self.text(x+14,y+27,title,size=16,weight=600)
        self.lines(x+14,y+51,lines,size=13,step=22,color=MUTED)

    def save(self, name):
        (OUT / name).write_text('\n'.join(self.parts+['</svg>'])+'\n',encoding='utf-8')


def pcb_base(title):
    s=SVG(1400,1120,title,'concept-0.2 · mm · 顶视：前方 ↑ / USB 朝后 · J 表示连接器编号，功能见标注与下方速查')
    ox,oy,k=90,205,6
    def xy(x,y): return ox+x*k,oy+y*k
    s.rect(ox,oy,110*k,80*k,'#fff',INK,radius=0)
    for x in range(10,110,10): s.path([xy(x,0),xy(x,80)],'#e8eef5',1)
    for y in range(10,80,10): s.path([xy(0,y),xy(110,y)],'#e8eef5',1)
    s.text(ox,oy-22,'X=0, Y=0',size=12,color=MUTED)
    s.text(ox+330,oy-50,'主 PCB 候选 110 × 80',size=17,weight=600,anchor='middle')
    for i,(x,y,d) in enumerate(PLAN['pcb']['holes'],1):
        s.circle(*xy(x,y),d*k/2,fill='#f5f8fc')
        s.text(*xy(x+3,y+1),f'H{i}',size=10)
    for zone in PLAN['pcb']['zones']:
        x,y,w,h=zone['box'];px,py=xy(x,y)
        s.rect(px,py,w*k,h*k,COLORS[zone['type']],dash=True)
        if zone['id']!='U1': s.text(px+9,py+22,zone['id'],size=16,weight=700)
        label = zone['label']
        if zone['id']=='U1':
            pass  # Draw below the RF overlay so the module identity remains visible.
        elif zone['id']=='U2': s.lines(px+9,py+46,['UART / GPIO','含晶振与去耦'],size=12,step=22)
        elif zone['id']=='U3': s.lines(px+9,py+46,['GY-521','实际外形21×16','孔位待测'],size=12,step=21)
        elif zone['id']=='PWR': s.lines(px+9,py+46,['5V 输入保护','保险 / 回流'],size=12,step=23)
        else: s.lines(px+9,py+48,['TB6612 模块','排针 / 温升待测'],size=12,step=24)
    x,y,w,h=PLAN['pcb']['rf_keepout'];px,py=xy(x,y)
    s.rect(px,py,w*k,h*k,'#fff4df',ORANGE,dash=True)
    s.lines(px+10,py+32,['天线与金属避让','规划区 40 × 20','最终按实际天线修订'],size=12,step=23,color=ORANGE)
    px,py=xy(12,0)
    s.text(px+10,py+163,'U1 NodeMCU',size=17,weight=700)
    s.lines(px+10,py+196,['成品开发板 / 可拆卸','区域 34 × 66','真实尺寸与插座待测'],step=28,size=13)
    x,y,w,h=PLAN['pcb']['usb_corridor'];px,py=xy(x,y)
    s.rect(px,py,w*k,h*k,'#edf2f7',MUTED,dash=True)
    s.lines(px+9,py+30,['USB 插拔走廊 → 后方开口','主控 USB 位置待量'],size=12,step=23)
    for connector in PLAN['pcb']['connectors']:
        x,y=connector['xy'];px,py=xy(x,y)
        s.rect(px-5,py-5,10,10,'#17324d','#17324d',radius=1)
        label=f'{connector["id"]} {connector["short_label"]}'
        if x<10:
            s.path([(ox-5,py),(px-6,py)],MUTED,1)
            s.text(ox-10,py+4,label,size=12,anchor='end')
        elif x>100:
            s.path([(px+6,py),(ox+110*k+9,py)],MUTED,1)
            s.text(ox+110*k+15,py+4,label,size=12)
        elif y<10:
            s.path([(px,py-6),(px,oy-5)],MUTED,1)
            s.text(px,oy-12,label,size=12,anchor='middle')
        else:
            s.path([(px,py+6),(px,oy+80*k+7)],MUTED,1)
            s.text(px,oy+80*k+22,label,size=12,anchor='middle')
    s.text(ox+330,oy+80*k+55,'参考点与区域坐标：layout/plan.json / connector_positions.csv',size=13,color=MUTED,anchor='middle')
    return s,xy


def connector_legend(s):
    s.rect(70,815,1260,245,'white')
    s.text(90,845,'J 编号功能速查（不是 GPIO 编号；针序详见 CONNECTOR_PINOUT.md）',size=18,weight=600)
    connectors=PLAN['pcb']['connectors']+PLAN['pcb'].get('unplaced_connectors',[])
    connectors=sorted(connectors,key=lambda c:int(''.join(ch for ch in c['id'].split('/')[0] if ch.isdigit())))
    for index,c in enumerate(connectors):
        column,row=divmod(index,6)
        s.text(90+column*415,880+row*29,f'{c["id"]}  {c["purpose_zh"]}',size=14)
    s.text(70,1090,'J4A/J4B、J10、J16、J17 尚未确定板上坐标，仅在速查表说明用途；其他标记仍是候选参考点。',size=13,color=MUTED)


def draw_pcb():
    s,xy=pcb_base('主 PCB 功能分区与接口候选位置')
    s.lines(950,195,['布局约束'],size=20,weight=700)
    s.lines(950,234,['1. 成品开发板可拆卸，天线靠前缘。','2. 射频区避免铜、走线、螺丝和电池。','3. MPU 平整固定并记录机器人轴向。','4. 入口保护与驱动靠近后方功率出口。','5. DHT、光照、OLED、ToF 由线束外置。','6. ASR 整板位于上层，串口经 U2。'],size=14,step=32)
    s.rect(940,450,410,192,'white')
    s.lines(960,478,['两路普通单颗 LED','GPIO13 → 1kΩ → J11 → LED1','GPIO16 → 1kΩ → J12 → LED2','两路独立；阴极均接 GND','未分配至启动绑带或电机停止信号'],size=14,step=30)
    s.lines(80,766,['孔与连接器仍为候选：必须使用真实封装复核螺丝头、锁扣、插头与 Z 向空间。'],size=14,color=ORANGE)
    connector_legend(s)
    s.save('pcb_partition.svg')


def draw_routing():
    s,xy=pcb_base('电源与信号布线路径走廊')
    # Paths intentionally show corridors, never actual copper widths or layers.
    for p in [[(60,77),(60,69),(70,62),(80,62),(92,62)],[(70,62),(50,62),(46,60)],[(70,62),(77,62),(77,27),(107,27)]]:
        s.path([xy(*v) for v in p],RED,4)
    for p in [[(46,32),(50,32),(76,32),(76,6),(98,6)],[(55,6),(55,3)],[(69,6),(69,3)],[(83,6),(83,3)],[(98,6),(98,3)],[(63,32),(63,26)],[(63,32),(63,38)]]:
        s.path([xy(*v) for v in p],BLUE,3)
    s.path([xy(46,53),xy(78,46),xy(92,49)],'#8054b3',3,dash=True)
    s.path([xy(75,20),xy(103,20),xy(107,27)],'#008a7c',3,dash=True)
    s.lines(950,195,['路径定义'],size=20,weight=700)
    for y,color,title,body in [(245,RED,'红：5V 功率支路','入口保护后分支，VM 回流就近回入口'),(345,BLUE,'蓝：共享 I²C','主控侧3.3V上拉，短支线与连续地参考'),(445,'#8054b3','紫：PWM / STBY','主控直接到驱动，停止不经过 U2'),(545,'#008a7c','绿：语音 UART','U2 到 ASR；电平适配后才接通')]:
        s.path([(955,y),(1000,y)],color,4)
        s.text(1015,y+5,title,size=15,weight=600)
        s.text(955,y+35,body,size=13,color=MUTED)
    s.lines(80,759,['示意路径可能交叉；没有定义铜层、焊盘、过孔或实际铜宽。GND 尽量连续，避免信号跨地缝。','电机启动/堵转与回灌数据未闭环，电源额定值及走线计算尚未放行。'],size=14,step=24,color=ORANGE)
    connector_legend(s)
    s.save('routing_plan.svg')


def draw_mechanical():
    s=SVG(1250,920,'底盘、传感器与前面板布局规划','concept-0.2 · 俯视 / 前视 · 已核对尺寸与规划空间分别标注')
    c=PLAN['chassis'];ox,oy,k=140,215,3
    def xy(x,y):return ox+x*k,oy+y*k
    s.text(ox+180,180,'俯视：底盘候选 120 × 160',size=18,weight=600,anchor='middle')
    s.rect(ox,oy,360,480,'white',INK,radius=10)
    for x in [-18,120]:
        px,py=xy(x,c['axle_y']-21.5);s.rect(px,py,18*k,43*k,'#586778',INK,radius=8)
    s.path([xy(0,c['axle_y']),xy(120,c['axle_y'])],MUTED,1,dash=True)
    for x in [0,90]:
        px,py=xy(x,c['axle_y']-6);s.rect(px,py,30*k,12*k,'#ffe8cf',ORANGE,dash=True)
    px,py=xy(*c['pcb_origin']);s.rect(px,py,110*k,80*k,'#e7effb',BLUE,dash=True)
    s.text(px+12,py+28,'主 PCB 110 × 80 / 电子层',size=14,weight=600)
    x,y,w,h=c['battery_reservation'];px,py=xy(x,y);s.rect(px,py,w*k,h*k,'#eee3f4','#8865a1',dash=True)
    s.lines(px+8,py+29,['电池预留','50 × 70','不是实物尺寸','底层两电机之间'],size=12,step=25)
    s.text(565,oy+c['axle_y']*k,'轮轴 Y=125',size=12,color=MUTED)
    cx,cy=xy(*c['caster_center']);s.circle(cx,cy,25*k,'#f1f4f7',MUTED)
    s.circle(cx,cy,8*k,'#d9e0e8',MUTED)
    s.text(cx,cy-36,'钢珠轮：底板避让区50',size=12,anchor='middle')
    s.text(cx,cy+53,'高21 / 孔距40 / 孔径4',size=11,anchor='middle')
    for x in [15,105]:
        px,py=xy(x,8);s.rect(px-14,py-8,28,16,'#dcefd8','#5d8d46',dash=True)
    s.text(ox+180,oy-9,'前向 ↑ / 下视红外待选',size=12,anchor='middle',color=MUTED)
    s.lines(85,760,['43 mm 轮径 / 18 mm 轮宽：商家标注。','电机、线束和电池在不同层，需实物检查三维干涉。','钢珠轮垫高量 = 21.5 + 轴心低于底板的距离 − 21。'],size=14,step=28)
    # Front view: Z is shown vertically upward from a conceptual ground datum.
    fx,fy=740,520
    def front(x,z):return fx+x*3,fy-z*3
    s.text(fx+180,180,'前视：显示与感知开口候选',size=18,weight=600,anchor='middle')
    s.rect(fx,fy-300,360,300,'white',INK,dash=True)
    px,py=front(47.5,83.5);s.rect(px,py,25*3,27*3,'#dbeafe',BLUE)
    s.text(px+37.5,py+43,'OLED',size=12,anchor='middle')
    for x in [50,70]:
        for z in [58.5,81.5]:s.circle(*front(x,z),4.5,'white',BLUE)
    s.text(fx+180,fy-270,'25 × 27 / 孔距20 × 23 / Ø3',size=12,anchor='middle')
    x,z,w,h=c['tof_front_reservation'];px,py=front(x,z+h);s.rect(px,py,w*3,h*3,'#fff0d9',ORANGE,dash=True)
    s.text(px+w*1.5,py+23,'ToF 预留40 × 20',size=12,anchor='middle')
    s.text(px+w*1.5,py+44,'实际孔位待复核',size=11,anchor='middle')
    for x in [30,90]:
        cx,cy=front(x,70);s.circle(cx,cy,7,'#f4bf62',ORANGE)
    s.text(fx+180,fy+28,'两颗普通指示 LED，分别接 J11 / J12',size=13,anchor='middle')
    s.rect(700,590,500,230,'white')
    s.lines(720,622,['外置模块位置原则','DHT：左前通风，避开稳压、驱动和热源。','BH1750：顶部采光，避开 OLED / LED 自照。','ASR02：上层预留40 × 50，整板 / 喇叭待量。','主控天线投影下不放电池、金属及扬声器磁体。','OLED 视窗偏移与透镜中心未测，禁止直接加工。'],size=14,step=31)
    s.lines(60,875,['主 PCB、底盘、层高与模块预留区都是候选设计；不是加工尺寸图，也没有定义装配公差。'],size=14,color=ORANGE)
    s.save('mechanical_layout.svg')


def draw_schematic():
    s=SVG(1330,1220,'系统原理图连接规划与安全停止路径','concept-0.2 · 逻辑网络名有效，模块排针物理脚号与器件外围尚未补齐')
    # Power path.
    s.block(50,165,200,95,'J1 受保护 5V 输入',['极性 / 输出电流待确认'])
    s.block(300,165,245,95,'F1 → SW1 → 输入保护',['额定值、压降与温升待核'],fill='#fff0cd')
    s.block(600,165,250,95,'5V_PROT 分配点',['VM / 主控 / 语音三支路'],fill='#fff0cd')
    s.path([(250,210),(300,210)],RED,3);s.path([(545,210),(600,210)],RED,3)
    s.block(930,165,340,95,'VM 滤波 / 回灌 / 储能',['5V_VM → TB6612 VM，钳位待设计'],fill='#fce0db')
    s.path([(850,210),(930,210)],RED,3)
    # Main blocks.
    s.block(50,340,330,200,'U1 NodeMCU 成品开发板',['VIN 经 JP_USB_SAFE 接 5V','3V3_LOGIC 取板载稳压：余量待验证','GPIO4/5：I²C SDA / SCL','GPIO1/3：保留 USB 下载与日志','GPIO0：保留 FLASH / 启动'],fill='#dbeafe')
    s.path([(725,260),(725,300),(215,300),(215,340)],RED,3)
    s.text(260,290,'JP_USB_SAFE：USB 供电隔离待验证',size=12,color=RED)
    s.block(490,340,350,200,'U2 SC16IS750（拟新增）',['3.3V / I²C 七位地址0x48','GPIO0..3 → AIN1/2、BIN1/2','UART → 电平适配 → ASR02','GPIO4 → 开漏级 → ToF XSHUT','GPIO5/6 → 数字红外适配后输入'],fill='#d7f0e5')
    s.path([(380,400),(490,400)],BLUE,3);s.text(393,386,'SDA / SCL',size=12,color=BLUE)
    s.path([(50,445),(28,445),(28,705),(100,705)],BLUE,3)
    s.block(930,340,340,200,'U4 TB6612 成品模块',['VCC=3.3V / VM=5V 分开','PWMA=GPIO12 / PWMB=GPIO14','AIN1/2、BIN1/2 来自 U2','STBY 由 GPIO15 独立允许','AO1/2 → 左电机；BO1/2 → 右电机'],fill='#fce0db')
    s.path([(1100,260),(1100,340)],RED,3)
    s.path([(840,410),(930,410)],'#7c59a4',2);s.text(850,397,'方向',size=12,color='#7c59a4')
    # Direct stop path highlighted; deliberately bypasses U2.
    s.rect(50,590,1220,88,'#fff0d9','#e0b16d')
    s.text(68,618,'直接安全路径：GPIO15 → R_ARM 1k → SW_MOTOR → STBY；驱动侧 R_STBY 10k 下拉',size=16,weight=600,color=ORANGE)
    s.text(68,649,'SW_MOTOR 断开或主控 GPIO15 为低时禁止运动。故障先清 STBY / PWM，再做日志和 I²C 恢复。',size=14,color=ORANGE)
    s.path([(215,540),(215,568),(1100,568),(1100,540)],'#8054b3',3)
    s.text(550,559,'直接 PWM / STBY（不经过 I²C 桥）',size=13,color='#8054b3')
    # Peripheral row.
    for x,title,lines in [(50,'J5 OLED',['SSD1315 新款','GND / VDD / SCL / SDA']),(360,'J6 GY-521 + J13 BH1750',['共用3.3V侧 I²C','供电、上拉与地址待实测']),(670,'J15 GY-530',['Wire 地址0x29','GPIO1不接 / XSHUT开漏']),(980,'J14 ASR02',['独立5V支路','UART TX/RX交叉且适配'])]:
        s.block(x,730,290,120,title,lines,fill='#eef4fb')
    s.path([(100,705),(950,705)],BLUE,3)
    for x in [195,505,815]:s.path([(x,705),(x,730)],BLUE,2)
    s.path([(840,495),(875,495),(875,560),(1290,560),(1290,712),(1125,712),(1125,730)],'#008a7c',2,dash=True)
    s.text(60,700,'共享 I²C（所有主控侧上拉仅接3.3V）',size=12,color=BLUE)
    # LED resistor chains and DHT.
    s.block(50,910,590,170,'两路普通单颗指示 LED',['GPIO13 → R_LED1 1kΩ → J11.1 → LED1 阳极；阴极 → J11.2 / GND','GPIO16 → R_LED2 1kΩ → J12.1 → LED2 阳极；阴极 → J12.2 / GND','测试点在电阻前；两路独立，本版不用于灯带或照明'],fill='#fff5dc')
    s.block(690,910,580,170,'J7 DHT11 / 红外 / 地参考',['GPIO2 → DHT DATA，3.3V 上拉；启动绑带兼容性待实测','J8/J9 红外型号 / 电压未确认，适配和供电选择暂不装','所有 GND 同网；功率回流不经过传感器地细颈','无电池采样网络，不产生虚假电量读数'],fill='#e9f2e6')
    s.lines(50,1135,['未画出全部复位、晶振、去耦、未用脚、接口保护与连接器物理脚号。逻辑网见 layout/logical_nets.csv。','此图用于连接评审；正式 EDA 原理图、ERC、PCB 铜线与 DRC 均尚未完成。'],step=27,size=14,color=ORANGE)
    s.save('schematic_connections.svg')


def export_tables():
    def write_csv(name, header, rows):
        with (HW/'layout'/name).open('w',newline='',encoding='utf-8-sig') as stream:
            writer=csv.writer(stream);writer.writerow(header);writer.writerows(rows)
    write_csv('logical_nets.csv',['net','endpoint','pin_number_status'],[(n['net'],p,'logical_name_only') for n in PLAN['nets'] for p in n['nodes']])
    write_csv('placement_zones.csv',['id','name','x_mm','y_mm','width_mm','height_mm','status'],[(z['id'],z['label'],*z['box'],'PLANNING_RESERVATION_NOT_FOOTPRINT') for z in PLAN['pcb']['zones']])
    write_csv('connector_positions.csv',['id','name','purpose_zh','x_mm','y_mm','status'],[(c['id'],c['name'],c['purpose_zh'],*c['xy'],'REFERENCE_POINT_NOT_PAD_CENTER') for c in PLAN['pcb']['connectors']])
    write_csv('gpio_plan.csv',['gpio','board_label_pending','signal','purpose'],[(g['gpio'],g['board_label'],g['signal'],g['purpose']) for g in PLAN['gpio']])


if __name__=='__main__':
    draw_pcb();draw_routing();draw_mechanical();draw_schematic();export_tables()
    print('Generated 4 editable concept SVGs and 4 planning CSVs. No EDA manufacturing output generated.')
