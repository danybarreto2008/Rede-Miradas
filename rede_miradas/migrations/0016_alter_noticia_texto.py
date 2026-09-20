import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rede_miradas', '0015_codigoprofessor_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='texto',
            field=django_ckeditor_5.fields.CKEditor5Field(config_name='default', verbose_name='Texto'),
        ),
    ]