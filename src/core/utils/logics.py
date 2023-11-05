from django.db import connection
from django.shortcuts import render


def index(request):
    return render(request, f'{request.tenant.get_tenant_type()}/index.html')
