# Alpha Photo Share

## Опис

**Alpha Photo Share** — це веб-застосунок для обміну світлинами, який дозволяє користувачам завантажувати, редагувати, оцінювати та коментувати фотографії. Він забезпечує аутентифікацію користувачів з різними ролями та підтримує функціональність пошуку, фільтрації і трансформації зображень, а також надає можливість працювати з QR-кодами та рейтингами фотографій.

## Вимоги

- Python 3.12+
- Файл `.env` із необхідними змінними середовища

## Встановлення

1. Клонуйте репозиторій:

   ```bash
   git clone https://github.com/your-org/alpha-photo-share.git
   cd alpha-photo-share
   ```

2. Встановіть залежності через Poetry:

   ```bash
   poetry install
   ```

3. Створіть файл `.env` у кореневій директорії на основі `.env.example`:

   ```bash
   cp .env.example .env
   ```

4. Активуйте середовище:

   ```bash
   poetry shell
   ```

## Запуск застосунку

```bash
uvicorn main:app --reload
```
- `app.main` — шлях до FastAPI застосунку.
- `--reload` — автоматичне перезавантаження при зміні коду.

    або

```bash
python -m main
```
- `main` — шлях до main.py файлу.

## Структура проєкту

```bash
.
├── src/
│   ├── db/                  # Підключення до баз даних, declarative_base
│   ├── api/                 # Роутери
│   ├── models/              # ORM моделі
│   ├── schemas/             # Pydantic-схеми
│   ├── repository/          # Логіка доступу до БД
│   ├── services/            # Бізнес-логіка
│   └── core/                # Конфігурації, логування
├── tests/                   # Юніт-тести
├── main.py                  # Точка входу FastAPI
├── .env                     # Конфігурація
├── .env.example             # Шаблон для конфігурації
├── pyproject.toml           # Poetry конфігурація
├── CONTRIBUTING.md          # Інструкції для внесення змін у проєкт
└── README.md                # Основна документація проєкту
```

## Документація API

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Тестування

```bash
pytest
```

Або, якщо ви не в `poetry shell`:

```bash
poetry run pytest
```

