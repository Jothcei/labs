class Product:
    def __init__(self, sku, name, price, stock):
        self.sku = sku
        self.name = name
        self.price = price
        self.stock = stock  

product = Product("M-01", "Mouse", 1500, 5)

print(product.name, product.price)