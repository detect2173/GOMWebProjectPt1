from django.db import models


class Lead(models.Model):
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(unique=True)
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"
