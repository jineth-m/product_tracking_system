from tracking import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import render

from tracking.views import (
    product_list,
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

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),

    path('subparts/<int:subpart_id>/history/', subpart_history, name='subpart_history'),

    path('dashboard/', pic_dashboard, name='pic_dashboard'),

    path(
    "products/range/<int:range_id>/excel/",
    views.export_range_excel,
    name="export_range_excel"
),



    path("products/range/<int:range_id>/excel/", views.export_range_excel, name="export_range_excel"),


    path(
    "dashboard/export/",
    views.export_pic_dashboard_excel,
    name="export_pic_dashboard_excel",
),


    path('reports/', reports, name='reports'),
    path(
    "products/excel/",
    views.product_list_excel,
    name="product_list_excel"
),



    path(
    "reports/product/<int:product_id>/excel/",
    views.product_progress_excel,
    name="product_progress_excel",
),




    path(
    "reports/product/<int:product_id>/",
    views.product_progress_report,
    name="product_progress"
),


    # Exports
    path('reports/export/product-summary/csv/', export_product_summary_csv),
    path('reports/export/product-summary/excel/', export_product_summary_excel),
    path('reports/export/status-history/csv/', export_status_history_csv),
    path('reports/export/status-history/excel/', export_status_history_excel),
    path(
    'subparts/<int:subpart_id>/history/',
    views.subpart_history,
    name='subpart_history'
),


]
