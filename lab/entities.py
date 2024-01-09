from marshmallow import Schema, fields, validates, ValidationError


class UserSchema(Schema):
    user_id = fields.UUID(dump_only=True)
    user_name = fields.Str(required=True)

class CategorySchema(Schema):
    category_id = fields.UUID(dump_only=True)
    category_name = fields.Str(required=True)
    is_common = fields.Boolean(required=True, default=False)

class RecordSchema(Schema):
    record_id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    category_id = fields.UUID(required=True)
    time = fields.DateTime(dump_only=True)
    amount_of_money = fields.Float(required=True)

    @validates('category_id')
    def validate_category_id(self, value):
        category = CategorySchema.query.get(value)
        if category is None:
            raise ValidationError("Invalid category_id")
        if not category.is_common and category.user_id != self.context.get('user_id'):
            raise ValidationError("User does not have access to this category")