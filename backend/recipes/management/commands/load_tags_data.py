from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'colour': '#3DD25A', 'slug': 'breakfast'},
            {'name': 'Обед', 'colour': '#10B7FF', 'slug': 'dinner'},
            {'name': 'Ужин', 'colour': '#F61930', 'slug': 'supper'},
            {'name': 'Первое', 'colour': '#B840CF', 'slug': 'first'},
            {'name': 'Второе', 'colour': '#003153', 'slug': 'second'},
            {'name': 'Салат', 'colour': '#D8FF10', 'slug': 'salad'},
        ]
        try:
            Tag.objects.bulk_create(Tag(**tag) for tag in data)
        except ValueError:
            print('Неопределенное значение.')
        else:
            print('Теги успешно импортированы.')
