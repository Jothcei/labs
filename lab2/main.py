import re

def binary(text):

    return re.fullmatch("[01]+", text) is not None

value = input("Введите двоичное число: ")

if binary(value):

    print("Это двоичное число.")

else:
    
    print("Введите хотя бы одну цифру. Допустимы только 0 и 1.")