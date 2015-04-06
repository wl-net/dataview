from django.core.management.base import BaseCommand
from automation.processor import Processor

class Command(BaseCommand):
 
    help = "Run an automation automator"

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
            action='store_true',
            dest='verbose',
            default=False)

        parser.add_argument('automator_name', type=str)
        parser.add_argument('automator_method', type=str)
        parser.add_argument('automator_params', nargs='+', type=str)

    def handle(self, *args, **options):
        processor = Processor()
        processor.call_automator(options['automator_name'], options['automator_method'], options['automator_params'])
