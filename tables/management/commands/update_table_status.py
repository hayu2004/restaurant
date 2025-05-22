from django.core.management.base import BaseCommand
from restaurant.tables.views import update_table_status

class Command(BaseCommand):
    help = 'Cập nhật trạng thái bàn và booking theo thời gian'

    def handle(self, *args, **kwargs):
        update_table_status()
        self.stdout.write(self.style.SUCCESS('Đã cập nhật trạng thái bàn!'))