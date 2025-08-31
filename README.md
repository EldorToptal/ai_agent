# AI Agentlarni Qurish Kursi

📌 Ushbu repo Eldor Abdukhamidov tomonidan tayyorlangan **AI Agentlarni Qurish** bepul onlayn kursi uchun kodlarni o‘z ichiga oladi. Har bir bo‘limda amaliy misollar va kod loyihalari mavjud bo‘lib, ular orqali siz AI agentlarni bosqichma-bosqich yaratishni o‘rganasiz.

---

## 🚀 O‘rnatish va Ishga Tushirish

### 1. Repozitoriyani klonlash
```bash
git clone https://github.com/username/ai-agents-course.git
cd ai-agents-course
```

### 2. Virtual muhit yaratish
```bash
python -m venv agent-env
source agent-env/bin/activate  # Mac/Linux
agent-env\Scripts\activate   # Windows
```

### 3. Kutubxonalarni o‘rnatish
```bash
pip install -r requirements.txt
```

### 4. Muhit sozlamalari
`.env` faylida quyidagilarni belgilang:
```
OPENAI_API_KEY=your_api_key
HF_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_token
```

---

## 📂 Loyihaning Tuzilishi

```
section_1/    # Boshlang‘ich agentlar (API, tarjimon, test agentlar)
section_2/    # Multi-agent va funksional agentlar
section_3/    # Amaliy loyihalar:
   ├── 3_1_qism/  # Chatbot + ChromaDB
   ├── 3_2_qism/  # Coding Agent
   ├── 3_3_qism/  # HR Resume Screening Agent
   └── 3_4_qism/  # Kontent yaratish (Post + Rasm)
section_4/    # Agentlarni tarqatish (FastAPI, Streamlit, Telegram)
requirements.txt
.env.example
README.md
```

---

## 📘 Kursdagi Mavzular

### Section 1: Oddiy agentlar
- API agenti
- Tarjimon agent
- LangChain va Transformers testlari

### Section 2: Multi-agent yondashuvi
- Arithmetic agent
- Multi-funksional agent
- Memory bilan ishlash

### Section 3: Amaliy loyihalar
- **3.1 Chatbot (ChromaDB bilan)**
- **3.2 Coding Agent** (kod yozish va testlash)
- **3.3 HR Resume Screening Agent** (PDF/Matn asosida)
- **3.4 Kontent yaratuvchi agent** (LinkedIn post + rasm)

### Section 4: Agentlarni tarqatish
- **FastAPI orqali REST API**
- **Streamlit orqali web interfeys**
- **Telegram bot orqali foydalanuvchilar bilan aloqa**

---

## 📌 Foydali Havolalar
- 📖 Kurs maqolalari: [AI Agentlarni Qurish Kursi](https://medium.com/@mr.eldorabdukhamidov/ai-agentlar-qurish-bepul-onlayn-kurs-e1ad0a2246b9)
- 💬 Telegram hamjamiyat: [@EldorML](https://t.me/EldorML)

---

## 🤝 Hissa Qo‘shish
Agar xatolik topsangiz yoki yangi g‘oya qo‘shmoqchi bo‘lsangiz:
1. Fork qiling
2. O‘z branchingizda o‘zgartirish kiriting
3. Pull Request yuboring

---

## 👤 Muallif
**Eldor Abdukhamidov**  
📧 Email: mr.eldorabdukhamidov@gmail.com  
🔗 [Medium Blog](https://medium.com/@mr.eldorabdukhamidov)  
🔗 [Telegram](https://t.me/EldorML)
