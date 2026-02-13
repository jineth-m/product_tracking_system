from tracking import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from django.shortcuts import render

from tracking.views import (
    product_detail,
    subpart_history,
    pic_dashboard,
    reports,
    export_product_summary_csv,
    export_product_summary_excel,
    export_status_history_csv,
    export_status_history_excel,
)


def home_view(request):
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),

    # Auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # ------------------------------------------------
    # PRODUCT RANGE LANDING PAGE
    # ------------------------------------------------
    path('products/', views.product_ranges, name='product_ranges'),

    # Products inside a range
    path(
        'products/range/<int:range_id>/',
        views.products_by_range,
        name='products_by_range'
    ),

    # Excel export per range
    path(
        'products/range/<int:range_id>/excel/',
        views.export_range_excel,
        name='range_excel'
    ),

    # Product detail
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),

    # ------------------------------------------------
    # SUB PART HISTORY
    # ------------------------------------------------
    path(
        'subparts/<int:subpart_id>/history/',
        subpart_history,
        name='subpart_history'
    ),

    # ------------------------------------------------
    # PIC DASHBOARD
    # ------------------------------------------------
    path('dashboard/', pic_dashboard, name='pic_dashboard'),

    path(
        'dashboard/export/',
        views.export_pic_dashboard_excel,
        name='export_pic_dashboard_excel'
    ),

    # ------------------------------------------------
    # REPORTS
    # ------------------------------------------------
    path('reports/', reports, name='reports'),

    path(
        'reports/product/<int:product_id>/',
        views.product_progress_report,
        name='product_progress'
    ),

    path(
        'reports/product/<int:product_id>/excel/',
        views.product_progress_excel,
        name='product_progress_excel'
    ),

    # Global exports
    path('reports/export/product-summary/csv/', export_product_summary_csv),
    path('reports/export/product-summary/excel/', export_product_summary_excel),
    path('reports/export/status-history/csv/', export_status_history_csv),
    path('reports/export/status-history/excel/', export_status_history_excel),

    # Product summary Excel
    path(
        'products/excel/',
        views.product_list_excel,
        name='product_list_excel'
    ),
]




# Password change
path(
    "password-change/",
    auth_views.PasswordChangeView.as_view(
        template_name="registration/password_change.html"
    ),
    name="password_change"
),

# Password change success → logout
path(
    "password-change/done/",
    auth_views.LogoutView.as_view(next_page="login"),
    name="password_change_done"
),
