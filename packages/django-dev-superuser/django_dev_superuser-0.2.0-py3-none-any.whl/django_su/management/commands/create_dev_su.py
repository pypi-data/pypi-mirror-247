from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from django_su import conf

User = get_user_model()


class Command(BaseCommand):
    help = "Create a SuperUser"

    def create_superuser(self):
        User.objects.create_superuser(
            conf.USERNAME,
            password=conf.PASSWORD,
            **conf.EXTRA_ARGS,
        )

    def handle(self, *args, **options):
        filter_args = {
            f"{conf.USERNAME_FIELD}__iexact": conf.USERNAME.lower(),
        }
        exists = User.objects.filter(**filter_args).exists()
        if exists:
            self.stdout.write(
                self.style.WARNING(
                    f"SuperUser with {conf.USERNAME_FIELD}"
                    f" {conf.USERNAME} already exists",
                ),
            )
            return

        self.create_superuser()
        self.stdout.write(
            self.style.SUCCESS(
                f"SuperUser created with \n"
                f"\t{conf.USERNAME_FIELD}: {conf.USERNAME}\n"
                f"\tPassword: {conf.PASSWORD}",
            ),
        )
