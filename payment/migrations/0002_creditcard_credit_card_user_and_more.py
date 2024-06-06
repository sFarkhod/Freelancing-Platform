# Generated by Django 5.0.4 on 2024-06-05 23:29

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='credit_card_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_credit_card', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='card_expiration_date',
            field=models.CharField(max_length=5, null=True, validators=[django.core.validators.RegexValidator(message='Expiration date must be in MM/YY format', regex='^(0[1-9]|1[0-2])\\/?([0-9]{2})$')]),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='card_holder_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='card_number',
            field=models.CharField(max_length=16, null=True, validators=[django.core.validators.RegexValidator(message='Card number must be 16 digits', regex='^\\d{16}$')]),
        ),
        migrations.AlterField(
            model_name='payment',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments_made', to='user.client'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='freelancer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments_received', to='user.freelancer'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='subscriptions', to='user.freelancer'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='freelancer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='withdrawals', to='user.freelancer'),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='withdraw_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
