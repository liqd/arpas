# Generated by Django 2.2.11 on 2020-04-05 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a4_candy_organisations", "0010_organisation_site"),
    ]

    operations = [
        migrations.AddField(
            model_name="organisation",
            name="data_protection",
            field=models.TextField(
                blank=True,
                help_text="Please provide your data protection information.",
                verbose_name="Data protection",
            ),
        ),
        migrations.AddField(
            model_name="organisation",
            name="netiquette",
            field=models.TextField(
                blank=True,
                help_text="Please provide your rules for online discussions.",
                verbose_name="Netiquette",
            ),
        ),
        migrations.AddField(
            model_name="organisation",
            name="terms_of_use",
            field=models.TextField(
                blank=True,
                help_text="Please provide your terms of use.",
                verbose_name="Terms of use",
            ),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="description",
            field=models.CharField(
                blank=True,
                help_text="The description will be displayed on the landing page. max. 800 characters",
                max_length=800,
                verbose_name="Short description of your organisation",
            ),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="imprint",
            field=models.TextField(
                blank=True,
                help_text="Please provide all the legally required information of your imprint. The imprint will be shown on a separate page.",
                verbose_name="Imprint",
            ),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="title",
            field=models.CharField(
                blank=True,
                default="Organisation",
                help_text="The title of your organisation will be shown on the landing page. max. 100 characters",
                max_length=100,
                verbose_name="Title of your organisation",
            ),
        ),
    ]
