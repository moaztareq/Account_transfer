from django.urls import path
from . import views

urlpatterns = [
    path('import-csv/', views.import_csv, name='import_csv'),
    path('list-accounts/', views.list_accounts, name='list_accounts'),
    path('account/<str:account_id>/', views.get_account, name='get_account'),
    path('transfer-funds/', views.transfer_funds, name='transfer_funds'),
]