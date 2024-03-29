from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Ingredients


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for row in DictReader(open('./data/ingredients.csv',
                                   encoding='utf-8')):
            ingredients = Ingredients(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            ingredients.save()
        print('Ингредиенты успешно импортированы.')
