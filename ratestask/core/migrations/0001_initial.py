# Generated by Django 3.1.7 on 2021-02-20 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Port',
            fields=[
                ('code', models.TextField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
            options={
                'db_table': 'ports',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('parent', models.ForeignKey(blank=True, db_column='parent_slug', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.region')),
            ],
            options={
                'db_table': 'regions',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(db_column='day')),
                ('price', models.DecimalField(db_column='price', decimal_places=2, max_digits=8)),
                ('dest_code', models.ForeignKey(db_column='dest_code', max_length=5, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dest_code', to='core.port')),
                ('orig_code', models.ForeignKey(db_column='orig_code', max_length=5, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orig_code', to='core.port')),
            ],
            options={
                'db_table': 'prices',
            },
        ),
        migrations.AddField(
            model_name='port',
            name='region',
            field=models.ForeignKey(db_column='parent_slug', on_delete=django.db.models.deletion.DO_NOTHING, to='core.region'),
        ),
    ]
