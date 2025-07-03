import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from graphql import GraphQLError

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('customer_id', 'name', 'email', 'phone')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('product_id', 'name', 'price', 'stock')


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ('order_id', 'customer_id', 'product_id')


class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()



class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()
    
    customer = graphene.Field(CustomerType)
    success = graphene.String()

    @classmethod
    def mutate(cls, root, info, name, email, phone):

        if Customer.objects.filter(email=email).exists():
            raise GraphQLError('The email is already been used by another customer')

        customer = Customer(
                name = name,
                email = email,
                phone = phone
                )
        customer.save()
        return CreateCustomer(customer=customer, success='Customer created successfully')




class BulkCreateCustomer():
    pass

class CreateProduct():
    pass

class CreateOrder():
    pass



class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()







