import logging
import random
import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from tabulate import tabulate

from core.factories import ItemFactory
from core.models import Item

log = logging.getLogger(__name__)


def chance(percent: int):
    return bool(random.randint(0, 100) <= percent)


class Command(BaseCommand):
    help = 'Resets and populates the database with basic data for local testing'

    def add_arguments(self, parser):

        parser.add_argument(
            'items',
            default=7,
            type=int,
            help='number of items to generate',
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        call_command('flush', '--noinput')
        ItemFactory.create_batch(options['items'])
        sys.stdout.write(tabulate(
            [
                (
                    s.id,
                    s.title,
                    s.desc[:40],
                    s.get_status_display(),
                    s.created_at.strftime('%Y.%m.%d %H:%M'),
                    s.modified.strftime('%Y.%m.%d %H:%M'),

                )
                for s in
                Item.objects.order_by('status')
            ],
            (
                'id',
                'title',
                'desc',
                'status',
                'created_at',
                'modified',
            ),
            tablefmt='fancy_grid'
        ) + '\n')
