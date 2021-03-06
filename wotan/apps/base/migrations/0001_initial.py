# Generated by Django 2.1.3 on 2018-12-01 12:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MockModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MockParentModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='mockmodel',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='base.MockParentModel'),
        ),
        migrations.AddField(
            model_name='mockmodel',
            name='parent_non_nullable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children_nn', to='base.MockParentModel'),
        ),
        migrations.AddField(
            model_name='mockmodel',
            name='under',
            field=models.ManyToManyField(related_name='over', to='base.MockModel'),
        ),
    ]
