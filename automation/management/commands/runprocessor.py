from django.core.management.base import NoArgsCommand, make_option
from automation.processor import Processor

class Command(NoArgsCommand):
 
    help = "Run the automation proccessor"
 
    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
        make_option('--call-automator', action='store_true', dest='call-automator'),
        make_option('--call-decider', action='store_true', dest='call-decider'),
    )
 
    def handle(self, *args, **options):
        if options['call-automator']:
            processor = Processor()
            processor.call_automator(args)
        elif options['call-decider']:
            processor = Processor()
            processor.call_decider(args)
        else:
            processor = Processor()
            processor.run()
        
    def handle_noargs(self, **options):
        processor = Processor()
        processor.run()