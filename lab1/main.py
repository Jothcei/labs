class Product:
    def __init__(self, sku, name, price, stock):
        if price <= 0:
            raise ValueError("Цена товара должна быть больше нуля.")
        
        if stock < 0:
            raise ValueError("Остаток товара не может быть отрицательным.")    
        
        self.sku = sku
        self.name = name
        self.price = price
        self.stock = stock

try:
    product = Product("M-01", "Mouse", 1500, 5)

except ValueError as error:
    print(error)

else:
    print(product.name, product.price)