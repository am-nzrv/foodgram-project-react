from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'colour': '#F61930', 'slug': 'breakfast'},
            {'name': 'Обед', 'colour': '#D8FF10', 'slug': 'dinner'},
            {'name': 'Ужин', 'colour': '#10B7FF', 'slug': 'supper'},
            {'name': 'Первое', 'colour': '#B840CF', 'slug': 'first'},
            {'name': 'Второе', 'colour': '#3DD25A', 'slug': 'second'},
            {'name': 'Салат', 'colour': '#003153', 'slug': 'salad'},
        ]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        print('Теги успешно импортированы.')
