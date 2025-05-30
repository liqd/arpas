from autoslug import AutoSlugField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4 import transforms
from adhocracy4.categories.fields import CategoryField
from adhocracy4.comments import models as comment_models
from adhocracy4.images.fields import ConfiguredImageField
from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.labels import models as labels_models
from adhocracy4.models import query
from adhocracy4.modules import models as module_models
from adhocracy4.ratings import models as rating_models
from apps.augmentedreality.models import Scene


class TopicQuerySet(query.RateableQuerySet, query.CommentableQuerySet):
    pass


class Topic(module_models.Item):
    item_ptr = models.OneToOneField(
        to=module_models.Item,
        parent_link=True,
        related_name="%(app_label)s_%(class)s",
        on_delete=models.CASCADE,
    )
    slug = AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=120, verbose_name=_("Title"))
    description = CKEditor5Field(
        config_name="image-editor",
        verbose_name=_("Description"),
        validators=[ImageAltTextValidator()],
    )
    image = ConfiguredImageField(
        "idea_image",
        verbose_name=_("Add image"),
        upload_to="ideas/images",
        blank=True,
    )
    ratings = GenericRelation(
        rating_models.Rating, related_query_name="topic", object_id_field="object_pk"
    )
    comments = GenericRelation(
        comment_models.Comment, related_query_name="topic", object_id_field="object_pk"
    )
    category = CategoryField()

    labels = models.ManyToManyField(
        labels_models.Label,
        verbose_name=_("Labels"),
        related_name=("%(app_label)s_" "%(class)s_label"),
    )

    objects = TopicQuerySet.as_manager()
    _scene = GenericRelation(Scene)

    class Meta:
        ordering = ["-created"]

    @cached_property
    def scene(self):
        return self._scene.first()

    @property
    def reference_number(self):
        return "{:d}-{:05d}".format(self.created.year, self.pk)

    def __str__(self):
        return self.name

    def save(self, update_fields=None, *args, **kwargs):
        self.description = transforms.clean_html_field(self.description, "image-editor")
        if update_fields:
            update_fields = {"description"}.union(update_fields)
        super().save(update_fields=update_fields, *args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "a4_candy_topicprio:topic-detail",
            kwargs=dict(
                organisation_slug=self.project.organisation.slug,
                pk="{:05d}".format(self.pk),
                year=self.created.year,
            ),
        )
