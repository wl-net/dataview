from django.core.management.base import BaseCommand
from sign.models import Sign

class Command(BaseCommand):

    help = "Reload a sign"

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
            action='store_true',
            dest='verbose',
            default=False)

        parser.add_argument('sign_name', type=str)

    def handle(self, *args, **options):
        sign = Sign.objects.get(name=options['sign_name'])

        sign.reload_sign()

    def handle_noargs(self, *args, **options):
        print("Please see --help")
