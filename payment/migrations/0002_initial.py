# Generated by Django 5.0.4 on 2024-05-10 10:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment', '0001_initial'),
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cards_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_made', to='user.client'),
        ),
        migrations.AddField(
            model_name='payment',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_received', to='user.freelancer'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='user.freelancer'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscription_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.subscriptiontype'),
        ),
        migrations.AddField(
            model_name='withdraw',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to='user.freelancer'),
        ),
    ]
