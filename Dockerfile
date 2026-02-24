```dockerfile
# Python 3.11 yoki 3.12 slim – eng kichik va tez variant
FROM python:3.12-slim

# Ishchi katalog
WORKDIR /app

# Avval requirements ni copy qilish – layer caching uchun
COPY requirements.txt .

# Paketlarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Qolgan loyiha fayllarini copy qilish
COPY . .

# Uvicorn orqali FastAPI ni ishga tushirish
# --host 0.0.0.0 → tashqi ulanishlarga ochiq
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]