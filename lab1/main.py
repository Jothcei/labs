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

class CatalogError(Exception):
    pass

class Catalog:
    def __init__(self):
        self.products = {}

    def add(self, product):
        self.products[product.sku] = product

    def get(self, sku: str) -> Product:
        if sku not in self.products:
            raise CatalogError(f"Товар с артикулом {sku} не найден.")
        return self.products[sku]        
        
try:
    product = Product("M-01", "Mouse", 1500, 5)
    catalog = Catalog()
    catalog.add(product)

    print(catalog.get("M-01").name)

except (ValueError, CatalogError) as error:
    print(error)