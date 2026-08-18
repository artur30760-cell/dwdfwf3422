import sqlite3
import datetime

DB_PATH = "bot_database.db"

def init_db():
    """Инициализация таблиц базы данных"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Таблица заказов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_key TEXT,
                amount INTEGER,
                currency TEXT DEFAULT 'XTR',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Автоматическая миграция для существующих баз
        try:
            cursor.execute("ALTER TABLE orders ADD COLUMN currency TEXT DEFAULT 'XTR'")
        except sqlite3.OperationalError:
            pass

        conn.commit()



def add_user(user_id: int, username: str, full_name: str):
    """Добавление или обновление пользователя"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name
        """, (user_id, username, full_name))
        conn.commit()


def get_all_user_ids() -> list[int]:
    """Получение списка ID всех пользователей для рассылки"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        return [r[0] for r in rows]


def add_order(user_id: int, product_key: str, amount: int, currency: str = "XTR"):
    """Запись совершенного заказа"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (user_id, product_key, amount, currency)
            VALUES (?, ?, ?, ?)
        """, (user_id, product_key, amount, currency))
        conn.commit()


def get_stats() -> dict:
    """Получение статистики для админ-панели"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Всего пользователей
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        # Всего заказов
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]

        # Заработано звезд (XTR)
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM orders WHERE currency = 'XTR'")
        total_stars = cursor.fetchone()[0]

        # Заработано рублей (RUB)
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM orders WHERE currency = 'RUB'")
        total_rubles = cursor.fetchone()[0]

        # Последние 5 покупок
        cursor.execute("""
            SELECT user_id, product_key, amount, currency, created_at
            FROM orders
            ORDER BY id DESC
            LIMIT 5
        """)
        recent_orders = cursor.fetchall()

        return {
            "total_users": total_users,
            "total_orders": total_orders,
            "total_stars": total_stars,
            "total_rubles": total_rubles,
            "recent_orders": recent_orders
        }
