import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from graphql import GraphQLError
from decimal import Decimal



class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('customer_id', 'name', 'email', 'phone')




class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('product_id', 'name', 'price', 'stock')




class OrderType(DjangoObjectType):
    total_amount = graphene.Decimal()

    class Meta:
        model = Order
        fields = ('order_id', 'customer', 'products', 'total_amount')

    def resolve_total_amount(parent, info):
        return parent.total_amount




class CustomerInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()



class ProductInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(required=True, default_value=0)



class OrderInputType(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)




class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)
    customer_by_id = graphene.Field(CustomerType, customer_id=graphene.ID(required=True))
    product_by_id = graphene.Field(ProductType, product_id=graphene.ID(required=True))
    order_by_id = graphene.Field(OrderType, order_id=graphene.ID(required=True))


    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()

    def resolve_customer_by_id(root, info, customer_id):
        customer = Customer.objects.get(customer_id=customer_id)
        if not customer:
            raise GraphQLError('Invalid customer ID')
        return customer

    def resolve_product_by_id(root, info, product_id):
        product = Product.objects.get(product_id=product_id)
        if not product_id:
            raise GraphQLError('Invalid Product ID')
        return product

    def resolve_order_by_id(root, info, order_id):
        order = Order.objects.get(order_id=order_id)
        if not order:
            raise GraphQLError('Invalid Order ID')
        return order







class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInputType(required=True)
    
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input):
        name = input.name
        email = input.email
        phone = input.phone

        if Customer.objects.filter(email=email).exists():
            raise GraphQLError(f'The email {email} is already been used by another customer')

        customer = Customer(
                name = name,
                email = email,
                phone = phone
                )
        customer.save()
        return CreateCustomer(customer=customer, message='Customer created successfully')




class BulkCreateCustomer(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInputType, required=True)

    customers = graphene.List(CustomerType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input):
        
        customers = []
        for obj in input:
            name = obj.name
            email = obj.email
            phone = obj.phone
            if Customer.objects.filter(email=email).exists():
                raise GraphQLError(f'The email {email} is already been used by another customer')
            customer = Customer(
                    name = name,
                    email = email,
                    phone = phone
                    )
            customer.save()
            customers.append(customer)
        return BulkCreateCustomer(customers=customers, message='Customers created successfully')




class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInputType(required=True)

    product = graphene.Field(ProductType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input):
        
        name = input.name
        price = input.price
        stock = input.stock

        if stock is not None and stock < 0:
            raise GraphQLError('The stock can not be a negative number')

        if price is None or price < 0:
            raise GraphQLError('Price must be a positive value')

        product = Product(
                name = name,
                price = price,
                stock = stock
                )
        product.save()
        return CreateProduct(product=product, message='Product created successfully')




class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInputType(required=True)

    order = graphene.Field(OrderType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input):
        
        customer_id = input.customer_id
        product_ids = input.product_ids

        customer = Customer.objects.get(customer_id=customer_id)
        if not customer:
            raise GraphQLError('Invalid customer ID')

        products = Product.objects.filter(product_id__in=product_ids)
        valid_ids = set()
        for product in products:
            valid_ids.add(str(product.product_id))

        if set(product_ids) != valid_ids:
            raise GraphQLError('One or more product IDs are invalid')

        order = Order(customer = customer)
        order.save()

        order.products.set(products)
        order.save()

        return CreateOrder(order=order, message='Order created successfully')




class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customer = BulkCreateCustomer.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


