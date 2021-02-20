"""
"""
from django.db import models


class Region(models.Model):
    """
    """
    slug = models.SlugField(primary_key=True)
    name = models.TextField()
    # below column name could be parent
    parent = models.ForeignKey('self', models.DO_NOTHING,
                               db_column='parent_slug',
                               blank=True, null=True)

    class Meta:
        db_table = 'regions'


class Port(models.Model):
    """
    """
    code = models.TextField(primary_key=True, max_length=5)
    name = models.TextField()
    # below column name could be region
    region = models.ForeignKey('Region', models.DO_NOTHING,
                               db_column='parent_slug')

    class Meta:
        db_table = 'ports'


class Price(models.Model):
    orig_code = models.ForeignKey(Port, models.DO_NOTHING,
                                  related_name='orig_code',
                                  max_length=5, db_column='orig_code')
    dest_code = models.ForeignKey(Port, models.DO_NOTHING,
                                  related_name='dest_code',
                                  max_length=5, db_column='dest_code')
    day = models.DateField(db_column='day')
    # changing column type to decimal
    price = models.DecimalField(max_digits=8, decimal_places=2, db_column='price')

    class Meta:
        db_table = 'prices'



