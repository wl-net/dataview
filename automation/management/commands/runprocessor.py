from django.core.management.base import NoArgsCommand, make_option
from automation.processor import Processor

class Command(NoArgsCommand):
 
    help = "Run the automation proccessor"
 
    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
        make_option('--call-automator', action='store_true', dest='call-automator'),
    )
 
    def handle(self, *args, **options):
        if options['call-automator']:
            processor = Processor()
            processor.call_automator(args)
        else:
            processor = Processor()
            processor.run()
        
    def handle_noargs(self, **options):
        processor = Processor()
        processor.run()