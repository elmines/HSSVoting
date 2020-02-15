#!/usr/bin/python3

from algebra import *

x = ModularInt(25, 7)
print(x)
x *= 7
print(x)
x += 3
print(x)
x = x * 3
print(x)


g = ModularInt(3, 17)
y = g ** 6
print(f"g={g}, y={y}, log_g(y)={discrete_log(g, y)}")
