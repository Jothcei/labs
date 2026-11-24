import re


def binary(text):
    return re.fullmatch("[01]+", text) is not None


def find_binary(text):
    return re.findall(r"\b[01]+\b", text)


def main():

    value = input("Введите двоичное число: ")


    if binary(value):
        print("Это двоичное число.")

    else:
        print("Введите хотя бы одну цифру. Допустимы только 0 и 1.")


    path = input("Путь к файлу (Enter — ввести текст): ")


    if path:
        try:
            with open(path, "r", encoding="utf-8") as file:
                text = file.read()
        except (OSError, UnicodeError):
            print("Не удалось прочитать файл. Проверьте путь.")
            return

    else:
        text = input("Введите текст для поиска: ")


    print(find_binary(text))   

if __name__ == "__main__":
    main()
