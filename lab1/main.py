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


def read_product(sku: str) -> Product:
    name = input("Название: ").strip()
    price = int(input("Цена в рублях: "))
    stock = int(input("Остаток в штуках: "))
    return Product(sku, name, price, stock)


def main() -> None:
    catalog = Catalog()

    cart = Cart()
    orders: list[Order] = []

    while True:
        print("\n1 — Каталог | 2 — Добавить | 3 — Изменить | 4 — Удалить | 0 — Выход")
        print("5 — Указать количество | 6 — Корзина | 7 — Оформить заказ")
        print("8 — Сохранить каталог | 9 — Загрузить каталог")
        
        choice = input("Команда: ").strip()

        try:
            if choice == "0":
                break

            elif choice == "1":
                if not catalog.products:
                    print("Каталог пуст.")
                for product in catalog.products.values():
                    print(product.sku, product.name, product.price, product.stock)

            elif choice == "2":
                sku = input("Артикул: ").strip()
                catalog.add(read_product(sku))
                print("Товар добавлен.")

            elif choice == "3":
                sku = input("Артикул: ").strip()
                catalog.update(read_product(sku))
                print("Товар изменён.")

            elif choice == "4":
                sku = input("Артикул: ").strip()
                catalog.remove(sku)
                print("Товар удалён.")

            elif choice == "5":
                sku = input("Артикул: ").strip()
                product = catalog.get(sku)
                quantity = int(input("Количество: "))
                cart.set_quantity(product, quantity)
                print("Количество в корзине обновлено.")

            elif choice == "6":
                if not cart.items:
                    print("Корзина пуста.")
                for item in cart.items.values():
                    print(item.product.name, item.quantity, item.subtotal())
                print("Итого:", cart.total(), "руб.")

            elif choice == "7":
                order = checkout(catalog, cart, len(orders) + 1)
                orders.append(order)
                print(f"Заказ №{order.number} оформлен. Сумма {order.total} руб.")

            elif choice in ("8", "9"):
                path = input("Путь к файлу (.json или .xml): ").strip()
                extension_path = path.lower()

                if extension_path.endswith(".json"):
                    save_catalog, load_catalog = save_json, load_json
                elif extension_path.endswith(".xml"):
                    save_catalog, load_catalog = save_xml, load_xml
                else:
                    raise ValueError("Укажите файл с расширением .json или .xml.")

                if choice == "8":
                    save_catalog(catalog, path)
                    print("Каталог сохранён.")
                else:
                    catalog = load_catalog(path)
                    cart.items.clear()
                    print("Каталог загружен. Корзина очищена.")

                    
            else:
                print("Неизвестная команда.")
        except (ValueError, CatalogError, OSError, KeyError, TypeError, ET.ParseError) as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()

