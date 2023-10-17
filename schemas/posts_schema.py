from app import ma
from marshmallow import fields
from models import Post, Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post

    category = fields.Nested(CategorySchema)
