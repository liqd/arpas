from rest_framework import serializers

from .models import Topic


class TopicSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    labels = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = (
            "id",
            "slug",
            "name",
            "description",
            "category",
            "labels",
            "module",
            "created",
        )

    def get_labels(self, topic):
        return [label.name for label in topic.labels.all()]
