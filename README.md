# Order Book 

## Описание

Теставая задача от azati.
Все тесты изолированы.

### Основные возможности:

- Создание покупок и продаж акций (buy/sell orders)
- Автоматическое создание транзакций при удовлетворении условий
- Поддержка частичных исполнений ордеров
- Отмена ордеров
- Просмотр выполненных транзакций

## Стек технологий

- **Back-end:** FastAPI
- **Database:** PostgreSQL
- **Dependency Management:** Poetry
- **Containerization:** Docker, Docker Compose
- **Testing:** Pytest

## Образ Докер хаб
docker pull saxles/order-book:latest
### Требования

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/) (если вы планируете запуск без Docker


