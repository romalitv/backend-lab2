from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    user_id = fields.UUID(dump_only=True)
    user_name = fields.Str(required=True)

class CategorySchema(Schema):
    category_id = fields.UUID(dump_only=True)
    category_name = fields.Str(required=True)

class RecordSchema(Schema):
    record_id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    category_id = fields.UUID(required=True)
    time = fields.DateTime(dump_only=True)
    amount_of_money = fields.Float(required=True)