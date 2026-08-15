<p align="center">
  <a href="https://github.com/b9b4ymiN/midas">
    <img alt="ปรมาจารย์แพนด้าลงทุนผู้เคร่งขรึมกำลังดีดนิ้วด้วยถุงมือทองในโปสเตอร์การ์ตูนวินเทจ" src="assets/midas-panda-banner.png" width="560">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> · <strong>ไทย</strong>
</p>

# midas

[![skills.sh](https://skills.sh/b/b9b4ymiN/midas)](https://skills.sh/b9b4ymiN/midas)

Midas คือชุดทักษะวิจัยการลงทุนสำหรับ AI agent ช่วยให้คุณเริ่มจาก ticker แล้วพัฒนาไปเป็นบทวิเคราะห์ที่มีแหล่งข้อมูล การประเมินมูลค่า แผนแบบมีเงื่อนไข และรายงาน HTML ที่สมบูรณ์ในไฟล์เดียว จากนั้นยังสามารถท้าทายผลงานนั้นก่อนที่คุณจะนำเงินจริงไปลงทุน

คุณไม่จำเป็นต้องจำชื่อทักษะทั้งหมด เริ่มด้วย `/midas` อธิบายสิ่งที่ต้องการด้วยภาษาปกติ แล้วระบบจะชี้ไปยัง workflow ที่เหมาะสม

> **เนื้อหาสำหรับการวิจัยและการศึกษาเท่านั้น ไม่ใช่คำแนะนำทางการเงิน** Midas ไม่ได้ตัดสินใจลงทุนแทนคุณและไม่รับประกันผลตอบแทน

## Midas ทำอะไร

Midas แยกงานลงทุนออกเป็นหน้าที่ที่ชัดเจน:

- **เลือก:** หาวิธีที่เหมาะกับคำถามที่คุณกำลังถาม
- **รวบรวม:** ดึงข้อมูลการเงินแบบระบุวันที่พร้อมแหล่งที่มา และบันทึก snapshot ที่นำมาเปิดซ้ำได้
- **สร้าง:** เชื่อมเรื่องราวของธุรกิจกับกำไร มูลค่า catalyst และจังหวะทางเทคนิค
- **อธิบาย:** เปลี่ยนงานทั้งหมดให้เป็น BF-Report แบบ HTML ที่อ่านง่ายและสมบูรณ์ในไฟล์เดียว
- **ท้าทาย:** มองหาข้อขัดแย้ง สมมติฐานที่เปราะบาง และเหตุผลที่ thesis อาจล้มเหลว

ทุกแผนเป็นแผนแบบมีเงื่อนไข โดยควรระบุว่าหลักฐานใดจะทำให้ thesis แข็งแรงขึ้น สิ่งใดจะทำให้อ่อนลง และควรทบทวนสถานการณ์เมื่อใด มนุษย์ยังคงมีอำนาจตัดสินใจ

## ทำไมจึงมี Midas

ความผิดพลาดในการลงทุนมักเริ่มหลังจากได้แนวคิดดีๆ ครั้งแรก เมื่อเราชอบ thesis หนึ่ง หลักฐานที่สนับสนุนมักรู้สึกหนักแน่นกว่าหลักฐานที่คัดค้าน หลายเดือนต่อมา เราอาจลืมเหตุผลที่เข้าลงทุน หรือค่อยๆ เปลี่ยนกฎเมื่อราคาเคลื่อนไหวสวนทาง

Midas ออกแบบมาโดยมีเกราะป้องกันสามชั้น:

1. **ติดตามหลักฐานได้** ตัวเลขสำคัญมีแหล่งที่มาและวันที่ของข้อมูล
2. **บันทึกเหตุผลไว้** รายงานเชื่อมเรื่องราว ตัวเลข scenario และเงื่อนไขในการทบทวนเข้าด้วยกัน
3. **โจมตี thesis ที่ทำเสร็จแล้ว** `stock-grill` ตรวจความสอดคล้องภายในรายงานก่อน stress-test เหตุผล

เป้าหมายไม่ใช่การรับประกันผลลัพธ์ที่ดี แต่คือทำให้กระบวนการตัดสินใจชัดเจน ทำซ้ำได้ และหาเหตุผลเข้าข้างตัวเองย้อนหลังได้ยากขึ้น

## การติดตั้ง

คุณต้องมี Node.js พร้อม `npm`/`npx`, Python 3.8 ขึ้นไป และสภาพแวดล้อม AI agent ที่รองรับ Agent Skills แบบติดตั้งได้ Node.js ใช้ติดตั้งทักษะ ส่วน Python ใช้รัน data และ analytical helper ใน workflow แบบเต็ม บน Windows ให้ตรวจทั้งสองรายการด้วย `npx --version` และ `python --version` รันคำสั่งต่อไปนี้ใน terminal ไม่ใช่ในแชตของ agent:

ติดตั้งทุกทักษะแบบ global:

```bash
npx skills add b9b4ymiN/midas -g --all --copy
```

แนะนำให้ใช้ `--copy` บน Windows เพราะช่วยหลีกเลี่ยงปัญหาสิทธิ์ของ symbolic link ที่พบบ่อย หลังติดตั้งให้ **restart agent session** เพื่อให้ทักษะใหม่ปรากฏขึ้น ตัวเลือก `-g` ทำให้ใช้งานทักษะได้แบบ global หากระบบไม่รู้จัก `npx` ให้ติดตั้ง Node.js รุ่นปัจจุบันแล้วเปิด terminal ใหม่ก่อนลองอีกครั้ง

<details>
<summary><strong>ติดตั้งเฉพาะทักษะที่เลือก</strong></summary>

```bash
npx skills add b9b4ymiN/midas -g -s stock-grill -s minervini-sepa --copy
```

ใช้วิธีนี้เมื่อต้องการเฉพาะการทบทวนแบบ adversarial และ workflow SEPA แบบ standalone คุณสามารถดูรายการทักษะที่มีอยู่ก่อนด้วย `npx skills add b9b4ymiN/midas -l`

</details>

<details>
<summary><strong>ติดตั้งสำเนาที่แก้ไขได้ภายในโปรเจกต์ปัจจุบัน</strong></summary>

ไม่ใส่ `-g` เพื่อให้ติดตั้งเป็นไฟล์ภายในโปรเจกต์ที่คุณเปิดดูและแก้ไขได้:

```bash
npx skills add b9b4ymiN/midas --all
```

สำเนาที่ติดตั้งจะไม่เปลี่ยนเองโดยอัตโนมัติ รัน `npx skills update` เมื่อคุณต้องการอัปเดต

</details>

## เริ่มใช้งานอย่างรวดเร็ว

หากไม่แน่ใจว่าจะเริ่มจากตรงไหน ให้พิมพ์ข้อความนี้ในแชตหรือ prompt ของ AI agent หลัง restart session:

```text
/midas
I want to analyze CPALL.BK but I do not know which workflow to use.
```

`/midas` จะอธิบายว่าทักษะใดเหมาะกับคำขอ ไม่ได้เรียกใช้ทุกวิธีโดยอัตโนมัติ เมื่อทราบเส้นทางที่ชัดเจนแล้ว ให้ขอ agent ดำเนินการต่อด้วยทักษะที่แนะนำ

หากต้องการวิเคราะห์บริษัทแบบครบถ้วน คุณสามารถขอโดยตรงได้เช่นกัน:

```text
Run a full analysis of CPALL.BK and produce the final BF-Report.
```

คำขอนี้จะไปยัง `both-stock-analysis` ซึ่งยืนยันตลาด รวบรวม data snapshot ชุดเดียวที่สอดคล้องกัน เดิน research pipeline สร้างรายงาน และจบด้วยการทบทวนแบบ adversarial

## Workflow ที่ใช้บ่อย

คุณเขียนคำขอด้วยภาษาปกติได้ Slash command มีประโยชน์สำหรับทักษะที่ผู้ใช้เรียกเอง เช่น `/midas` ส่วนทักษะที่โมเดลเรียกใช้สามารถถูกเลือกโดยอัตโนมัติเมื่อคำขอของคุณชัดเจน

| สิ่งที่คุณต้องการ | ตัวอย่าง prompt | ทักษะและผลลัพธ์ |
|---|---|---|
| รายงานการลงทุนแบบครบถ้วน | `Run a full analysis of CPALL.BK and produce the final BF-Report.` | `both-stock-analysis` → research pipeline ครบชุดและ BF-Report แบบ HTML |
| การประเมินมูลค่าเฉพาะด้าน | `Estimate the fair value of NVDA using DCF, relative valuation, and SOTP where applicable.` | `company-valuation` → fair value แบบผสมและ sensitivity grid |
| การทบทวน setup แบบ Minervini | `Run the Minervini SEPA process on AAPL.` | `minervini-sepa` → การประเมิน SEPA สี่ด่านและ setup แบบมีเงื่อนไข |
| ข้อมูลที่ย้อนดูแหล่งที่มาได้ | `Fetch reproducible financial facts for TU.BK and save a dated snapshot.` | `har-to-api` → JSON snapshot ที่มีแหล่งข้อมูลและเปิดซ้ำได้ |
| ท้าทายรายงานที่มีอยู่ | `Stress-test this BF-Report before I make a decision.` | `stock-grill` → ตรวจความสอดคล้อง โจมตีห้ารอบ และ decision journal |

## สิ่งที่คุณจะได้รับ

การทำงานแบบเต็มรูปแบบสร้าง audit trail แทนคำตอบขนาดใหญ่ที่ไม่อธิบายที่มา:

1. **Sourced data snapshot** — ชุดข้อมูลแบบระบุวันที่ที่ทั้งการวิเคราะห์ใช้ร่วมกัน
2. **Business narrative** — บริษัททำอะไร เหตุใดจึงอาจเติบโต และเรื่องราวควรสะท้อนในตัวเลขอย่างไร
3. **Business drivers** — ตัวแปรที่ทำให้กำไรเปลี่ยน พร้อม sensitivity และจังหวะเวลา
4. **Normalized earnings** — ฐานกำไรที่ปรับวัฏจักรและรายการครั้งเดียวแล้ว
5. **Valuation** — DCF, relative valuation, SOTP เมื่อเหมาะสม, fair value แบบผสม และ sensitivity grid
6. **Context** — คู่แข่งที่กระทบกำไรจริง ภาพก่อนหรือหลังประกาศงบ การเติบโตที่ทำซ้ำได้ catalyst แบบระบุวันที่ และจังหวะทางเทคนิค
7. **Investment synthesis** — insight หลัก, scenario แบบ bull/base/bear, thesis-builder, thesis-breaker และแผนแบบมีเงื่อนไข
8. **BF-Report** — เอกสารวิจัย HTML ที่ responsive บนมือถือและสมบูรณ์ในไฟล์เดียว
9. **Adversarial review** — ตรวจความสอดคล้องภายในและจงใจโจมตี thesis
10. **Decision journal** — บันทึกความเชื่อ ระดับความมั่นใจ เงื่อนไขความล้มเหลว และ trigger สำหรับทบทวนก่อนทราบผลลัพธ์

## การวิเคราะห์เต็มรูปแบบทำงานอย่างไร

<p align="center">
  <img alt="แพนด้า Midas เลือกหุ่นแนวคิดแบบ Minervini จากชั้นที่แบ่งหมวดเครื่องมือคิดของนักลงทุน" src="assets/midas-investor-module-lab.png" width="760">
</p>

workflow แบบเต็มเลือก “เครื่องมือคิด” ที่ต่างกันให้เหมาะกับงานแต่ละประเภท โดย `both-stock-analysis` ประสานงานตามลำดับนี้:

```text
Step 0: data snapshot
→ resolve market, exchange suffix, currency, and country risk
→ business narrative
→ business drivers
→ earnings quality
→ company valuation
→ impact peers
→ earnings setup/recap and growth catalysts
→ technical timing
→ investment synthesis
→ BF-Report
→ stock-grill
```

ขั้น construction มี **สิบเอ็ด sub-skills** โดย data layer ทำงานก่อน จากนั้น orchestrator ควบคุมลำดับ และ `stock-grill` โจมตีผลลัพธ์ที่เสร็จแล้วในภายหลัง หากต้องการเพียงบางส่วน เช่น valuation หรือ earnings quality คุณเรียกใช้ทักษะนั้นได้โดยไม่ต้องเดินทั้ง pipeline

## เลือกทักษะที่เหมาะสม

| คำถามของคุณ | ใช้ |
|---|---|
| “ฉันไม่รู้ว่าจะเริ่มตรงไหน” | `/midas` |
| “ขอภาพรวมทั้งหมดและรายงานที่เสร็จสมบูรณ์” | `both-stock-analysis` |
| “ดึงข้อมูลครั้งเดียวและแสดงว่าเอามาจากไหน” | `har-to-api` |
| “อธิบายเรื่องราวของธุรกิจที่อยู่เบื้องหลังตัวเลข” | `business-narrative` |
| “อะไรขับเคลื่อนกำไรของบริษัทนี้จริงๆ” | `business-drivers` |
| “กำไรที่รายงานเป็นฐานประเมินมูลค่าที่เชื่อถือได้หรือไม่” | `earnings-quality` |
| “บริษัทมีมูลค่าเท่าไร” | `company-valuation` |
| “คู่แข่งรายใดส่งผลต่อกำไรอย่างมีนัยสำคัญได้” | `peer-impact` |
| “ควรรู้อะไรก่อนประกาศผลประกอบการครั้งต่อไป” | `earnings-preview` |
| “ผลประกอบการล่าสุดเปลี่ยนแปลงอะไร” | `earnings-recap` |
| “การเติบโตทำซ้ำได้หรือไม่ และ catalyst ใดมีวันที่ชัดเจน” | `growth-outlook` |
| “กราฟรายสัปดาห์และรายวันบอกอะไรเกี่ยวกับจังหวะ” | `bf-tech-analysis` |
| “รวมงานวิจัยเป็น thesis และแผนแบบมีเงื่อนไขหนึ่งชุด” | `investment-synthesis` |
| “สร้างงานวิจัยเป็นเอกสาร HTML แบบมืออาชีพ” | `bf-report` |
| “ลองทำลาย thesis ที่เสร็จแล้วนี้” | `stock-grill` |
| “เรียกใช้กระบวนการ Minervini SEPA” | `minervini-sepa` |

หากยังไม่คุ้นกับคำศัพท์: **DCF** ประเมินมูลค่าจากกระแสเงินสดที่คาดหวัง; **SOTP** ประเมินส่วนต่างๆ ของธุรกิจแยกกัน; **sensitivity grid** แสดงว่ามูลค่าเปลี่ยนอย่างไรเมื่อสมมติฐานเปลี่ยน; **provenance tier** ระบุคุณภาพหรือบทบาทของแหล่งข้อมูล; **Trend Template** และ **VCP** คือตัวกรองกราฟของ Minervini; และ **risk geometry** เปรียบเทียบจุดเข้า stop target และผลขาดทุนที่เป็นไปได้

## รายการอ้างอิงทักษะ

ปัจจุบัน repository มี **16 skills** เริ่มที่ router เมื่อคุณไม่แน่ใจ ใช้ workflow แบบเต็มสำหรับงานตั้งแต่ต้นจนจบ หรือเข้าถึง construction skill โดยตรงเมื่อต้องการคำตอบเฉพาะด้านหนึ่ง

### เริ่มที่นี่

- **[midas](./skills/midas/SKILL.md)** — router ที่ผู้ใช้เรียกเองเพื่อเลือก workflow การลงทุนที่เหมาะสมจากคำขอภาษาปกติ

### Data layer

- **[har-to-api](./skills/har-to-api/SKILL.md)** — ดึงข้อมูลการเงินพร้อม provenance บันทึก snapshot แบบระบุวันที่ และสร้าง client จาก traffic ของเว็บไซต์ที่บันทึกไว้เมื่อต้องเพิ่มแหล่งข้อมูลใหม่

### Workflow แบบเต็ม

- **[both-stock-analysis](./skills/pipeline/both-stock-analysis/SKILL.md)** — ประสานงาน workflow จาก ticker ไปถึงรายงานทั้งหมด รวม construction sub-skills สิบเอ็ดตัวและการทบทวนแบบ adversarial ขั้นสุดท้าย

### Construction: ทักษะเฉพาะด้านสิบเอ็ดตัว

- **[business-narrative](./skills/pipeline/business-narrative/SKILL.md)** — เปลี่ยนงานวิจัยบริษัทเป็นแผนที่เชื่อมเรื่องราวกับตัวเลข
- **[business-drivers](./skills/pipeline/business-drivers/SKILL.md)** — ระบุและวัดปัจจัยที่ขับเคลื่อนกำไร
- **[earnings-quality](./skills/pipeline/earnings-quality/SKILL.md)** — ปรับฐานกำไรให้เป็นปกติและทดสอบว่าการเติบโตที่รายงานเชื่อถือได้หรือไม่
- **[company-valuation](./skills/pipeline/company-valuation/SKILL.md)** — รวม DCF, relative valuation และ SOTP เมื่อเหมาะสม แล้วแสดง sensitivity
- **[peer-impact](./skills/pipeline/peer-impact/SKILL.md)** — ค้นหาคู่แข่งที่การกระทำสามารถส่งผลต่อกำไรของบริษัทผ่านการใช้ input หรือลูกค้ากลุ่มเดียวกัน หรือผ่านอำนาจในการกำหนดราคา
- **[earnings-recap](./skills/pipeline/earnings-recap/SKILL.md)** — เปรียบเทียบผลที่รายงานกับความคาดหวังและอธิบายสิ่งที่เปลี่ยนไป
- **[earnings-preview](./skills/pipeline/earnings-preview/SKILL.md)** — เตรียมพร้อมก่อนประกาศงบด้วย consensus ประวัติ และ positioning
- **[growth-outlook](./skills/pipeline/growth-outlook/SKILL.md)** — แยกแหล่งที่มาของการเติบโต ตัดสินความสามารถในการทำซ้ำ และบันทึก catalyst แบบระบุวันที่
- **[bf-tech-analysis](./skills/pipeline/bf-tech-analysis/SKILL.md)** — อ่านกราฟรายสัปดาห์และรายวันเพื่อหาจังหวะ ความเสี่ยง และระดับ invalidation แบบมีเงื่อนไข
- **[investment-synthesis](./skills/pipeline/investment-synthesis/SKILL.md)** — รวม narrative, valuation, earnings และ timing เป็น scenario กับแผนแบบมีเงื่อนไข
- **[bf-report](./skills/pipeline/bf-report/SKILL.md)** — สร้างงานวิจัยที่เสร็จแล้วเป็นเอกสาร HTML สมบูรณ์ในตัวเองสไตล์เอกสารยื่นตลาด

### การทบทวนแบบ Adversarial

- **[stock-grill](./skills/stock-grill/SKILL.md)** — ตรวจรายงานที่เสร็จแล้วเพื่อหาข้อขัดแย้ง โจมตีสมมติฐานห้ารอบ และสร้าง decision journal ที่ลงทะเบียนความคิดไว้ล่วงหน้า

### ระบบเทคนิคแบบ Standalone

- **[minervini-sepa](./skills/minervini-sepa/SKILL.md)** — ใช้กระบวนการ SEPA สี่ด่าน: fundamentals, Trend Template, VCP setup และ risk geometry

## ข้อมูลที่ติดตามและเปิดซ้ำได้

data layer `har-to-api` คือ Step 0 ของการวิเคราะห์เต็มรูปแบบ ระบบดึงข้อมูลครั้งเดียวเพื่อให้ขั้นตอนต่อๆ ไปไม่ใช้ราคาหรือรอบรายงานที่ต่างกันโดยไม่บอก

กฎหลักคือ:

- ข้อมูลทุกตัวที่ดึงมาบันทึก **แหล่งที่มา วันที่ของข้อมูล URL และ provenance tier**
- ข้อมูลที่ขาดจะยังคงเป็นข้อมูลที่ขาด ระบบไม่ควรสร้างตัวเลขขึ้นมาเพื่อเติมตาราง
- แหล่งสำรอง เช่น yfinance จะถูกระบุเป็น `FALLBACK` พร้อมเหตุผล
- หากผู้ให้บริการสองรายให้ข้อมูลตัวเดียวกันต่างกันเกิน **2%** ระบบจะรายงานความต่างแทนการเลือกคำตอบหนึ่งอย่างเงียบๆ
- snapshot แบบระบุวันที่เปิดซ้ำได้ จึงช่วยแยกได้ว่า “ข้อมูลเปลี่ยน” หรือ “การวิเคราะห์เปลี่ยน”
- ข้อมูล segment ควรตรวจสอบกับเอกสาร filing หลักของบริษัทเสมอ

mapping `stockanalysis` ที่ให้มามี local-fixture coverage และเส้นทางที่ map ไว้หกเส้นทางสำหรับหลักทรัพย์ US และ Thai อย่างไรก็ตาม เส้นทางจริงบนเครือข่ายสามารถเปลี่ยนได้ และ live HTTP path รวมถึง provider profile อื่นนอกจาก `stockanalysis` ยังมีข้อจำกัดด้านการตรวจสอบที่บันทึกไว้ smoke check ระดับ repository นี้มีไว้สำหรับผู้ใช้ที่ต้องการตรวจ provider โดยตรง ไม่จำเป็นสำหรับการเปิดใช้ทักษะที่ติดตั้งแล้ว ให้ดาวน์โหลด repository checkout และรันใน Bash (Git Bash หรือ WSL บน Windows):

```bash
git clone https://github.com/b9b4ymiN/midas.git
cd midas
bash skills/har-to-api/tests/smoke_live.sh TU bkk
```

เคารพเงื่อนไขและ rate limit ของผู้ให้บริการ และตรวจตัวเลขสำคัญต่อการตัดสินใจกับ filing หลัก การ replay snapshot ที่บันทึกไว้จะทำซ้ำ input data ของการวิเคราะห์ครั้งก่อน ส่วนการดึงข้อมูลจาก live provider ใหม่คือการ capture ครั้งใหม่และอาจได้ข้อมูลที่เปลี่ยนไป

## ข้อจำกัดและการใช้งานอย่างรับผิดชอบ

- Midas ช่วยปรับโครงสร้างงานวิจัย แต่ไม่สามารถกำจัดความไม่แน่นอนหรือรับประกันผลลัพธ์
- ความพร้อมของแหล่งข้อมูล รูปแบบเว็บไซต์ ข้อมูลตลาด และประมาณการของนักวิเคราะห์สามารถเปลี่ยนแปลงได้
- valuation ขึ้นอยู่กับสมมติฐาน ให้อ่าน sensitivity grid ไม่ใช่ดูเฉพาะ fair value หลัก
- ระดับทางเทคนิคเป็นตัวกำหนดความเสี่ยงแบบมีเงื่อนไข ไม่ใช่คำรับรองว่าราคาจะเคลื่อนไหวตามที่คาด
- persona และ methodology ที่มีชื่อเป็นเครื่องมือคิดอย่างมีโครงสร้าง ไม่ใช่การจำลองบุคคลเหล่านั้นอย่างแม่นยำหรือการรับรองจากบุคคลดังกล่าว
- รายงานสุดท้ายอาจมีข้อผิดพลาดหรือข้อมูลจากบุคคลที่สามที่ล้าสมัย ตรวจสอบข้อเท็จจริงสำคัญกับ filing และประกาศทางการ
- ผลลัพธ์คือแผนแบบมีเงื่อนไขและคำถามวิจัย ไม่ใช่คำสั่งให้ซื้อ ขาย หรือถือ

<details>
<summary><strong>รายละเอียดภายในระบบ</strong></summary>

### โครงสร้าง Repository

```text
skills/
├── midas/                  router
├── har-to-api/             traceable and replayable data layer
├── pipeline/               orchestrator plus 11 construction skills
├── stock-grill/            adversarial review
└── minervini-sepa/         standalone SEPA system
```

แต่ละทักษะเป็น folder ที่มี `SKILL.md` ซึ่งจำเป็น และอาจมี directory `references/`, `scripts/`, `assets/`, `agents/` หรือ `tests/` แต่ละทักษะทำงานได้ด้วยตัวเองเมื่อติดตั้ง

helper script ใช้ Python 3.8+ standard library ส่วน `har-to-api` จะ import yfinance แบบ lazy เฉพาะเมื่อต้องใช้ fallback ที่มีการทำเครื่องหมายไว้ Shell regression test ครอบคลุม data layer และ analytical helper หลายตัว แต่พฤติกรรมของ provider จริงยังต้องใช้ smoke check ตามที่บันทึกไว้

[`CONTEXT.md`](./CONTEXT.md) คือคำศัพท์มาตรฐานสำหรับการเขียนของ maintainer ทักษะที่ติดตั้งแล้วไม่พึ่งพา root file นี้ แต่ละทักษะมีคำจำกัดความที่ตัวเองต้องใช้ การตัดสินใจด้าน methodology ที่ย้อนกลับยากควรอยู่ใน `docs/adr/` ส่วน decision journal ของแต่ละหุ้นควรอยู่กับผลการวิเคราะห์หุ้นนั้น ไม่ใช่ใน repository นี้

deliverable หลักใช้ชื่อ `[TICKER]_BF-Report.html`: เป็นไฟล์สมบูรณ์ในตัวเองหนึ่งไฟล์ที่ agent นำเสนอให้ดาวน์โหลดและเปิดด้วย web browser ปกติได้ ส่วน data snapshot แบบระบุวันที่และ decision journal จะอยู่กับผลการวิเคราะห์หุ้นนั้น `stock-grill` อ่านรายงานที่ render แล้ว โดยควรแก้ consistency error ระดับสูงก่อนเริ่มห้ารอบการทดสอบเหตุผล ส่วนข้อค้นพบจาก grill และ journal จะยังเป็น analysis artifact แยกต่างหาก เว้นแต่ผู้ใช้ขอรายงานฉบับแก้ไข

</details>

## License

Midas ใช้งานได้ภายใต้ [MIT License](LICENSE)

## ข้อสงวนสิทธิ์

**เนื้อหาสำหรับการวิจัยและการศึกษาเท่านั้น ไม่ใช่คำแนะนำทางการเงิน** ไม่มีสิ่งใดใน repository นี้หรือ artifact ที่สร้างขึ้นเป็นคำแนะนำให้ซื้อ ขาย หรือถือหลักทรัพย์ใด โปรดตรวจตัวเลขสำคัญกับ filing หลักและตัดสินใจตามสถานการณ์กับขีดจำกัดความเสี่ยงของคุณเอง
