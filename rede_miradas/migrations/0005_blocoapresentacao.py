from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rede_miradas', '0004_noticia'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlocoApresentacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.CharField(help_text='Emoji exibido no topo do card. Ex: 🎬', max_length=10)),
                ('texto', models.TextField(max_length=200)),
                ('cor_gradiente_1', models.CharField(default='#8b2ff7', max_length=7)),
                ('cor_gradiente_2', models.CharField(default='#22d3ee', max_length=7)),
                ('ativo', models.BooleanField(default=True)),
                ('ordem', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Bloco de apresentação',
                'verbose_name_plural': 'Blocos de apresentação',
            },
        ),
    ]