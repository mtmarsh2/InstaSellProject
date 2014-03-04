from django.core.management.base import BaseCommand, CommandError
from dormpics.models import DormPic
from taggit.managers import TaggableManager

class Command(BaseCommand):
    args = ""
    help = ""

    def handle(self, *args, **options):
        for dormpic_id in args:
            try:
                dormpic = DormPic.objects.get(pk=int(dormpic_id))
            except DormPic.DoesNotExist:
                raise CommandError('DormPic "%s" does not exist' % dormpic_id)

            print str(dormpic.title)
            dormpic.tags.add('action')
            dormpic.save()
            self.stdout.write('Success in adding tag')

