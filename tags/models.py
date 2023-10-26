from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label

# making a class that will consist of all the applied tag on the objects


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # we import contenttype from django instead of importing the store app as with that our
    # entire tag app would have depend on that class as this import the properties of the
    # product class#
    # this will get us the id of the product
    object_id = models.PositiveIntegerField()
    # this will get us the detail about the object
    content_object = GenericForeignKey()
