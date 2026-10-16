from django.db import migrations


def criar_grupos_padrao(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    # Grupo Editores de Conteúdo
    grupo_editores, _ = Group.objects.get_or_create(name="Editores de Conteúdo")
    for codename in [
        "pode_publicar_noticia",
        "pode_destacar_noticia",
        "pode_gerenciar_destaques",
        "pode_gerenciar_trilhas",
        "pode_gerenciar_votacao",
    ]:
        perm = Permission.objects.filter(codename=codename).first()
        if perm:
            grupo_editores.permissions.add(perm)

    # Grupos de Professores e Alunos
    Group.objects.get_or_create(name="Professores")
    Group.objects.get_or_create(name="Alunos")


def remover_grupos_padrao(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(
        name__in=["Editores de Conteúdo", "Professores", "Alunos"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = (
        ("rede_miradas", "0033_alter_blocoapresentacao_options_and_more"),
    )

    operations = (
        migrations.RunPython(criar_grupos_padrao, remover_grupos_padrao),
    )

