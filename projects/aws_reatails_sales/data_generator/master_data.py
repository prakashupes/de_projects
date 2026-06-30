import random

# ===========================
# Categories
# ===========================

CATEGORIES = {
    "Electronics": (10000, 90000),
    "Fashion": (500, 5000),
    "Grocery": (20, 500),
    "Home": (500, 10000),
    "Sports": (300, 15000)
}

# ===========================
# Products
# ===========================

PRODUCTS = [
    ("P0001", "iPhone 16", "Electronics"),
    ("P0002", "Samsung TV", "Electronics"),
    ("P0003", "Laptop", "Electronics"),
    ("P0004", "Men T-Shirt", "Fashion"),
    ("P0005", "Women's Jeans", "Fashion"),
    ("P0006", "Rice Bag", "Grocery"),
    ("P0007", "Milk", "Grocery"),
    ("P0008", "Dining Table", "Home"),
    ("P0009", "Office Chair", "Home"),
    ("P0010", "Cricket Bat", "Sports"),
]

# ===========================
# Stores
# ===========================

STORES = [
    ("ST001", "Delhi", "Delhi"),
    ("ST002", "Mumbai", "Maharashtra"),
    ("ST003", "Bengaluru", "Karnataka"),
    ("ST004", "Hyderabad", "Telangana"),
    ("ST005", "Chennai", "Tamil Nadu"),
    ("ST006", "Pune", "Maharashtra"),
    ("ST007", "Kolkata", "West Bengal"),
    ("ST008", "Ahmedabad", "Gujarat"),
    ("ST009", "Jaipur", "Rajasthan"),
    ("ST010", "Lucknow", "Uttar Pradesh"),
]

# ===========================
# Payment Modes
# ===========================

PAYMENT_MODES = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Net Banking"
]

# ===========================
# Discount Options
# ===========================

DISCOUNTS = [0, 5, 10, 15, 20]

# ===========================
# Helper Functions
# ===========================

def get_random_product():
    return random.choice(PRODUCTS)


def get_random_store():
    return random.choice(STORES)


def get_random_payment_mode():
    return random.choice(PAYMENT_MODES)


def get_random_discount():
    return random.choice(DISCOUNTS)


def get_price(category):
    low, high = CATEGORIES[category]
    return random.randint(low, high)