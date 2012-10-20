from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from ratings.models import Category, Rating

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = "user"
        fields = ["username", "first_name", "last_name", "last_login"]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class CategoryResource(ModelResource):
    owner = fields.ForeignKey(UserResource, "owner")

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class RatingResource(ModelResource):
    rater = fields.ForeignKey(UserResource, "rater")
    category = fields.ForeignKey(CategoryResource, "category")

    class Meta:
        queryset = Rating.objects.all()
        resource_name = "rating"
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

