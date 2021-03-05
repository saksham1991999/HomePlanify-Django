from django.contrib import admin
from .models import Business, Customer, Note, Task, Label

admin.site.register(Business)
admin.site.register(Customer)
admin.site.register(Note)
admin.site.register(Task)
admin.site.register(Label)
