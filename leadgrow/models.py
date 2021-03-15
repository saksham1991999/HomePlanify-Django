from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Business(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    email = models.EmailField()
    mobile = PhoneNumberField()
    address = models.CharField(max_length=512)
    image = models.ImageField()
    website = models.URLField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    business = models.ForeignKey("leadgrow.Business", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    mobile = PhoneNumberField()
    labels = models.ManyToManyField("leadgrow.Label", related_name="customer_labels")
    location = models.CharField(max_length=256)
    address = models.CharField(max_length=512)
    budget = models.PositiveIntegerField()
    property_type = models.CharField(max_length=128)
    event_name = models.CharField(max_length=128)
    event_date = models.DateTimeField()
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=128)
    color = models.CharField(max_length=128)
    customer = models.ForeignKey("leadgrow.Customer", related_name='labelled', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    customer = models.ForeignKey("leadgrow.Customer", on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    time = models.DurationField()
    task = models.TextField()
    completed = models.BooleanField(default=False)
    task_importance_choices = (
        ("I", "Important But Not Urgent"),
        ("U", "Urgent"),
        ("R", "Routine Task"),
    )
    importance = models.CharField(choices=task_importance_choices, max_length=1)


class Note(models.Model):
    customer = models.ForeignKey("leadgrow.Customer", on_delete=models.CASCADE)
    note = models.TextField()
