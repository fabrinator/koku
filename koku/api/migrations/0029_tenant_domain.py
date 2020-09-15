# Generated by Django 3.1.1 on 2020-09-15 15:37
import django.db.models.deletion
import django_tenants.postgresql_backend.base
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("api", "0028_public_function_update")]

    operations = [
        migrations.AlterField(
            model_name="providerauthentication", name="credentials", field=models.JSONField(default=dict)
        ),
        migrations.AlterField(
            model_name="providerbillingsource", name="data_source", field=models.JSONField(default=dict)
        ),
        migrations.AlterField(model_name="sources", name="authentication", field=models.JSONField(default=dict)),
        migrations.AlterField(
            model_name="sources", name="billing_source", field=models.JSONField(default=dict, null=True)
        ),
        migrations.AlterField(model_name="sources", name="status", field=models.JSONField(default=dict, null=True)),
        migrations.AlterField(
            model_name="tenant",
            name="schema_name",
            field=models.CharField(
                db_index=True,
                max_length=63,
                unique=True,
                validators=[django_tenants.postgresql_backend.base._check_schema_name],
            ),
        ),
        migrations.CreateModel(
            name="TenantDomain",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("domain", models.CharField(db_index=True, max_length=253, unique=True)),
                ("is_primary", models.BooleanField(db_index=True, default=True)),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="domains", to="api.tenant"
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]