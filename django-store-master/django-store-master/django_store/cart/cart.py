from decimal import Decimal
from django.conf import settings
from store.models import Product

class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
                مقداردهی اولیه به سبد خرید.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            # صرفه جویی در یک سبد خرید خالی در جلسه
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
         اضافه کردن یک محصول به سبد خرید یا به روز رسانی مقدار آن است.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                        'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        # به روز رسانی سبد خرید جلسه
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        # علامت جلسه را به عنوان "اصلاح شده" مطمئن شوید آن ذخیره شده است
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
         حذف یک محصول از سبد خرید.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
         تکرار بیش از اقلام در سبد خرید و دریافت محصولات از پایگاه داده.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        # گرفتن اشیاء محصول و به سبد خرید اضافه کردن آنها
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        تعداد تمام اقلام در سبد خرید.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
            self.cart.values())

    def clear(self):
        # remove cart from session
        # حذف سبد خرید را از جلسه
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
