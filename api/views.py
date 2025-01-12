from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from .models import Account
from decimal import Decimal
import csv


def import_csv(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        for row in reader:
            account, created = Account.objects.get_or_create(
                account_id=row['ID'],
                defaults={
                    'name': row['Name'],
                    'opening_balance': row['Balance'],
                    'current_balance': row['Balance']
                }
            )
            if not created:
                account.name = row['name']
                account.opening_balance = row['opening_balance']
                account.current_balance = row['opening_balance']
                account.save()
        return JsonResponse({"message": "Accounts imported successfully"})
    return render(request, 'import_csv.html')


def list_accounts(request):
    accounts = Account.objects.all()
    data = serialize('json', accounts)
    return JsonResponse({'accounts': data})


def get_account(request, account_id):
    account = get_object_or_404(Account, account_id=account_id)
    return JsonResponse({
        'account_id': account.account_id,
        'name': account.name,
        'opening_balance': float(account.opening_balance),
        'current_balance': float(account.current_balance),
    })


@csrf_exempt
def transfer_funds(request):
    if request.method == "POST":
        source_id = request.POST['source_id']
        target_id = request.POST['target_id']
        amount = Decimal(request.POST['amount'])  # Convert to Decimal

        try:
            source_account = Account.objects.get(account_id=source_id)
            target_account = Account.objects.get(account_id=target_id)

            if source_account.current_balance < amount:
                return JsonResponse({"error": "Insufficient funds"}, status=400)

            with transaction.atomic():
                source_account.current_balance -= amount
                target_account.current_balance += amount
                source_account.save()
                target_account.save()

            return JsonResponse({"message": "Transfer successful"})
        except Account.DoesNotExist:
            return JsonResponse({"error": "One or both accounts not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
