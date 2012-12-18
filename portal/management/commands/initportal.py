from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group,Permission

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Init portal and add customer groups'

    def handle(self, *args, **options):
        try:
            cg = Group.objects.create(name="customer")
        except:
            self.stderr.write('DB OPS failed\n')
            return

        p1=Permission.objects.get(codename="add_user")
        p2=Permission.objects.get(codename="change_user")
        p3=Permission.objects.get(codename="delete_user")
        p4=Permission.objects.get(codename="add_session")
        p5=Permission.objects.get(codename="change_session")
        p6=Permission.objects.get(codename="delete_session")

        cg.permissions.add(p4)
        cg.permissions.add(p5)
        cg.permissions.add(p6)

        self.stdout.write('Successfully init\n')
