from model.product import Product


# data set with all valid products
valid_products = [[],  # No elements
                  [Product('popular', 'Blue Duck', 1)],  # single product
                  [Product('popular', 'Blue Duck', 2),  # multiple products
                   Product('popular', 'Red Duck', 3),
                   Product('campaigns', 'Yellow Duck', 1, 'Small')]
                  ]

# data set with partially valid products
partially_invalid_products = [[Product('popular', 'Blue Duck', 1)],  # single VALID product
                              [Product('popular', 'Blue Duck not exists', 2),  # multiple not exist products
                               Product('popular', 'Red Duck not exists', 3),
                               Product('campaigns', 'Yellow Duck not exists', 1, 'Small')]
                              ]


# data set with all invalid/not exists products
invalid_products = [[Product('popular', 'Blue Duck not exists', 1)],  # single NOT EXISTS product
                    [Product('popular', 'Blue Duck not exists', 2),  # multiple NOT EXISTS products
                    Product('popular', 'Red Duck not exists', 3),
                    Product('campaigns', 'Yellow Duck not exists', 1, 'Small')]
                    ]
