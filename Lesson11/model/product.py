class Product(object):
    def __init__(self, category=None, name=None, amount=None, size=None):
        self.category = category
        self.name = name
        self.amount = 1 if amount is None else amount
        self.size = 'Small' if size is None else size

    # repr(object): Return a string containing a printable representation of an object.
    # this method allows to see in console test's params
    def __repr__(self):
        return 'Category: {category} name: {name} amount: {amount} size: {size}'.format(category=self.category,
                                                                                        name=self.name,
                                                                                        amount=self.amount,
                                                                                        size=self.size)
