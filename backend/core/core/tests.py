from django.test import TestCase
from .models import SystemStatus

class SystemStatusTestCase(TestCase):
    def test_system_status_creation(self):
        """SystemStatus objects are created with resilience_mode_active=False"""
        status = SystemStatus.objects.create()
        self.assertIs(status.resilience_mode_active, False)
