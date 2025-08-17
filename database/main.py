from db_connect import get_connection

# --- LOGIN FUNCTION ---
def login(username, password):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    db.close()
    if user:
        print(f"✅ Login successful! Welcome {user['username']} ({user['role']})")
        return user
    else:
        print("❌ Invalid username or password")
        return None


# --- SHOW PRODUCTS ---
def show_products():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    db.close()
    print("\n📦 Available Products:")
    for p in products:
        print(f"{p['product_id']}: {p['name']} - ${p['price']} (Stock: {p['stock']})")


# --- VIEW CART ---
def view_cart(user_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT p.name, c.quantity, p.price, (c.quantity * p.price) AS total
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()
    db.close()

    print("\n🛒 Your Cart:")
    total = 0
    for item in cart_items:
        print(f"{item['name']} x {item['quantity']} = ${item['total']}")
        total += item['total']
    print(f"Total = ${total}")


# --- PLACE ORDER ---
def place_order(user_id):
    db = get_connection()
    cursor = db.cursor()

    # Get cart items
    cursor.execute("""
        SELECT product_id, quantity, p.price
        FROM cart c JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """, (user_id,))
    items = cursor.fetchall()

    if not items:
        print("❌ Cart is empty!")
        db.close()
        return

    # Calculate total
    total = sum(qty * price for (_, qty, price) in items)

    # Insert order
    cursor.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s)", (user_id, total))
    order_id = cursor.lastrowid

    # Insert order items
    for (product_id, qty, price) in items:
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (order_id, product_id, qty, price)
        )

    # Clear cart
    cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
    db.commit()
    db.close()

    print(f"✅ Order #{order_id} placed successfully! Total = ${total}")


# --- DEMO RUN ---
if __name__ == "__main__":
    user = login("alice", "pass123")
    if user:
        show_products()
        view_cart(user["user_id"])
        place_order(user["user_id"])
