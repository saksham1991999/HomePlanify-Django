from django.db import models


class Business(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=512)
    image = models.ImageField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    business = models.ForeignKey("leadgrow.Business", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15)
    labels = models.ManyToManyField("leadgrow.Label", related_name="customer_labels", null=True)
    location = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=512, null=True, blank=True)
    budget = models.PositiveIntegerField(null=True, blank=True)
    property_type = models.CharField(max_length=128, null=True, blank=True)
    event_name = models.CharField(max_length=128, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=128)
    color = models.CharField(max_length=128)
    business = models.ForeignKey("leadgrow.Business", related_name='labelled', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    customer = models.ForeignKey("leadgrow.Customer", on_delete=models.CASCADE, null=True)
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
