## Loyihani ishga tushirish (Quick Start)

### 1. Loyihani GitHubdan klon qilish

```bash
git clone https://github.com/SIZNING_USERNAME/sales-intelligence-api.git
cd sales_intelligence_api

# Virtual muhit yaratish (tavsiya etiladi)
python -m venv venv
source venv/bin/activate          # Linux/Mac
# yoki Windowsda:
venv\Scripts\activate

# Paketlarni o'rnatish
pip install -r requirements.txt
python scripts/data_pipeline.py

# Ma'lumotlarni tozalash va tayyorlash (bir marta)
python scripts/data_pipeline.py

#API ni lokalda ishga tushirish
uvicorn app.main:app --reload

#Brauzerda oching:
http://127.0.0.1:8000/docs → Swagger interfeysi ochiladi
http://127.0.0.1:8000/metrics → asosiy metrikalarni ko'rasiz
..................