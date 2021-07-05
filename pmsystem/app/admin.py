from django.contrib import admin
from .models import Project, Programmer, Task
# Register your models here.
admin.site.register(Project)
admin.site.register(Programmer)
admin.site.register(Task)