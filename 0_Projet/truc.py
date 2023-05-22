import copy


a = 10
b = a

b = 20
print(a)
print("TEST 1")
class A:
    def __init__(self):
        self.a = 10
    def set_a(self, a):
        self.a = a


a = A()
b = a
b.set_a(20)
print(a.a)
print("TEST 2")

lista = [1, 2, 3]
listb = copy.deepcopy(lista)
listb[0] = 10
print(lista)
print("TEST 3")