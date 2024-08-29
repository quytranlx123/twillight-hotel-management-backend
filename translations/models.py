# translations/models.py

from django.db import models

class Translation(models.Model):
    language_code = models.CharField(max_length=10)
    table_name = models.CharField(max_length=50)
    column_name = models.CharField(max_length=50)
    record_id = models.IntegerField()
    translated_text = models.TextField()

    def __str__(self):
        return f"Translation {self.id} for {self.table_name} - {self.column_name}"
