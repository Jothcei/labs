import re
value = input("Введите двоичное число: ")

match = re.fullmatch("[01]+", value)

if match is None:
    print("Введите хотя бы одну цифру. Допустимы только 0 и 1.")

else:
    print("Это двоичное число.")