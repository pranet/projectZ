class Result:
    def __init__(self, name, price, quantity, s_name, where):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.s_name = s_name
        self.where = where

    def __str__(self):
        name = self.name.replace("\n", " ")
        where = self.where.replace("\n", " ")
        return name + " " + str(self.price) + "z " + self.quantity + " unit(s) \"" + self.s_name + "\" " + where

    def __repr__(self):
        return self.__str__


class Query:
    def __init__(self, keyword, ignore, maximum_price):
        self.keyword = keyword
        self.ignore = ignore
        self.maximum_price = maximum_price
