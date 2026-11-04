from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria ou atualiza o usuário fixo da empresa"

    def handle(self, *args, **options):
        User = get_user_model()
        user, criado = User.objects.get_or_create(username=config("EMPRESA_USER"))
        user.set_password(config("EMPRESA_PASSWORD"))
        user.is_staff = False      
        user.is_superuser = False
        user.save()
        self.stdout.write(self.style.SUCCESS(
            "Usuário criado." if criado else "Senha do usuário atualizada."
        ))