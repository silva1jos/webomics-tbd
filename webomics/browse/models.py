import datetime

from django.db import models
from django.utils import timezone

from .filetools import user_directory_path


class Experiment(models.Model):
    exp_name = models.CharField('experiment name', max_length=200)
    date_pref = models.DateTimeField('date performed')
    last_update = models.DateTimeField(auto_now=True)
    file_type = models.CharField(max_length=20)
    file_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    version = models.IntegerField()
    comments = models.TextField()
    # I don't know if settings.BASE_DIR is same as settings.py file
    file_path = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return self.exp_name

    @classmethod
    def fields(cls):
        return [field.name for field in Experiment._meta.get_fields()]

    def human_read_list(self):
        human = ['Experiment Name', 'Date Performed', 'Last Update',
                 'File Type', 'File Name', 'Author', 'Version', 'Comments',
                 'File Path']
        result = []
        for name, field in zip(human, self._meta.get_fields()[1:]):
            value = getattr(self, field.name)
            result.append((name, value))
        return result

    def was_recently_updated(self):
        return (timezone.now() - datetime.timedelta(days=1) <= self.last_update
                <= timezone.now())
