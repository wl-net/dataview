from django.core.management.base import NoArgsCommand, make_option
from sign.models import Widget

class Command(NoArgsCommand):
 
    help = "Run the automation proccessor"
 
    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
        make_option('--update-widgets', action='store_true', dest='update-widgets'),
    )
 
    def handle(self, *args, **options):
        if options['update-widgets']:
            print("Updating widgets...")
            Widget.update_widget_list()

    def handle_noargs(self, **options):
        pass
