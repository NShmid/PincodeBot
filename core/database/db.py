import sqlite3
from datetime import datetime


def create_tables():
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE,
        name TEXT,
        phone_number TEXT
    )            
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY,
        admin_id INTEGER UNIQUE
    )            
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        count INTEGER,
        price DOUBLE
    )            
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS basket (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product_id INTEGER,
        count INTEGER
    )            
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY,
        seller_id INTEGER UNIQUE,
        admin_id INTEGER,
        token TEXT,
        is_used BOOL
    )            
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders  (
        id INTEGER PRIMARY KEY,
        order_descr TEXT,
        user_id INTEGER,
        seller_id INTEGER,
        date DATETIME,
        time TEXT,
        order_status TEXT
    )            
    """)
    
    conn.commit()
    conn.close()


def add_product(name: str, descr: str, count: int, price: float):
    """Функция для добавления продукта в ленту"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("""INSERT INTO products (name, description, count, price) 
                   VALUES (?, ?, ?, ?)""", (name, descr, count, price))
    
    conn.commit()
    conn.close()


def get_products(offset: int, limit=7):
    """Возвращает информацию о всех продуктах"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    
    conn.close()
    
    return rows


def get_product(product_id: int):
    """Возвращает информацию о продукте"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    rows = cursor.fetchall()
    
    conn.close()
    
    return rows


def get_basket(user_id: int):
    """Функция для получения корзины покупателя"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT product_id, count FROM basket WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    
    conn.close()
    
    return rows


def add_product_to_basket(user_id: int, product_id):
    """Функция для добавления продукта в корзину"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM basket WHERE product_id = ? AND user_id = ?", (product_id, user_id))
    rows = cursor.fetchall()
    if not rows:
        cursor.execute("""INSERT INTO basket (user_id, product_id, count) 
                    VALUES (?, ?, ?)""", (user_id, product_id, 1))
    
    conn.commit()
    conn.close()
    

def remove_product_from_basket(user_id: int, product_id: int):
    """Функкция для удаления продукта из корзины"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM basket WHERE user_id = ? and product_id = ?", (user_id, product_id))
    rows = cursor.fetchall()
    
    conn.commit()
    conn.close()
    

def clear_basket(user_id: int):
    """Функция для очистки корзины пользователя"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM basket WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    
    conn.commit()
    conn.close()
    

def adding_one(user_id: int, product_id: int):
    """Функция для увеличения количества товара в корзине"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE basket SET count = count + 1 WHERE product_id = ? and user_id = ?",
                   (product_id, user_id))
    rows = cursor.fetchall()
    
    conn.commit()
    conn.close()
    


def subtraction_one(user_id: int, product_id: int):
    """Функция для уменьшения количества товара в корзине"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE basket SET count = count - 1 WHERE product_id = ? and user_id = ?",
                   (product_id, user_id))
    rows = cursor.fetchall()
    
    conn.commit()
    conn.close()


def get_admins():
    """Функция для получения списка id админов"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT admin_id FROM admins")
    rows = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    return [item[0] for item in rows]


def get_sellers():
    """Функция для получения списка id продавцов"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT seller_id FROM tokens")
    rows = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    return [item[0] for item in rows]


def add_token(admin_id: int, token: str):
    """Функция для добавления токена из ссылки-приглашения"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("""INSERT INTO tokens (admin_id, token, is_used) 
                   VALUES (?, ?, false)""", (admin_id, token))
    
    conn.commit()
    cursor.close()


def is_token_used(token: str):
    """Функция для проверки актуальности ссылки-приглашения"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT is_used FROM tokens WHERE token = ?", (token,))
    row = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    
    return row[0] if row is not None else True


def is_new_seller(seller_id):
    """Функция для проверки уникальности продавцов"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tokens WHERE seller_id = ?", (seller_id,))
    row = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    
    return row is None


def activate_token(seller_id: int, token: str):
    """Функция для активации ссылки-приглашения"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE tokens SET seller_id = ?, is_used = true WHERE token = ?",
        (seller_id, token)
    )
    
    conn.commit()
    cursor.close()


def add_order(user_id: int, date: datetime, time: str):
    """Функция для добавления заказа"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    user_basket = get_basket(user_id)
    if user_basket:
        descr = ""
        price = 0
        for i, x in enumerate(user_basket):
            product_id, count = x
            product = get_product(product_id)[0]
            descr += f"◽ {product[1]} - {count} шт.\n"
            price += product[-1]
        else:
            descr += f"\n<b>💰 Общая стоимость</b> - {price} рублей"

        cursor.execute("""INSERT INTO orders 
                       (order_descr, user_id, date, time, order_status)
                       VALUES (?, ?, ?, ?, "Ожидает проверки")""",
                       (descr, user_id, date, time))
        
    conn.commit()
    cursor.close()
    
    
def get_orders(user_id: int):
    """Функция для получения заказов пользователя"""
    
    conn = sqlite3.connect("PinCode.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM orders WHERE user_id = ?",
        (user_id,)
    )
    orders = cursor.fetchall()
    
    conn.commit()
    cursor.close()
    
    return orders
    
    
admins = get_admins()
sellers = get_sellers()