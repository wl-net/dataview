from django.core.management.base import BaseCommand
from sign.models import SignType, Sign, Widget


class Command(BaseCommand):
 
    help = "Update sign functionality"

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
            action='store_true',
            dest='verbose',
            default=False)

        parser.add_argument('--update-widgets',
            action='store_true',
            dest='update-widgets',
            default=False)

        parser.add_argument('--update-widgets-list',
            action='store_true',
            dest='update-widgets-list',
            default=False)

        parser.add_argument('--update-sign-type-list',
            action='store_true',
            dest='update-sign-type-list',
            default=False)

    def handle(self, *args, **options):
        if options['update-widgets']:
            print("Updating widgets...")
            Sign.update_signs()

        if options['update-widgets-list']:
            print("Updating widgets list...")
            Widget.update_widget_list()

        if options['update-sign-type-list']:
            print("Updating sign type list...")
            SignType.update_sign_type_list()

    def handle_noargs(self, *args, **options):
        print("Please see --help")
