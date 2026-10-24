"""Validate planning consistency, not electrical correctness or ERC/DRC."""
import hashlib
import csv
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HW=ROOT/'hardware'
plan=json.loads((HW/'layout/plan.json').read_text(encoding='utf-8'))
errors=[]


def require(condition,message):
    if not condition: errors.append(message)


def overlaps(a,b):
    x,y,w,h=a;u,v,p,q=b
    return min(x+w,u+p)>max(x,u) and min(y+h,v+q)>max(y,v)


manifest=json.loads((HW/'evidence/manifest.json').read_text(encoding='utf-8'))
products=json.loads((HW/'evidence/product_links.json').read_text(encoding='utf-8'))
require(len(products)==11,'Expected 11 product references')
for item in manifest:
    path=ROOT/item['file']
    require(path.is_file(),f'Missing source {path}')
    if path.is_file():require(hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],f'Evidence changed: {path}')
    require(item['product_id'] in {p['id'] for p in products},'Unknown product in evidence')
for p in products:
    require(not any(token in p['url'] for token in ['mi_id=','spm=','boughtlist']),f'Tracking data in {p["id"]}')

gpio=plan['gpio'];signals={p['signal']:p['gpio'] for p in gpio}
require(len(gpio)==len({p['gpio'] for p in gpio}),'Duplicate controller GPIO assignment')
require(not any(6<=p['gpio']<=11 for p in gpio),'Flash GPIO allocated')
require(signals.get('LED1_GPIO')==13 and signals.get('LED2_GPIO')==16,'Independent LED reservation changed')
require(signals.get('MOTOR_ARM')==15,'Direct stop GPIO must be reviewed')
require(signals.get('DEBUG_TX')==1 and signals.get('DEBUG_RX')==3,'USB/debug UART must remain reserved')
require('SC16IS750' in plan['expansion'],'Bridge must include GPIO')
addresses=[a['address_7bit'] for a in plan['i2c']]
require(len(addresses)==len(set(addresses)),'I2C address conflict in proposed defaults')
require(all(0x08<=a<=0x77 for a in addresses),'Invalid seven-bit I2C address')
require(next(a['address_7bit'] for a in plan['i2c'] if a['name']=='VL53L0X')==0x29,'VL53L0X address must be seven-bit')

pcb=plan['pcb'];zones=pcb['zones']
for i,z in enumerate(zones):
    x,y,w,h=z['box']
    require(x>=0 and y>=0 and x+w<=pcb['width'] and y+h<=pcb['height'],f'Zone outside PCB: {z["id"]}')
    if z['id']!='U1':require(not overlaps(z['box'],pcb['rf_keepout']),f'Zone intrudes RF planning area: {z["id"]}')
    require(not overlaps(z['box'],pcb['usb_corridor']),f'Zone intrudes USB corridor: {z["id"]}')
    for other in zones[i+1:]:require(not overlaps(z['box'],other['box']),f'Zone overlap: {z["id"]}/{other["id"]}')
for c in pcb['connectors']:
    x,y=c['xy'];require(0<=x<=pcb['width'] and 0<=y<=pcb['height'],f'Connector point outside: {c["id"]}')
    rx,ry,rw,rh=pcb['rf_keepout'];require(not(rx<x<rx+rw and ry<y<ry+rh),f'Connector in RF area: {c["id"]}')
chassis=plan['chassis'];bx,by=chassis['pcb_origin'];rx,ry,rw,rh=pcb['rf_keepout']
require(not overlaps([bx+rx,by+ry,rw,rh],chassis['battery_reservation']),'Battery reservation intrudes RF projection')
require(not overlaps([bx+rx,by+ry,rw,rh],chassis['asr_reservation']),'ASR reservation intrudes RF projection')

nodes={}
for net in plan['nets']:
    require(len(net['nodes'])>=2,f'One-ended logical net: {net["net"]}')
    for pin in net['nodes']:
        require(pin not in nodes,f'Endpoint on two nets: {pin}')
        nodes[pin]=net['net']
require(nodes.get('U1.GPIO15')=='MOTOR_ARM','Missing direct arm output')
require(nodes.get('U4.STBY')=='MOTOR_STBY','Missing STBY network')
require(nodes.get('U1.GPIO13')=='LED1_GPIO' and nodes.get('J11.1')=='LED1_A','LED1 resistor chain incomplete')
require(nodes.get('U1.GPIO16')=='LED2_GPIO' and nodes.get('J12.1')=='LED2_A','LED2 resistor chain incomplete')
require(nodes.get('U2.TX')!='DEBUG_TX' and nodes.get('U2.RX')!='DEBUG_RX','ASR tied to debug UART')

expected_svgs={'pcb_partition','mechanical_layout','schematic_connections','routing_plan'}
require({p.stem for p in (HW/'diagrams').glob('*.svg')}==expected_svgs,'Missing or unexpected concept SVGs')
for svg in (HW/'diagrams').glob('*.svg'):
    ET.parse(svg)
    require('NOT FOR FABRICATION' in svg.read_text(encoding='utf-8'),f'Missing concept marking: {svg}')
with (HW/'layout/logical_nets.csv').open(encoding='utf-8-sig',newline='') as stream:
    rows=list(csv.DictReader(stream))
require([(r['net'],r['endpoint']) for r in rows]==[(n['net'],p) for n in plan['nets'] for p in n['nodes']],'Generated logical CSV is stale')
with (HW/'layout/gpio_plan.csv').open(encoding='utf-8-sig',newline='') as stream:
    rows=list(csv.DictReader(stream))
require([(int(r['gpio']),r['signal']) for r in rows]==[(p['gpio'],p['signal']) for p in gpio],'Generated GPIO CSV is stale')
for folder in [ROOT,HW,ROOT/'software']:
    for doc in folder.glob('*.md'):
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
            if re.match(r'\w+://|#',link):continue
            require((doc.parent/link.split('#')[0]).exists(),f'Broken link {doc.relative_to(ROOT)} -> {link}')
if errors:
    raise SystemExit('\n'.join(['Planning consistency FAILED:']+errors))
print(f'PASS: {len(manifest)} source hashes; 11 products; GPIO/address uniqueness; LED/stop logical paths; zone/keepout bounds; SVG/XML; Markdown links.')
print('LIMIT: no footprint geometry, ERC, DRC, trace-current, mechanical tolerance or hardware qualification was checked.')
