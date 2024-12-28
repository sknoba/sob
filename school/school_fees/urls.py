from django.urls import path
from .import views
from .views import *
# from .export_util import GenerateInvoincePDF
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', FeesDashboardView.as_view(), name='fees-dashboard'),
    path('fees-collections/', FeesCollectionListView.as_view(), name='fees-collection-list'),
    path('fees-collection/<int:pk>/detail', FeesCollectionDetailView.as_view(), name='fees-detail'),
    path('fees-structures/', FeesStructureView.as_view(), name='fees-structure-list'),
    path('fees-strucrure-create', FeesStructureCreateView.as_view(), name='add_fees_structure'),
    path('fees-structure/delete/<int:fee_struc_id>/', FeesStuctureDeleteView.as_view(), name='fees_structure_delete'),

    path('fees-tranports/', TransportFeesView.as_view(), name="fees-traport-list"),


    path('get_transport_fee/', views.get_transport_fee, name='get_transport_fee'),
    # ###Invoince
    path('invoince/<int:pk>/create', InvoiceCreateView.as_view(), name='invoice-create'),

    # ###Export PDF
    # path('<int:id>/invoince-pdf/', GenerateInvoincePDF.as_view(), name='invoince-pdf'),
    # path('get_invoice_details/<int:pk>/', views.get_invoice_details, name='get_invoice_details'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)