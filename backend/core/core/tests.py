from django.test import TestCase, Client
from .models import SystemStatus
from unittest.mock import patch

class SystemStatusTestCase(TestCase):
    def test_system_status_creation(self):
        """SystemStatus objects are created with resilience_mode_active=False"""
        status = SystemStatus.objects.create()
        self.assertIs(status.resilience_mode_active, False)

class RecommendationsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('core.recommendations.get_grid_region')
    @patch('core.recommendations.get_realtime_emissions')
    def test_recommendations_view_success(self, mock_get_realtime_emissions, mock_get_grid_region):
        """Recommendations view returns a list of recommendations"""
        mock_get_grid_region.return_value = "PH"
        mock_get_realtime_emissions.return_value = {"percent": 40}

        response = self.client.post('/api/recommendations/', {"lat": 14.5995, "lng": 120.9842}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            "The grid is currently running on clean energy. It's a good time to run your appliances.",
            "Take advantage of the clean energy and charge your devices.",
        ])

    @patch('core.recommendations.get_grid_region')
    def test_recommendations_view_no_grid_region(self, mock_get_grid_region):
        """Recommendations view returns a default grid region"""
        mock_get_grid_region.return_value = None

        with patch('core.recommendations.get_realtime_emissions') as mock_get_realtime_emissions:
            mock_get_realtime_emissions.return_value = {"percent": 40}
            response = self.client.post('/api/recommendations/', {"lat": 14.5995, "lng": 120.9842}, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), [
                "The grid is currently running on clean energy. It's a good time to run your appliances.",
                "Take advantage of the clean energy and charge your devices.",
            ])

    @patch('core.recommendations.get_grid_region')
    @patch('core.recommendations.get_realtime_emissions')
    def test_recommendations_view_no_emissions(self, mock_get_realtime_emissions, mock_get_grid_region):
        """Recommendations view returns an error message"""
        mock_get_grid_region.return_value = "PH"
        mock_get_realtime_emissions.return_value = None

        response = self.client.post('/api/recommendations/', {"lat": 14.5995, "lng": 120.9842}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["Could not get real-time emissions data."])

    def test_recommendations_view_invalid_location(self):
        """Recommendations view returns an error message"""
        response = self.client.post('/api/recommendations/', '{"lat": "invalid", "lng": "invalid"}', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid location data'})

    def test_recommendations_view_invalid_method(self):
        """Recommendations view returns an error message"""
        response = self.client.put('/api/recommendations/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'error': 'Invalid request method'})
