# Generated by Django 2.2.7 on 2019-11-23 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grantmaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('kind', models.CharField(choices=[('OPEN', 'Open'), ('PRIVATE', 'Private'), ('GOVT', 'Government')], max_length=20)),
                ('description', models.CharField(max_length=2500, null=True)),
                ('mission', models.CharField(max_length=5000, null=True)),
                ('address', models.CharField(max_length=250, null=True)),
                ('address2', models.CharField(max_length=250, null=True)),
                ('city', models.CharField(max_length=250, null=True)),
                ('state', models.CharField(max_length=20, null=True)),
                ('zip_code', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(max_length=250, null=True)),
                ('email', models.CharField(max_length=250, null=True)),
                ('url', models.CharField(max_length=250, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('extension', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=2500, null=True)),
                ('deadline', models.DateTimeField(null=True)),
                ('restricted', models.CharField(choices=[('YES', 'Restricted'), ('NO', 'Unrestricted'), ('UNK', 'Unknown')], max_length=20)),
                ('restrictions', models.CharField(max_length=5000, null=True)),
                ('grantmaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sygma.Grantmaker')),
            ],
        ),
    ]
