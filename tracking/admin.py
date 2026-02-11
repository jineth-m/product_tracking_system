from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin



from .models import (
    Product,
    SubPart,
    ProductSubPart,
    SubPartType,
    Status,
    SubPartStatusHistory,
    ProductMainType,
    ProductRange
)

# =====================================================
# PRODUCT MAIN TYPE (Local / Export)
# =====================================================
@admin.register(ProductMainType)
class ProductMainTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


# =====================================================
# PRODUCT RANGE
# =====================================================
@admin.register(ProductRange)
class ProductRangeAdmin(admin.ModelAdmin):
    list_display = ("name", "main_type")
    list_filter = ("main_type",)
    search_fields = ("name",)


# =====================================================
# PRODUCT RESOURCE
# =====================================================
class ProductResource(resources.ModelResource):
    product_range = fields.Field(
        column_name="product_range",
        attribute="product_range",
        widget=ForeignKeyWidget(ProductRange, "name")
    )

    class Meta:
        model = Product
        fields = ("product_code", "product_name", "product_range")
        import_id_fields = ("product_code",)
        skip_unchanged = True
        report_skipped = True


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ("product_code", "product_name", "product_range", "created_at")
    search_fields = ("product_code", "product_name")
    list_filter = ("product_range",)


# =====================================================
# SUB PART RESOURCE
# =====================================================
class ProductResource(resources.ModelResource):
    product_range = fields.Field(
        column_name="product_range",
        attribute="product_range",
        widget=ForeignKeyWidget(ProductRange, "id")   # ← change here
    )

    class Meta:
        model = Product
        fields = ("product_code", "product_name", "product_range")
        import_id_fields = ("product_code",)
        skip_unchanged = True
        report_skipped = True


# =====================================================
# SUB PART RESOURCE
# =====================================================
class SubPartResource(resources.ModelResource):
    sub_part_type = fields.Field(
        column_name="sub_part_type",
        attribute="sub_part_type",
        widget=ForeignKeyWidget(SubPartType, "name")
    )

    class Meta:
        model = SubPart
        fields = ("sub_part_code", "sub_part_name", "sub_part_type")
        import_id_fields = ("sub_part_code",)
        skip_unchanged = True
        report_skipped = True


@admin.register(SubPart)
class SubPartAdmin(ImportExportModelAdmin):
    resource_class = SubPartResource
    list_display = ("sub_part_code", "sub_part_name", "sub_part_type")
    search_fields = ("sub_part_code", "sub_part_name")
    list_filter = ("sub_part_type",)





# =====================================================
# PRODUCT SUB PART RESOURCE
# =====================================================
class ProductSubPartResource(resources.ModelResource):
    product = fields.Field(
        column_name="product",
        attribute="product",
        widget=ForeignKeyWidget(Product, "product_code")
    )
    sub_part = fields.Field(
        column_name="sub_part",
        attribute="sub_part",
        widget=ForeignKeyWidget(SubPart, "sub_part_code")
    )
    current_status = fields.Field(
        column_name="current_status",
        attribute="current_status",
        widget=ForeignKeyWidget(Status, "name")
    )

    class Meta:
        model = ProductSubPart
        fields = ("product", "sub_part", "current_status", "comment")
        import_id_fields = ("product", "sub_part")
        skip_unchanged = True
        report_skipped = True


@admin.register(ProductSubPart)
class ProductSubPartAdmin(ImportExportModelAdmin):
    resource_class = ProductSubPartResource
    list_display = (
        "product",
        "sub_part",
        "current_status",
        "updated_by",
        "updated_at",
    )
    list_filter = ("current_status",)
    search_fields = (
        "product__product_code",
        "sub_part__sub_part_code",
        "sub_part__sub_part_name",
    )


# =====================================================
# LOOKUP TABLES (NO IMPORT)
# =====================================================
@admin.register(SubPartType)
class SubPartTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)


# =====================================================
# STATUS HISTORY (READ ONLY)
# =====================================================
@admin.register(SubPartStatusHistory)
class SubPartStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "sub_part",
        "old_status",
        "new_status",
        "comment",
        "changed_by",
        "changed_at",
    )
    list_filter = ("old_status", "new_status", "changed_by")
    search_fields = (
        "sub_part__sub_part_code",
        "sub_part__sub_part_name",
        "comment",
    )
    ordering = ("-changed_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

