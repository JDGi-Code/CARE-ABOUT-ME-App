from app.models import Product
from app.dto import Product as ProductDTO
from typing import List


class ProductRepository():
    @classmethod
    def get_by_id(cls, id: int) -> ProductDTO:
        return Product.objects.get(id=id).to_dto()

    # iterate over all products and build a list of dtos
    @classmethod
    def get_all(cls) -> List[ProductDTO]:
        all_products = Product.objects.all()
        return [x.to_dto() for x in all_products]

    # if existing product, update; if new product, save
    @classmethod
    def create_or_update(cls, product: ProductDTO) -> ProductDTO:
        if product.id:                      # if a product has an ID
            p = Product.objects.get(id=product.id)                    # retrieve product from db
        else:
            p = Product()
        p.name = product.name
        p.description = product.description
        p.brand = product.brand
        p.save()
        return p.to_dto()

    @classmethod
    def delete(cls, product: ProductDTO, hard=False) -> bool:
        p = Product.objects.get(id=product.id)
        if hard:
            return p.hard_delete()
        else:
            return p.delete()
