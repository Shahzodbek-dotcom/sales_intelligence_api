## 6. Performance & Scalability

Loyiha 120 000+ qatorli dataset bilan ishlaydi (sales.csv). Katta hajmda tez va barqaror ishlashi uchun quyidagi yondashuvlar qo‘llanilgan yoki rejalashtirilgan.

### Katta datasetni tez ishlash strategiyasi

- **Faylni chunks (bo‘laklar) bilan o‘qish va ishlov berish**  
  `data_pipeline.py` da `pd.read_csv(chunksize=30_000)` orqali butun fayl birdaniga xotiraga yuklanmaydi. Har bir 30 ming qatorlik bo‘lak alohida tozalanadi (duplicates, missing values, noto‘g‘ri narx/quantity filtrlanadi), revenue va profit hisoblanadi. Oxirida `pd.concat` bilan birlashtiriladi.  
  Bu yondashuv xotira sarfini 5–10 baravar kamaytiradi va millionlab qator bilan ham muammosiz ishlaydi.

- **Tozalangan ma’lumotni bir marta saqlash va qayta ishlatish**  
  Pipeline natijasi `cleaned_sales.csv` fayliga saqlanadi.  
  `analytics.py` va `main.py` da global `df_global` o‘zgaruvchisi orqali bu fayl faqat dastur ishga tushganda bir marta o‘qiladi. Barcha endpointlar shu bir xil DataFrame dan foydalanadi.  
  Natija: har bir so‘rovda 120 000 qatorni qayta tozalash yoki hisoblash amalga oshirilmaydi.

- **PostgreSQL optimizatsiyalari**  
  `load_to_db.py` da ma’lumotlar `to_sql(chunksize=10_000)` bilan yuklanadi.  
  Kelajakda qo‘shilishi rejalashtirilgan:  
  - Indekslar: `order_date`, `product_id`, `region`, `category` ustunlariga  
  - Materialized views: masalan oylik revenue jami summalari uchun (har kuni yangilanadi)  
  - Partitioning: `order_date` bo‘yicha yillar bo‘yicha jadvalni bo‘lish

### Caching qayerda ishlatiladi

Hozirgi versiyada **tashqi caching** (Redis, Memcached) ulanmagan, lekin quyidagi oddiy in-memory caching mexanizmi qo‘llanilgan:

- Global `df_global` — tozalangan DataFrame dastur boshlanganda bir marta yuklanadi va butun API davomida xotirada saqlanadi. Bu eng samarali oddiy caching usuli hisoblanadi (har so‘rovda faylni qayta o‘qish yo‘q).

Kelajakda yaxshilash rejalari (tavsiya etilgan joylar):

- `/metrics` (jami revenue, profit, margin) → 5–15 daqiqa cache  
- `/top-products` (top 10 mahsulot) → 30–60 daqiqa cache  
- `/sales-trend` (monthly trend, weekday/weekend, payment dist) → 15–60 daqiqa cache  
- `/forecast` (moving average) → 1 soat cache  

Amalga oshirish usuli:  
- `fastapi-cache2` + Redis (docker-compose ga Redis qo‘shish orqali)  
- Endpointlarga `@cache(expire=... )` decorator qo‘shish  
- Eng qimmat funksiyalarga `@lru_cache` yoki vaqt bilan cheklangan oddiy cache

### Async vs Sync qachon ishlatiladi

Hozirgi loyiha to‘liq **synchronous** (sync) tarzda yozilgan.

- **Sync ishlatilgan joylar va sabablari**  
  - Pandas operatsiyalari (groupby, sum, merge, nlargest) — CPU-bound, async foydasi deyarli yo‘q  
  - Fayl o‘qish va tozalash — bir marta bajariladi, bloklash muammo emas  
  - Endpointlar oddiy va tez hisoblanadi → sync bilan yetarli va kod sodda  

- **Async qachon va nima uchun kerak bo‘ladi**  
  - Yuklama yuqori bo‘lganda (100+ so‘rov/sekund)  
  - PostgreSQL dan ko‘p o‘qish bo‘lganda (I/O-bound)  
  - External API chaqiruvlari paydo bo‘lganda (masalan real vaqt savdo monitoringi)  

Yaxshilash rejalari:  
- Endpointlarni `async def` ga o‘zgartirish  
- DB uchun `asyncpg` yoki `databases[postgresql]` ishlatish  
- Heavy hisoblar (masalan forecasting) ni background task (Celery yoki FastAPI background_tasks) ga o‘tkazish

### Batch processing

Batch processing — katta ma’lumotlarni kichik guruhlar bilan ishlash (xotira tejash va xavfsizlik uchun).

Qo‘llanilgan joylar:

- **Data pipeline’da**  
  `pd.read_csv(chunksize=30_000)` bilan fayl 30 ming qatorlik bo‘laklarda o‘qiladi va ishlov beriladi. Har chunk alohida merge, tozalash va hisoblashdan o‘tadi.  

- **DB ga yuklashda**  
  `load_to_db.py` da `df.to_sql(..., chunksize=10_000)` — 10 ming qator bir tranzaksiyada yoziladi. Bu katta jadvalni yuklashda xotira va vaqtni tejaydi, tranzaksiya xavfsizligini oshiradi.

Afzalliklari:  
- Xotira to‘lib ketmaydi (ayniqsa 500 MB+ datasetda)  
- Agar xato chiqsa, butun jarayon emas, faqat bitta chunk buziladi  
- Kelajakda multiprocessing bilan parallel batch ishlash mumkin

Xulosa:  
Hozirgi loyiha o‘rta hajmdagi dataset (100–500 ming qator) uchun yetarli tezlik va barqarorlikka ega.  
Millionlab qator va yuqori trafik uchun chunks, caching (Redis), async DB va partitioning qo‘shish orqali yanada skalable qilish mumkin.