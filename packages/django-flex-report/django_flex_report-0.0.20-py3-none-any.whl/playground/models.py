from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from report import report_model


class IntermediateTest(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="intermediate_tests")

    @classmethod
    def report_search_fields(cls):
        return ["name"]


@report_model.register
class Test(models.Model):
    test = models.ForeignKey(IntermediateTest, on_delete=models.CASCADE, related_name="tests")
    title = models.CharField(max_length=200, verbose_name=_("Title"))

    @classmethod
    def report_search_fields(cls):
        return ["title"]
