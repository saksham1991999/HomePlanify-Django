from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from datetime import datetime

from .models import Business, Customer, Label, Task, Note


class BusinessSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Business
        fields = (
            "id",
            "user",
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
    # created_at = serializers.DateTimeField(
    #     default=serializers.CreateOnlyDefault(datetime.now)
    # )

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
            "event_name",
            "event_date",
        )
        read_only_fields = (
            "created_at",
        )

    def create(self, validated_data):
        user = self.context['request'].user
        business = Business.objects.get(user=user)
        return Customer.objects.create(business = business, **validated_data)

    def get_cleaned_data(self):
        user = self.context['request'].user
        business = Business.objects.get(user=user)
        return {
            'business': business.id,
            'name': self.validated_data.get('name', ''),
            'location': self.validated_data.get('location', ''),
            'mobile': self.validated_data.get('mobile', ''),
            'email': self.validated_data.get('email', ''),
            'address': self.validated_data.get('address', ''),
            'labels': self.validated_data.get('labels', ''),
            'budget': self.validated_data.get('budget', ''),
            'property_type': self.validated_data.get('property_type', ''),
            'event_name': self.validated_data.get('event_name', ''),
            'event_date': self.validated_data.get('event_date', ''),
            'pinned': self.validated_data.get('pinned', ''),
        }

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


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = (
            "id",
            "customer",
            "note",
        )