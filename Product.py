class Product:
    def __init__(self, name, minPrice, maxPrice, rating, sales, link):
        self.name = name
        self.minPrice = minPrice
        self.maxPrice = maxPrice
        self.rating = rating
        self.sales = sales
        self.link = link
    def __str__(self): # to string method
        return f'{self.name}\t{self.minPrice}\t{self.maxPrice}\t{"%.1f"%self.rating},{self.sales}\t{self.link}'
    def __iter__(self): # for export to csv file
        return iter([self.name, self.minPrice, self.maxPrice, "%.1f"%self.rating, self.sales, self.link])

