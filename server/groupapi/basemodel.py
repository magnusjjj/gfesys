from django.db import models
from member.models import Member
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField

class GroupBaseModel(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    slug = AutoSlugField(max_length=40, populate_from='name')

    description = models.TextField()
    questions = models.TextField()

    image = models.ImageField(max_length=500, width_field='image_width', height_field='image_height',
                              upload_to='servers')
    image_height = models.IntegerField()
    image_width = models.IntegerField()


class Volunteer(models.Model):
    member = models.ForeignKey(Member)
    server = models.ForeignKey(Server)
    answer = models.TextField()
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.server.name + '/' + self.member.firstname + ' ' + self.member.surname

    STATUSCODES = (
        ("OK", "Accepted"),
        ("WAITING", "Waiting"),
        ("DENIED", "Denied"),
    )

    # accepted = models.BooleanField(default=False)

    status = models.CharField(max_length=200, default="WAITING", choices=STATUSCODES)

    sec_edit = models.BooleanField(default=False)
    sec_accept = models.BooleanField(default=False)
    sec_moderator = models.BooleanField(default=False)

    createdon = models.DateTimeField('Created on', auto_now_add=True)

    @staticmethod
    def patch_user_moderator(user, server):
        is_server_moderator = False
        try:
            # And return if we find admin rights on the current user
            volun = Volunteer.objects.all().filter(member=user, server=server, status="OK")[0]
            if volun.sec_moderator:
                is_server_moderator = True
        except:
            pass

        if is_server_moderator:
            user.is_moderator = True
            return user

    class Meta:
        ordering = ["-sec_accept", "-sec_edit", "role"]


class rocketchat(models.Model):
    server = models.ForeignKey(Server)
    channelname = models.CharField(max_length=200)
    rocketenabled = models.BooleanField(default=False)