def thing(self, a, b):
    print(a, b)


class X:
    a = thing

x = X()
x.a('1', '2')