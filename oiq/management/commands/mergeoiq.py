from django.core.management.base import BaseCommand

from dtfapp.models import Employment, EmploymentRole, Company
from ...models import OIQResult

class Command(BaseCommand):
    help = "Merges OIQ query results into dtfapp's employment records."
    def handle(self, *args, **options):
        engineer_role = EmploymentRole.objects.get(code='engineer')
        to_process = OIQResult.objects.filter(employment=None).exclude(employer='')
        print("OIQ results to process: {}".format(to_process.count()))
        for result in to_process.all():
            person = result.query.person
            employer = result.employer
            if not employer:
                continue
            print("Processing {} working for {}".format(person, employer))
            company, created = Company.objects.get_or_create(name=employer)
            result.employment = Employment.objects.create(
                employee=person,
                employer=company,
                role=engineer_role,
                query_date=result.query.date,
            )
            result.save()

