from django.core.management import BaseCommand
import pandas as pd
from product.models import Products
from sqlalchemy import create_engine
from django.conf import settings


class Command(BaseCommand):
    help = 'to add product data to database with csv file'

    def handle(self, *args, **kwargs):
        exel_file = 'add your path file'
        df = pd.read_excel(exel_file)

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'. \
            format(user=user, password=password, database_name=database_name, )

        engine = create_engine(database_url, echo=False)

        df.to_sql(Products._meta.db_table, if_exists='replace', con=engine, index=False)
