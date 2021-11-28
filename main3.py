# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import typing
from datetime import date
import math

class Person:
    """this is the person class"""
    name = 'gukt'
    r = None
    i = None

    def __init__(self, realpart = 3.0, imagpart = -4.5):
        self.data = []
        self.r = realpart
        self.i = imagpart

    def m1(self):
        """this is the doc"""
        print('I am a method1')
        self.m2()

    def m2(self):
        print('m2')


class Student(Person):
    """this is the clss person"""
    def m3(self):
        Person.m1(self)


def class_test():

    s1 = Student()
    s1.m1()
    s1.m3()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

    if True:
        class Student:
            name = 'foo'

    p1 = Person(1.0, 20.0)
    print(p1, p1.name)
    p1.m1()
    del p1.data
    print(p1.data)
    print('aaa')

    # s1 = Student()
    # print(s1.name)

    # b = typing.Union[int, str, int] == typing.Union[int, str] == (int | str)
    # print(b)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    class_test()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
