from django.core.management.base import BaseCommand
from sensors.models import SensorValue
import datetime

class Command(BaseCommand):
 
    help = "Deletes old sensor values"

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
            action='store_true',
            dest='verbose',
            default=False)

        parser.add_argument('-y',
            action='store_true',
            dest='verbose',
            default=False)

        parser.add_argument('sensor_id', type=str)
        parser.add_argument('age', type=str)

    def handle(self, *args, **options):      
        now = datetime.datetime.now()
        then = now - datetime.timedelta(days=int(options['age']))
        svs = SensorValue.objects.filter(sensor=options['sensor_id'], updated__lte=then)
        print("Delete {0} recorded senor values before {1}?".format(svs.count(), then))
        choice = input("Type 'delete' to confirm: ").lower()
        if choice == "delete":
            print("Deleting...")
            svs.delete()
        else:
            print("Aborting...")