import graphene
from graphene_django.types import DjangoObjectType
from .models import Product
from datetime import datetime

# If you already have ProductType defined, skip this class
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'stock')

class UpdateLowStockProducts(graphene.Mutation):
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)

        message = f"{len(updated_products)} products restocked successfully at {datetime.now()}."
        return UpdateLowStockProducts(message=message, updated_products=updated_products)

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
