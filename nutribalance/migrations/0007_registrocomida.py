# Generated by Django 5.1.1 on 2024-11-17 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutribalance', '0006_alter_paciente_foto_perfil'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroComida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='comidas/')),
                ('emocion', models.PositiveSmallIntegerField(choices=[(1, '😠'), (2, '😞'), (3, '😐'), (4, '😊'), (5, '😁')])),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_comida', to='nutribalance.paciente')),
            ],
        ),
    ]