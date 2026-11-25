import json
import xml.etree.ElementTree as ET


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


class Order:
    def __init__(self, number: int, cart: Cart) -> None:
        if not cart.items:
            raise ValueError("Корзина не может быть пустой.")

        self.number = number
        self.items = []
        for item in cart.items.values():
            self.items.append({
                "sku": item.product.sku,
                "name": item.product.name,
                "price": item.product.price,
                "quantity": item.quantity,
            })
        self.total = cart.total()

        
def checkout(catalog: Catalog, cart: Cart, number: int) -> Order:
    checked_cart = Cart()
    for item in cart.items.values():
        product = catalog.get(item.product.sku)
        checked_cart.set_quantity(product, item.quantity)

    order = Order(number, checked_cart)

    for item in checked_cart.items.values():
        item.product.stock -= item.quantity

    cart.items.clear()
    return order


def catalog_to_data(catalog: Catalog) -> list[dict]:
    rows = []
    for product in catalog.products.values():
        rows.append({
            "sku": product.sku,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
        })
    return rows


def save_json(catalog: Catalog, path: str) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(catalog_to_data(catalog), file, ensure_ascii=False, indent=2)


def catalog_from_data(rows: list[dict]) -> Catalog:
    if not isinstance(rows, list):
        raise ValueError("В файле должен быть список товаров.")

    catalog = Catalog()
    for row in rows:
        product = Product(row["sku"], row["name"], row["price"], row["stock"])
        catalog.add(product)
    return catalog


def load_json(path: str) -> Catalog:
    with open(path, "r", encoding="utf-8") as file:
        rows = json.load(file)
    return catalog_from_data(rows)


def save_xml(catalog: Catalog, path: str) -> None:
    root = ET.Element("catalog")
    for row in catalog_to_data(catalog):
        ET.SubElement(root, "product", {
            "sku": row["sku"],
            "name": row["name"],
            "price": str(row["price"]),
            "stock": str(row["stock"]),
        })

    ET.indent(root, space="  ")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def load_xml(path: str) -> Catalog:
    root = ET.parse(path).getroot()
    if root.tag != "catalog":
        raise ValueError("В XML ожидается корневой элемент catalog.")

    rows = []
    for element in root:
        if element.tag != "product":
            raise ValueError("В каталоге ожидаются элементы product.")
        rows.append({
            "sku": element.attrib["sku"],
            "name": element.attrib["name"],
            "price": int(element.attrib["price"]),
            "stock": int(element.attrib["stock"]),
        })
    return catalog_from_data(rows)


try:
    product = Product("M-01", "Mouse", 1500, 5)
    catalog = Catalog()
    catalog.add(product)

    catalog.update(Product("M-01", "Mouse", 1700, 5))
    print(catalog.get("M-01").price)

    cart = Cart()
    cart.set_quantity(catalog.get("M-01"), 2)
    print(cart.total())

    order = checkout(catalog, cart, 1)
    print("Заказ", order.number, "на сумму", order.total, "руб.")  

    print("Остаток на складе:", catalog.get("M-01").stock)
    print("Позиций в корзине:", len(cart.items))  

    save_json(catalog, "lab1/catalog.json")    

    loaded_catalog = load_json("lab1/catalog.json")
    loaded_product = loaded_catalog.get("M-01")
    print("Из JSON:", loaded_product.name, loaded_product.price, loaded_product.stock)


    save_xml(catalog, "lab1/catalog.xml")
    xml_catalog = load_xml("lab1/catalog.xml")
    xml_product = xml_catalog.get("M-01")
    print("Из XML:", xml_product.name, xml_product.price, xml_product.stock)


except (ValueError, CatalogError, OSError, KeyError, TypeError, ET.ParseError) as error:
    print(error)