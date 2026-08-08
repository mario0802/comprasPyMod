from marshmallow import Schema, fields, validate


class CreateUserSchema(Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=100))
    correo = fields.Email(required=True, validate=validate.Length(max=150))
    nick = fields.String(required=True, validate=validate.Length(min=3, max=50))
    password = fields.String(required=True, validate=validate.Length(min=8, max=128))

class UserResponseSchema(Schema):
    id = fields.Integer()
    nombre = fields.String()
    apellido = fields.String()
    correo = fields.String()
    nick = fields.String()
    fecha_creacion = fields.DateTime()
    fecha_modificacion = fields.DateTime(allow_none=True)

class LoginSchema(Schema):
    correo = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)