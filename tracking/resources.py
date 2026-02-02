from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Product, SubPart, ProductSubPart, SubPartType, Status


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'product_code', 'product_name')
        import_id_fields = ('product_code',)


class SubPartResource(resources.ModelResource):
    sub_part_type = fields.Field(
        column_name='sub_part_type',
        attribute='sub_part_type',
        widget=ForeignKeyWidget(SubPartType, 'name')
    )

    class Meta:
        model = SubPart
        fields = ('id', 'sub_part_code', 'sub_part_name', 'sub_part_type')
        import_id_fields = ('sub_part_code',)


class ProductSubPartResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'product_code')
    )

    sub_part = fields.Field(
        column_name='sub_part',
        attribute='sub_part',
        widget=ForeignKeyWidget(SubPart, 'sub_part_code')
    )

    current_status = fields.Field(
        column_name='current_status',
        attribute='current_status',
        widget=ForeignKeyWidget(Status, 'name')
    )

    class Meta:
        model = ProductSubPart
        fields = ('id', 'product', 'sub_part', 'current_status')
        import_id_fields = ('product', 'sub_part')

    def before_import_row(self, row, **kwargs):
        """
        Automatically assign default status if missing
        """
        if not row.get('current_status'):
            default_status = Status.objects.get(name='Not Started')
            row['current_status'] = default_status.name