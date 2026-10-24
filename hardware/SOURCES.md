# 器件资料来源与证据

核对日期：2026-10-24。桌面清单是所购规格描述的来源；商品页及图片是商家声明，不等于实测。首条重复拼接的 URL 已去重；仅保留 item ID / SKU ID，未保存购买记录或账户信息。

## 商品链接

| ID | 清单规格 | 商品详情 |
|---|---|---|
| P01 | 新款四脚蓝色 OLED，已焊针 | [558395483864 / SKU 6018269419830](https://detail.tmall.com/item.htm?id=558395483864&skuId=6018269419830) |
| P02 | TB6612FNG，已焊针 | [41248562401 / SKU 5049592548086](https://detail.tmall.com/item.htm?id=41248562401&skuId=5049592548086) |
| P03 | 原装 GY-521，直针向下 | [41337720621 / SKU 5050248973051](https://detail.tmall.com/item.htm?id=41337720621&skuId=5050248973051) |
| P04 | DHT11 | [524011396641](https://detail.tmall.com/item.htm?id=524011396641) |
| P05 | GY-302 / BH1750 光照度 | [41286408463](https://detail.tmall.com/item.htm?id=41286408463) |
| P06 | ESP8266，NodeMCU V3 / CH340 商品 | [609017742477 / SKU 4527105763291](https://item.taobao.com/item.htm?id=609017742477&skuId=4527105763291) |
| P07 | 小号钢珠轮单只 | [695759952754 / SKU 6038912268513](https://detail.tmall.com/item.htm?id=695759952754&skuId=6038912268513) |
| P08 | N20 座、43 mm 轮、6V 1000 转/10 mm 轴长电机 | [967344792284](https://detail.tmall.com/item.htm?id=967344792284) |
| P09 | 3000mAh 5V，Type-C 公母头 | [911754989740](https://detail.tmall.com/item.htm?id=911754989740) |
| P10 | ASR02 整板，内置下载器、USB 线和喇叭 | [736159554057](https://detail.tmall.com/item.htm?id=736159554057) |
| P11 | GY-530 双孔紫色，未焊 | [625713911541](https://detail.tmall.com/item.htm?id=625713911541) |

清单没有 SKU 的商品尚不能从购买标题反推出具体订单选项或数量。保留结构化引用：[product_links.json](evidence/product_links.json)。

## 图像证据

以下图像按读取时的资源原样保存，可能是 WebP 内容而沿用资源文件扩展名；检查工具按文件内容识别。用于复核尺寸和发现版本冲突，不属于本项目绘制的生产图。

| 文件 | 适用内容 |
|---|---|
| [oled-new-4pin.webp](evidence/oled-new-4pin.webp) | 新款蓝色四脚的尺寸、孔位、针序与控制器 |
| [tb6612-approximate-comparison.jpg](evidence/tb6612-approximate-comparison.jpg) | TB6612 的近似外形，不是插座图 |
| [mpu6050-original-outline.jpg](evidence/mpu6050-original-outline.jpg) | 原装 GY-521 的 21 × 16 外形与丝印 |
| [dht11-outline.jpg](evidence/dht11-outline.jpg)、[pin-labels](evidence/dht11-pin-labels.jpg) | DHT11 模块尺寸与接口说明 |
| [bh1750-dimensions.jpg](evidence/bh1750-dimensions.jpg)、[pin-labels](evidence/bh1750-pin-labels.webp) | GY-302 外形参数与针序 |
| [nodemcu-v3-product-photo.jpg](evidence/nodemcu-v3-product-photo.jpg)、[seller-pin-reference](evidence/nodemcu-seller-pin-reference.jpg) | 商品板型及卖家引脚参考；没有尺寸 |
| [caster-small-dimensions.jpg](evidence/caster-small-dimensions.jpg) | 小号和大号对照；本项目只使用小号行 |
| [wheel-and-motor-bracket.jpg](evidence/wheel-and-motor-bracket.jpg) | 43 mm 轮子及底座局部尺寸 |
| [motor-other-variant-not-applicable.jpg](evidence/motor-other-variant-not-applicable.jpg) | 不适用于所购 6V 版本的电机图，作为排除证据 |
| [battery-12v-table-not-applicable.jpg](evidence/battery-12v-table-not-applicable.jpg) | 12V 参数表，排除用于所购 5V 版本 |
| [asr-motherboard-reference.jpg](evidence/asr-motherboard-reference.jpg)、[core-not-motherboard](evidence/asr-core-not-motherboard.jpg) | 主板示意与小模块尺寸的区别；未证实整板尺寸 |
| [tof-outline-conflict.jpg](evidence/tof-outline-conflict.jpg)、[spec-and-pin-conflict](evidence/tof-spec-and-pin-conflict.jpg) | GY-530 尺寸解释、针序与地址位宽问题 |

每张图的原始 URL、关联商品和 SHA-256 在 [manifest.json](evidence/manifest.json) 中；不按相似商品图补齐缺项。

## 已核对的芯片原厂资料

- [Espressif ESP8266EX 资源与启动说明](https://www.espressif.com/en/products/socs/esp8266ex/resources/)：GPIO 启动条件及平台资料；不用于推断 NodeMCU 克隆板的机械尺寸。
- [Toshiba TB6612FNG 数据手册](https://toshiba.semicon-storage.com/info/TB6612FNG_datasheet_en_20141001.pdf?did=10660&prodName=TB6612FNG)：逻辑供电、VM、控制真值表及电流条件；注意区分工作条件与绝对最大额定值。
- [ST VL53L0X 数据手册](https://www.st.com/resource/en/datasheet/vl53l0x.pdf)：§2.4 电气连接、§4 地址字节；0x52 写地址对应 Wire 七位 0x29。
- [NXP SC16IS740/750/760 数据手册](https://www.nxp.com/docs/en/data-sheet/SC16IS740_750_760.pdf)：本项目拟新增 SC16IS750，提供 I²C UART 与 8 个 GPIO；§10.3 的 0x90 地址字节对应七位 0x48，A1/A0 均接 VDD。**SC16IS740 没有这 8 个 GPIO，不能直接替代。**

商家 OLED PDF 的标题可见，但本次下载/预览未成功，未把其内容写作已核验来源。BH1750 的地址暂作为待扫描配置，未将同类模块经验当作实测。
