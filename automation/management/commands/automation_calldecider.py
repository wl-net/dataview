from django.core.management.base import BaseCommand
from automation.processor import Processor

class Command(BaseCommand):
 
    help = "Run an automation decider"

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
            action='store_true',
            dest='verbose',
            default=False)

        parser.add_argument('decider_name', type=str)

    def handle(self, *args, **options):
        processor = Processor()
        processor.call_decider(options['decider_name'])
