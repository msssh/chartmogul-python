from marshmallow import Schema, fields, post_load
from ..resource import Resource, DataObject, _add_method
from .customer import Customer
from collections import namedtuple


class Tags(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#customer-attributes
    """
    _path = "/customers{/uuid}/attributes/tags"

    class _Schema(Schema):
        tags = fields.List(fields.String())

        @post_load
        def make(self, data):
            return Tags(**data)

    _customers = namedtuple('Customers', ['entries'])
    _schema = _Schema(strict=True)

    @classmethod
    def _load(cls, response):
        """
        Workaround: when using email, the return value is actually
        a list of customers, but without paging.
        """
        response.raise_for_status()
        if response.status_code == 204:
            return None
        jsonObj = response.json()
        if 'entries' in jsonObj:
            return _customers(Customer._schema.load(jsonObj['entries']))
        else:
            return cls._schema._load(response)