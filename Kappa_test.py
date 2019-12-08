#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Boss:

    def __init__(self, money, product, emplyList):
        self.money = money
        self.product = product
        self.emplyList = emplyList

    def addEmploy(self):
        self.emplyList.append(Employee())
        print("增加了一个员工")

    def addEmploy(self, count):
        self.money += count * 10
        print("卖了 " + str(count) + " 个商品,共得金钱:" + count * 10)


class Employee:

    def __init__(self, proficiency):
        self.proficiency = proficiency      #熟练度,每年增加50

    def work(self):
        print("该员工每个月生产 " + str(self.proficiency) + " 个商品,老板付薪2k")


print("1942001414309"[-3:])

o={"1":"111"}
for i in o.items():
    print(i[0],i[1])
list = [1,2,3,4,5]
print(list[1:])


#
# x = "h"
#
# print("1xn".encode("utf-8"))


#递归函数得到老板手上的钱
def getMoney(boss,year):
    money = boss.money
    emply_list = boss.emplyList
    product = boss.product
