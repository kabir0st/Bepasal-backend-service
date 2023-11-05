from django.shortcuts import render
from django.http.response import JsonResponse
from django.db import connection
from users.models import UserBase


def index(request):
    return render(request, 'frontend/template-1/index.html')


def test(request):
    schema_name = connection.schema_name
    print(schema_name)
    for users in UserBase.objects.all():
        print(users)
    return JsonResponse({"status": True})
