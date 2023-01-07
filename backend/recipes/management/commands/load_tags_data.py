from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#F61930', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#D8FF10', 'slug': 'dinner'},
            {'name': 'Ужин', 'color': '#10B7FF', 'slug': 'supper'},
            {'name': 'Первое', 'color': '#B840CF', 'slug': 'first'},
            {'name': 'Второе', 'color': '#3DD25A', 'slug': 'second'},
            {'name': 'Салат', 'color': '#003153', 'slug': 'salad'},
        ]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        print('Теги успешно импортированы.')
