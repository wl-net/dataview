from django.core.management.base import NoArgsCommand, make_option
from sign.models import Sign, Widget

class Command(NoArgsCommand):
 
    help = "Run the automation proccessor"
 
    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
        make_option('--update-widgets', action='store_true', dest='update-widgets'),
        make_option('--update-widgets-list', action='store_true', dest='update-widgets-list'),
    )
 
    def handle(self, *args, **options):
        if options['update-widgets']:
            print("Updating widgets...")
            Sign.update_signs()

        if options['update-widgets-list']:
            print("Updating widgets list...")
            Widget.update_widget_list()

    def handle_noargs(self, **options):
        pass
