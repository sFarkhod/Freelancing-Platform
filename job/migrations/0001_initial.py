# Generated by Django 5.0.4 on 2024-05-09 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_type', models.CharField(choices=[('fixed', 'Fixed'), ('monthly', 'Monthly'), ('hourly', 'Hourly')], max_length=10)),
                ('project_length', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('proposal_text', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('proposal_date', models.DateTimeField(auto_now_add=True)),
                ('project_lengs', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RequiredSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField(default=0)),
                ('payment_type', models.CharField(choices=[('fixed', 'Fixed'), ('monthly', 'Monthly'), ('hourly', 'Hourly')], max_length=144)),
                ('project_lengs', models.CharField(max_length=255)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_text', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.offer')),
            ],
        ),
    ]
