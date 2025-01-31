# Итоговый проект по Python

## Запуск

### Инициализация airflow

Выполните следующую команду для инициализации Airflow:
   ```bash
   docker compose -f docker-compose.init.yaml -d up
   ```

### Инициализация всего сервиса
Выполните:
```bash
docker compose up
```
---

## Airflow Dags

### Вход в Airflow
Используйте следующие учетные данные для входа:
- **Логин:** `admin`
- **Пароль:** `admin`

### Описание доступных DAGs

#### 1. **`initial_migration`**
- Запускается **один раз** для инициализации.
- Функциональность:
  - Создание таблиц в Postgres и MySQL.
  - Загрузка первичных данных в Postgres.

#### 2. **`import`**
- Периодичность: **ежедневно**.
- Функциональность:
- Импорт таблиц из PG в MySQL сделан через Sparj

- **Настройка таблиц для импорта**:
  - Содержится в директории `code/tasks/import/`.

#### 3. **`data_marts`**
- Функциональность:
  - Построение аналитических витрин сделано внутри MySQL. Чисто по опыту, аналитикам намного привычнее работать с SQL, чем с pyspark. И большинство аналитиков pyspark не владеют. Поэтому для удоства конечного пользователя было принято такое решение, что витрины собираются не через спарк.
- **Создание витрин**:
  - Конфиги для задач лежат в `code/tasks/marts/`.
  - SQL-скрипты для сборки лежат в `code/queries/marts`
---


# Аналитическая витрина `sales_analysis`

## Описание
Витрина `sales_analysis` создана для объединения данных о пользователях, заказах, продуктах и категориях в единую таблицу, предназначенную для аналитики. Она предоставляет исчерпывающую информацию, необходимую для построения отчетов, анализа продаж и принятия управленческих решений.

### Основные цели:
- Оценка доходов по продуктам, категориям и клиентам.
- Выявление самых прибыльных клиентов и наиболее продаваемых продуктов.
- Анализ статусов заказов для оптимизации выполнения заказов.
- Построение аналитических отчетов на основе интеграции данных из операционных таблиц.

## Структура витрины

| Поле                   | Описание                                                   |
|-------------------------|-----------------------------------------------------------|
| `user_id`              | Уникальный идентификатор пользователя.                     |
| `full_name`            | Полное имя клиента.                                        |
| `email`                | Email клиента.                                             |
| `phone`                | Телефон клиента.                                           |
| `loyalty_status`       | Статус лояльности клиента (`Gold`, `Silver`, `Bronze`).     |
| `order_id`             | Уникальный идентификатор заказа.                           |
| `order_date`           | Дата размещения заказа.                                    |
| `order_total`          | Общая сумма заказа.                                        |
| `product_id`           | Уникальный идентификатор продукта.                         |
| `product_name`         | Название продукта.                                         |
| `category_name`        | Название категории продукта.                               |
| `quantity`             | Количество купленного продукта.                           |
| `price_per_unit`       | Цена за единицу продукта.                                  |
| `total_price_per_product` | Общая стоимость продукта в рамках одного заказа.         |
| `order_status`         | Статус заказа (`Pending`, `Completed`, `Canceled`).        |

## SQL Исходник

```sql
-- Создание аналитической витрины "sales_analysis"
CREATE TABLE sales_analysis AS
SELECT
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) AS full_name,
    u.email,
    u.phone,
    u.loyalty_status,
    o.order_id,
    o.order_date,
    o.total_amount AS order_total,
    p.product_id,
    p.name AS product_name,
    pc.name AS category_name,
    od.quantity,
    od.price_per_unit,
    od.quantity * od.price_per_unit AS total_price_per_product,
    o.status AS order_status
FROM
    orders o
JOIN
    users u ON o.user_id = u.user_id
JOIN
    orderDetails od ON o.order_id = od.order_id
JOIN
    products p ON od.product_id = p.product_id
JOIN
    productCategories pc ON p.category_id = pc.category_id;
```

## Примеры использования

### 1. Доходы по категориям продуктов
```sql
SELECT
    category_name,
    SUM(total_price_per_product) AS total_revenue
FROM
    sales_analysis
GROUP BY
    category_name
ORDER BY
    total_revenue DESC;
```

### 2. Топ-5 клиентов по доходам
```sql
SELECT
    full_name,
    email,
    SUM(order_total) AS total_spent
FROM
    sales_analysis
GROUP BY
    user_id, full_name, email
ORDER BY
    total_spent DESC
LIMIT 5;
```

### 3. Самые продаваемые продукты
```sql
SELECT
    product_name,
    category_name,
    SUM(quantity) AS total_sold
FROM
    sales_analysis
GROUP BY
    product_id, product_name, category_name
ORDER BY
    total_sold DESC
LIMIT 10;
```

### 4. Процент завершенных заказов
```sql
SELECT
    order_status,
    COUNT(*) AS order_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage
FROM
    sales_analysis
GROUP BY
    order_status;
```

