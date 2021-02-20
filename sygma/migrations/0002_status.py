# Generated by Django 2.2.7 on 2019-11-26 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sygma', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NEVER', 'Never Applied'), ('LOISENT', 'Letter of Intent Sent'), ('LOIACCEPTED', 'Letter of Intent Accepted'), ('INPROGRESS', 'Application in progress'), ('SUBMITTED', 'Submitted'), ('REJECTED', 'Rejected'), ('OFFERED', 'Offered'), ('ACCEPTED', 'Accepted'), ('RECEIVED', 'Received')], max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18, null=True)),
                ('details', models.CharField(max_length=5000, null=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('grant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sygma.Grant')),
            ],
        ),
    ]
