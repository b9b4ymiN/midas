# MINT historical integrity example (20 Oct 2026)

**Teaching fixture only.** Do not treat it as live price or current financial data.

## Q3 baseline error

An early MINT research report wrote that Q3 FY2026 core profit of THB 2.3–2.4 billion would represent 8–12% growth over Q3 FY2025. The reported historical base used in that report was **THB 2.768 billion** in Q3 FY2025.

Arithmetic: 2.300 / 2.768 − 1 = **−16.9%**, and 2.400 / 2.768 − 1 = **−13.3%**. Thus positive 8–12% growth is inconsistent with the stated base. **Treat as a BLOCKER** before writing headlines, charts or trade-trigger narration. Route back to `earnings-preview` or `investment-synthesis` (whichever owns the threshold), then revalidate.

## WACC/ROIC accounting-basis error

Another section presented ROIC of 9.96% and a valuation WACC of 9.50%, but described the spread as approximately +1.6 percentage points. On those two inputs the arithmetic difference is **0.46 percentage points**. The +1.6 calculation appears to use a different WACC, roughly 8.31%. The editor should flag the definitions and request an upstream reconciliation instead of silently picking one result.

## Recommended reader-language example

"บริษัทประเมินต้นทุนเงินทุนเฉลี่ยไว้ที่ 9.50% ขณะที่ตัวเลขผลตอบแทนจากเงินลงทุนที่ไม่นับภาระเช่าอยู่ที่ 9.96% เมื่อหักลบตรง ๆ จะต่างกัน 0.46 จุดเปอร์เซ็นต์ แต่เรายังไม่ควรใช้ผลต่างนี้เพื่อฟันธงว่าบริษัทสร้างมูลค่าเพิ่ม จนกว่าจะยืนยันว่านิยามเงินทุนของทั้งสองอัตราสอดคล้องกัน"

If the numerical base is not reconciled, **do not** create a bar chart comparing these as directly equivalent.