# DigiNest — магазин цифрових товарів

**DigiNest** — це e-commerce-движок на **Django 5**, розрахований на продаж шаблонів, e-книг, іконок та іншого цифрового контенту. У репозиторії вже налаштовані Tailwind CSS, система авторизації, кошик і локальна LLM-інтеграція для «розумного» пошуку.

---

## 🔥 Основні можливості

| Блок | Функціонал |
|------|------------|
| **Каталог** | пагінація, фільтр, звичайний та AI-пошук |
| **Картка товару** | назва, ціна, опис, зображення, кнопка «Додати до кошика» |
| **Кошик** | Many-to-Many із Product, підрахунок суми, видалення позицій |
| **Auth** | реєстрація, логін, профіль (аватар, телефон) |
| **Tailwind 4** | чорно-білий clean-theme (локальна збірка, без CDN) |
| **AI Search** | локальна Llama-модель (GGUF) через API `/ai-suggest/` |
| **Адмінка** | Django admin із кастомним `ProductAdmin` |

<p align="center">
  <img src="docs/home.png" width="720" alt="Головна сторінка DigiNest">
</p>

---

## ⚙ Технологічний стек

* Python 3.12 · Django 5.2  
* Tailwind CSS 4 (+ PostCSS, Autoprefixer)  
* llama.cpp + llama-cpp-python 0.2 (формат GGUF)  
* SQLite 3 (легко змінюється на PostgreSQL/MySQL)

---

## 🚀 Швидкий старт (локально)

> **Windows PowerShell**; на Linux/macOS — змініть шляхи та активацію `venv`.

```powershell
git clone https://github.com/your-user/DigiNest.git
cd DigiNest

# 1) Python-довкілля
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2) Міграції та суперкористувач
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 3) Завантажити LLM-модель (≈4 ГБ, GGUF)
$env:HF_TOKEN = "hf_xxxxxxxxxxxxxxxxx"
python scripts\get_model.py   # збережеться в store\models\…

# 4) Зібрати Tailwind
npm install
npm run build   # постійний watch: npx @tailwindcss/cli …

# 5) Запуск
python manage.py runserver
