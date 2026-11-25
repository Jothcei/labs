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
        if product.sku in self.products:
            raise CatalogError(f"Артикул {product.sku} уже есть в каталоге.")
        self.products[product.sku] = product

    def get(self, sku: str) -> Product:
        if sku not in self.products:
            raise CatalogError(f"Товар с артикулом {sku} не найден.")
        return self.products[sku]        
    
    def update(self, product: Product) -> None:
        self.get(product.sku)
        self.products[product.sku] = product

    def remove(self, sku: str) -> None:
        self.get(sku)
        del self.products[sku]

class CartItem:
    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля.")
        self.product = product
        self.quantity = quantity

    def subtotal(self) -> int:
        return self.product.price * self.quantity
 
class Cart:
    def __init__(self) -> None:
        self.items: dict[str, CartItem] = {}

    def set_quantity(self, product: Product, quantity: int) -> None:
        item = CartItem(product, quantity)
        if quantity > product.stock:
            raise ValueError("На складе недостаточно товара.")
        self.items[product.sku] = item

    def total(self) -> int:
        total = 0
        for item in self.items.values():
            total += item.subtotal()
        return total    

    
try:
    product = Product("M-01", "Mouse", 1500, 5)
    catalog = Catalog()
    catalog.add(product)

    catalog.update(Product("M-01", "Mouse", 1700, 5))
    print(catalog.get("M-01").price)

    cart = Cart()
    cart.set_quantity(catalog.get("M-01"), 6)
    print(cart.total())

except (ValueError, CatalogError) as error:
    print(error)