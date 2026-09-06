from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rede_miradas', '0005_blocoapresentacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, help_text='Usado apenas como texto alternativo da imagem (acessibilidade).', max_length=200)),
                ('capa', models.ImageField(upload_to='curtas/')),
                ('link_youtube', models.URLField()),
                ('ativo', models.BooleanField(default=True)),
                ('ordem', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Curta em destaque',
                'verbose_name_plural': 'Curtas em destaque',
            },
        ),
        migrations.CreateModel(
            name='SecaoCurtas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='CURTAS EM DESTAQUE', max_length=200)),
                ('subtitulo', models.CharField(blank=True, max_length=300)),
            ],
            options={
                'verbose_name': 'Texto da seção de curtas',
                'verbose_name_plural': 'Texto da seção de curtas',
            },
        ),
    ]