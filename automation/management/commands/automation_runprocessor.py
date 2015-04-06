from django.core.management.base import BaseCommand
from automation.processor import Processor

class Command(BaseCommand):
 
    help = "Run the automation proccessor"

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
            action='store_true',
            dest='verbose',
            default=False)

    def handle(self, *args, **options):
        processor = Processor()
        processor.run()

    def handle_noargs(self, *args, **options):
        processor = Processor()
        processor.run()
