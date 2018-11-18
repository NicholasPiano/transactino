# Generated by Django 2.0.4 on 2018-11-14 01:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('is_active', models.BooleanField(default=False)),
                ('blocks_to_include', models.PositiveIntegerField(default=1)),
                ('latest_block_hash', models.CharField(default='', max_length=64)),
                ('has_been_ready', models.BooleanField(default=False)),
                ('has_been_run', models.BooleanField(default=False)),
                ('is_processing', models.BooleanField(default=False)),
                ('average_tx_fee', models.FloatField(default=0)),
                ('average_tx_fee_density', models.FloatField(default=0)),
                ('last_update_start_time', models.DateTimeField(null=True)),
                ('last_update_end_time', models.DateTimeField(null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fee_reports', to='subscription.Account')),
            ],
        ),
        migrations.CreateModel(
            name='FeeReportBlockWrapper',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('hash', models.CharField(max_length=64)),
                ('average_tx_fee', models.FloatField(default=0.0)),
                ('average_tx_fee_density', models.FloatField(default=0.0)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('is_processing', models.BooleanField(default=False)),
                ('is_complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FeeReportBlockWrapperPrototype',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('hash', models.CharField(max_length=64)),
            ],
        ),
    ]