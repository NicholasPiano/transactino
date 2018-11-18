# Generated by Django 2.0.4 on 2018-11-14 01:45

import apps.subscription.models.challenge.generate
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('public_key', models.TextField(default='')),
                ('long_key_id', models.CharField(default='', max_length=255)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=False)),
                ('is_locked', models.BooleanField(default=False)),
                ('is_superadmin_locked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('value', models.CharField(max_length=255)),
                ('is_external', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('origin', models.UUIDField(default=uuid.uuid4)),
                ('content', models.TextField(default=apps.subscription.models.challenge.generate.generate_challenge_content, editable=False)),
                ('encrypted_content', models.TextField(default='')),
                ('is_open', models.BooleanField(default=True)),
                ('has_been_used', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to='subscription.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('ip_value', models.CharField(max_length=255, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('port', models.PositiveIntegerField(null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('closed_at', models.DateTimeField(null=True)),
                ('closed_with_code', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('value', models.BigIntegerField(default=0)),
                ('is_open', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('value', models.CharField(max_length=255)),
                ('is_online', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ips', to='subscription.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('address', models.CharField(default='', max_length=255)),
                ('origin', models.UUIDField(default=uuid.uuid4)),
                ('is_open', models.BooleanField(default=True)),
                ('has_been_used', models.BooleanField(default=False)),
                ('time_confirmed', models.DateTimeField(null=True)),
                ('base_amount', models.BigIntegerField(default=0)),
                ('unique_btc_amount', models.BigIntegerField(default=0)),
                ('full_btc_amount', models.BigIntegerField(default=0)),
                ('block_hash', models.CharField(default='', max_length=64)),
                ('txid', models.CharField(default='', max_length=64)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='subscription.Account')),
                ('from_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_sent', to='subscription.Address')),
                ('to_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_received', to='subscription.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('origin', models.UUIDField(default=uuid.uuid4)),
                ('duration_in_days', models.PositiveIntegerField(default=0)),
                ('activation_date', models.DateTimeField(null=True)),
                ('is_valid_until', models.DateTimeField(null=True)),
                ('is_payment_confirmed', models.BooleanField(default=False)),
                ('has_been_activated', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('last_update_time', models.DateTimeField(null=True)),
                ('is_contract_signed', models.BooleanField(default=False)),
                ('contract', models.TextField(default='')),
                ('contract_client_signature', models.TextField(default='')),
                ('contract_system_signature', models.TextField(default='')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='subscription.Account')),
            ],
        ),
        migrations.AddField(
            model_name='connection',
            name='ip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='connections', to='subscription.IP'),
        ),
    ]