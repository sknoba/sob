from django.urls import path
from .import views
from .views import FeesCollectionListView, FeesCollectionDetailView, InvoiceCreateView, FeesDashboardView
from .export_util import GenerateInvoincePDF
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', FeesDashboardView.as_view(), name='fees-dashboard'),
    path('fees-collection/', FeesCollectionListView.as_view(), name='fees-list'),
    path('fees-collection/<int:pk>/detail', FeesCollectionDetailView.as_view(), name='fees-detail'),

    ###Invoince
    path('invoince/<int:pk>/create', InvoiceCreateView.as_view(), name='invoice-create'),

    ###Export PDF
    path('<int:id>/invoince-pdf/', GenerateInvoincePDF.as_view(), name='invoince-pdf'),
    path('get_invoice_details/<int:pk>/', views.get_invoice_details, name='get_invoice_details'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)