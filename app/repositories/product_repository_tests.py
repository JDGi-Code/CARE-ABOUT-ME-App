import pytest

from app.repositories.product_repository import ProductRepository
from app.models import Product
from app.dto import Product as ProductDTO


# Verify that get_by_id returns the correct object matching the id, in the correct format
@pytest.mark.django_db
def test_get_by_id():
    # 1. Setup
    p = Product(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    p.save()
    # 2. Execute
    result = ProductRepository.get_by_id(id=p.id)
    # 3. Assert
    assert p.id == result.id
    assert p.name == result.name
    assert p.description == result.description
    assert p.brand == result.brand


# Verify all products were retrieved
@pytest.mark.django_db
def test_get_all():
    # 1. Setup
    Product(name='Mock1', description='Mock1Desc', brand='Mock1Brand').save()
    Product(name='Mock2', description='Mock2Desc', brand='Mock2Brand').save()
    # 2. Execute
    result = ProductRepository.get_all()
    # 3. Assert
    assert result[0].name == 'Mock1'
    assert result[1].name == 'Mock2'
    assert len(result) == 2


# Verify objects are created
@pytest.mark.django_db
def test_create():
    # 1. Setup
    new_product = ProductDTO(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    # 2. Execute
    new_product = ProductRepository.create_or_update(new_product)
    # 3. Assert
    assert new_product.id is not None
    assert Product.objects.get(id=new_product.id).name == 'Mock1'


# Verify objects are updated
@pytest.mark.django_db
def test_update():
    # 1. Setup
    new_product = ProductDTO(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    new_product = ProductRepository.create_or_update(new_product)
    old_id = new_product.id
    new_product.name = 'Mock2'
    # 2. Execute
    new_product = ProductRepository.create_or_update(new_product)
    # 3. Assert
    assert new_product.id == old_id
    assert Product.objects.get(id=new_product.id).name == 'Mock2'


# Verify objects are soft-deleted
@pytest.mark.django_db
def test_soft_delete():
    # 1. Setup
    new_product = ProductDTO(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    new_product = ProductRepository.create_or_update(new_product)
    # 2. Execute
    ProductRepository.delete(new_product)
    # 3. Assert
    with pytest.raises(Product.DoesNotExist):
        Product.objects.get(id=new_product.id)                          # filtered queryset
    assert Product.all_objects.get(id=new_product.id) is not None       # unfiltered queryset


# Verify objects are hard-deleted
@pytest.mark.django_db
def test_hard_delete():
    # 1. Setup
    new_product = ProductDTO(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    new_product = ProductRepository.create_or_update(new_product)
    # 2. Execute
    ProductRepository.delete(new_product, hard=True)
    # 3. Assert
    # filtered queryset
    with pytest.raises(Product.DoesNotExist):
        Product.objects.get(id=new_product.id)
    # unfiltered queryset
    with pytest.raises(Product.DoesNotExist):
        assert Product.all_objects.get(id=new_product.id)