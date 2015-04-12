from django.core.management.base import BaseCommand
from automation.processor import Processor

class Command(BaseCommand):
 
    help = "Run an automation task"

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
            action='store_true',
            dest='verbose',
            default=False)

        parser.add_argument('automation_task', type=str)

    def handle(self, *args, **options):
        processor = Processor()
        processor.run_task(options['automation_task'])
