from tenants.models import Domain

for domain in Domain.objects.all():
    domain.domain = domain.domain.replace('bepasal.com', 'localhost')
    domain.save()
