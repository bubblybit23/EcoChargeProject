from django.db import models

class SystemStatus(models.Model):
    resilience_mode_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resilience Mode Active: {self.resilience_mode_active}"
