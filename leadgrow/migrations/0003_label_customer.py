# Generated by Django 2.2 on 2021-03-13 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leadgrow', '0002_customer_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='labelled', to='leadgrow.Customer'),
        ),
    ]
