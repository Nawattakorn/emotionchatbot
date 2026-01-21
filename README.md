# Emotion Chatbot

## ภาพรวม

โครงการ **Emotion Chatbot** นี้เป็นส่วนหนึ่งของวิชา NLP โดยบอทสามารถตรวจจับอารมณ์ของข้อความผู้ใช้และตอบกลับด้วยข้อความที่เหมาะสม แสดงการประยุกต์ใช้เทคนิคการประมวลผลภาษาธรรมชาติ เช่น การทำความสะอาดข้อความ การสกัดคุณลักษณะ และการจำแนกด้วยโมเดล Deep learning

## คุณสมบัติ

- **การตรวจจับอารมณ์**: รองรับอารมณ์เช่น Joy, Sadness, Anger, Fear, Love ,Surprise
- **การตอบสนองอย่างเห็นอกเห็นใจ**: สร้างข้อความตอบที่สอดคล้องกับอารมณ์ที่ตรวจพบ
- **Chatbot แบบโต้ตอบ**: อินเทอร์เฟซ Chatbot สำหรับการสนทนา


## การติดตั้ง

1. **คลอนรีโพซิทอรี**
   ```bash
   git clone https://github.com/Nawattakorn/emotionchatbot.git
   cd emotionchatbot
   ```
2. **สร้าง virtual environment** (แนะนำ) 
   ```bash
   python -m venv venv
   source venv/bin/activate   # บน Windows ใช้ `venv\\Scripts\\activate`
   ```
3. **ติดตั้ง dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## วิธีใช้งาน


```bash
python app.py
```

---

หมายเหตุ: โปรเจคนี้เป็นส่วนหนึ่งของวิชา NLP
