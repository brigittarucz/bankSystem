from django.db import models

class TestModel(models.Model):
    testcol = models.CharField(max_length=20)

    def __str__(self):
        # Returning self would get an infinite loop
        return f"{self.testcol}"