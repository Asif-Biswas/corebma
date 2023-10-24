# Generated by Django 4.2.1 on 2023-10-24 14:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_userprofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Text",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "login_page_welcome_text",
                    models.TextField(blank=True, max_length=100, null=True),
                ),
                (
                    "login_page_text",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "create_an_account_text",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "signup_page_text",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "signup_page_welcome_text",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "signin_instead_text",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "chat_with_admin",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("logo", models.ImageField(blank=True, upload_to="media/logo")),
            ],
        ),
    ]