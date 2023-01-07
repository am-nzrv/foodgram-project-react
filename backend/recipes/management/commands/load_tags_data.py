from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#FF0000', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#C71585', 'slug': 'dinner'},
            {'name': 'Ужин', 'color': '#006400', 'slug': 'supper'},
            {'name': 'Первое', 'color': '#808000', 'slug': 'first'},
            {'name': 'Второе', 'color': '#FFFF00', 'slug': 'second'},
            {'name': 'Салат', 'color': '#000000', 'slug': 'salad'},
            {'name': 'Десерт', 'color': '#00BFFF', 'slug': 'dessert'}
        ]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        print('Теги успешно импортированы.')
