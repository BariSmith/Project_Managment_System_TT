import uuid
from django.db import models
import os
from django.dispatch import receiver
from versatileimagefield.fields import VersatileImageField


# Create your models here.
class Project(models.Model):
    # project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField('shortcut', blank=True)
    project_name = models.CharField(max_length=25, unique=True)
    project_detail = models.CharField(max_length=150)
    project_image = VersatileImageField(upload_to='media')


    def __str__(self):
        return self.project_name

@receiver(models.signals.post_delete, sender=Project)
def delete_Project_images(sender, instance, **kwargs):
    # Deletes Image Renditions
    instance.project_image.delete_all_created_images()
    # Deletes Original Image
    instance.project_image.delete(save=False)


class Programmer(models.Model):
    programmer_name = models.CharField(max_length=50, unique=False)
    programmer_surname = models.CharField(max_length=50, unique=False)
    programmer_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    programmer_deadline = models.DateField()
    programmer_birthday = models.DateField()
    programmer_rank = models.CharField(max_length=50, unique=False)
    programmer_image = VersatileImageField(upload_to='profile', blank=True)

    def __str__(self):
        return self.programmer_name

@receiver(models.signals.post_delete, sender=Programmer)
def delete_Programmer_images(sender, instance, **kwargs):
    # Deletes Image Renditions
    instance.programmer_image.delete_all_created_images()
    # Deletes Original Image
    instance.programmer_image.delete(save=False)

@receiver(models.signals.pre_save, sender=Programmer)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image = sender.objects.get(pk=instance.pk).student_image
    except sender.DoesNotExist:
        return False

    new_image = instance.programmer_image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)

type = (
    ('1', 'Feature'),
    ('2', 'Bug'),
)

priority = (
    ('1', 'Normal'),
    ('2', 'Hight'),
    ('3', 'Low'),
)
class Task(models.Model):
    task_name = models.CharField(max_length=25, unique=True)
    task_description = models.CharField(max_length=150)
    task_startwork = models.DateField()
    task_deadline = models.DateField()
    task_type = models.CharField(max_length=20, choices=type, default=None)

    task_programmer = models.ForeignKey(Programmer, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name
# Create your models here.
