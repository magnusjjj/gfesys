from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
# Create your models here.
class Page(models.Model):
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('page.views.page', args=[str(self.id)])
	
	name = models.CharField(max_length=200)
	content = models.TextField()
	type= models.CharField(max_length=200, default="")
	
	parent_content_type = models.ForeignKey(ContentType, blank=True, null=True)
	parent_object_id = models.PositiveIntegerField(blank=True, null=True)
	
	parent = GenericForeignKey('parent_content_type', 'parent_object_id')