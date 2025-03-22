import sqlite3


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
    
    cursor.execute("SELECT * FROM basket WHERE product_id = ?", (product_id,))
    rows = cursor.fetchall()
    if not rows:
        cursor.execute("""INSERT INTO basket (user_id, product_id, count) 
                    VALUES (?, ?, ?)""", (user_id, product_id, 1))
    
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