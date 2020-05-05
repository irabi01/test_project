from decimal import Decimal
from django.conf import settings
from cart_app.models import Product

class Tray(object):
    def __init__(self,request):
        self.session = request.session
        tray = self.session

        if not tray:
            tray ={}
        self.tray=tray

    def add(self, product, quantity = 1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.tray:
            self.tray[product_id]={'quantity':0,'price':str(product.price)}


        if update_quantity:
            self.tray[product_id]['quantity'] = quantity
            
        else:
            self.tray[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.tray:
            del self.tray[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.tray.keys()
        products = Product.objects.filter(id__in = product_ids)
       

        for product in products:
            self.tray[str(product.id)]['product']=product

        for item in self.tray.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']*item['quantity']
            yield item
        return self.tray

    def __len__ (self):
        return sum(item['quantity'] for item in self.tray.values())

    def get_total_price(self):
        return sum(Decimal(item['price'])*Decimal(item['quantity']) for item in self.tray.values())

    #this function is for cleanin the shopping cart
    def clear(self):
        del self.session
        self.save()
        
        

    
    
