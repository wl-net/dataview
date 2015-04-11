from django.core.management.base import BaseCommand
from sensors.models import SensorValue

class Command(BaseCommand):
 
    help = "Get a sensor's value"

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
            action='store_true',
            dest='verbose',
            default=False)

        parser.add_argument('sensor_id', type=str)

    def handle(self, *args, **options):
        sv = SensorValue.objects.filter(sensor=options['sensor_id']).order_by('-updated')[0]
        print("'{0}' was reported at {1}".format(sv.value, sv.updated))
