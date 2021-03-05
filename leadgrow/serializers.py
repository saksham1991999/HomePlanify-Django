from rest_framework import serializers
from .models import Business, Customer, Label, Task, Note


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = (
            "id",
            "name",
            "email",
            "mobile",
            "address",
            "image",
            "website",
        )


class LabelCustomerSerializer(serializers.ModelSerializer):
    customers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Label
        fields = (
            "id",
            "name",
            "color",
            "customers",
        )

    def get_customers(self, obj):
        customers = obj.customer_labels.all().values_list('id', flat=True)
        return customers

class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = (
            "id",
            "name",
            "color",
        )


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            "id",
            "datetime",
            "time",
            "customer",
            "task",
            "completed",
            "importance",
        )


class CustomerSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField(read_only=True)
    labels = serializers.SerializerMethodField(read_only=True)
    tasks = serializers.SerializerMethodField(read_only=True)
    notes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "location",
            "mobile",
            "email",
            "address",
            "event",
            "labels",
            "tasks",
            "notes",
            'budget',
            "property_type",
            "pinned",
        )

    def get_event(self, obj):
        event = {
            "name": obj.event_name,
            "day": obj.event_date,
        }
        return event

    def get_labels(self, obj):
        labels = obj.labels.all()
        data = LabelSerializer(labels, many=True).data
        return data

    def get_tasks(self, obj):
        tasks = Task.objects.filter(customer = obj)
        data = TaskSerializer(tasks, many=True).data
        return data

    def get_notes(self, obj):
        notes = Note.objects.values_list('note', flat=True)
        return notes

