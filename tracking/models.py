from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# MASTER DATA
# -----------------------------

class SubPartType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# -----------------------------
# CORE ENTITIES
# -----------------------------

class Product(models.Model):
    product_code = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    product_range = models.ForeignKey(
        ProductRange,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )


    def __str__(self):
        return f"{self.product_code} - {self.product_name}"


class SubPart(models.Model):
    sub_part_code = models.CharField(max_length=50, unique=True)
    sub_part_name = models.CharField(max_length=200)
    sub_part_type = models.ForeignKey(SubPartType, on_delete=models.PROTECT)

    # default status for sub parts not linked to products
    default_status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="default_subpart_status"
    )
    default_comment = models.TextField(blank=True)
    default_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_subpart_user"
    )
    default_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.sub_part_code} - {self.sub_part_name}"


# -----------------------------
# RELATION: PRODUCT ↔ SUB PART
# -----------------------------

class ProductSubPart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sub_part = models.ForeignKey(SubPart, on_delete=models.CASCADE)
    current_status = models.ForeignKey(Status, on_delete=models.PROTECT)
    comment = models.TextField(blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "sub_part")

    def update_status_and_comment(self, status_id, user, comment=""):
        old_status = self.current_status
        old_comment = self.comment or ""

        # determine new status
        if status_id:
            new_status = Status.objects.get(id=status_id)
        else:
            new_status = old_status

        # 🔴 critical fix: prevent NULL old_status
        if old_status is None:
            old_status = new_status

        status_changed = old_status != new_status
        comment_changed = old_comment != (comment or "")

        if not status_changed and not comment_changed:
            return

        self.current_status = new_status
        self.comment = comment
        self.updated_by = user
        self.save()

        SubPartStatusHistory.objects.create(
            sub_part=self.sub_part,
            old_status=old_status,
            new_status=new_status,
            comment=comment,
            changed_by=user,
        )

    def __str__(self):
        return f"{self.product} | {self.sub_part}"


# -----------------------------
# AUDIT TRAIL (SUB PART LEVEL)
# -----------------------------

class SubPartStatusHistory(models.Model):
    sub_part = models.ForeignKey(SubPart, on_delete=models.CASCADE)
    old_status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name="old_status_history"
    )
    new_status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name="new_status_history"
    )
    comment = models.TextField(blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sub_part} ({self.old_status} → {self.new_status})"

# -----------------------------
# PRODUCT TYPE STRUCTURE
# -----------------------------

class ProductMainType(models.Model):
    """
    Example:
    - Local
    - Export
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductRange(models.Model):
    """
    Example:
    Local → Range A
    Local → Range B
    Export → Range X
    """
    main_type = models.ForeignKey(
        ProductMainType,
        on_delete=models.CASCADE,
        related_name="ranges"
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("main_type", "name")

    def __str__(self):
        return f"{self.main_type} / {self.name}"
