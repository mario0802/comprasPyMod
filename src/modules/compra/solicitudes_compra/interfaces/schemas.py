from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from src.modules.compra.solicitudes_compra.domain.entities import EstadoSolicitud


class CrearSolicitudCompraSchema(Schema):
    solicitante_id = fields.Integer(required=True, validate=validate.Range(min=1))
    descripcion = fields.String(required=False, allow_none=True, validate=validate.Length(max=2000))
    monto = fields.Decimal(required=False, allow_none=True, places=2, validate=validate.Range(min=0))


class ActualizarSolicitudCompraSchema(Schema):
    descripcion = fields.String(required=False, allow_none=True, validate=validate.Length(max=2000))
    monto = fields.Decimal(required=False, allow_none=True, places=2, validate=validate.Range(min=0))
    estado = fields.String(
        required=False,
        allow_none=True,
        validate=validate.OneOf(EstadoSolicitud.VALIDOS),
    )
    aprobado_por = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1))

    @validates_schema
    def validar_aprobado_por(self, data, **kwargs):
        estado = data.get("estado")
        if estado in (EstadoSolicitud.APROBADA, EstadoSolicitud.ANULADA):
            if not data.get("aprobado_por"):
                raise ValidationError(
                    "aprobado_por es obligatorio cuando el estado es APROBADA o ANULADA",
                    field_name="aprobado_por",
                )


class ListarSolicitudesCompraSchema(Schema):
    solicitante_id = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1))
    estado = fields.String(
        required=False,
        allow_none=True,
        validate=validate.OneOf(EstadoSolicitud.VALIDOS),
    )
    limit = fields.Integer(required=False, load_default=100, validate=validate.Range(min=1, max=500))
    offset = fields.Integer(required=False, load_default=0, validate=validate.Range(min=0))


class SolicitudCompraResponseSchema(Schema):
    id = fields.Integer()
    solicitante_id = fields.Integer()
    fecha_solicitud = fields.DateTime()
    descripcion = fields.String(allow_none=True)
    monto = fields.Decimal(allow_none=True, places=2, as_string=True)
    estado = fields.String()
    aprobado_por = fields.Integer(allow_none=True)
    fecha_aprobacion = fields.DateTime(allow_none=True)
    fecha_creacion = fields.DateTime()
    fecha_modificacion = fields.DateTime(allow_none=True)