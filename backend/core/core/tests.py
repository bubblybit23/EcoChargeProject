from django.test import TestCase, Client
from .models import SystemStatus
from .errors import EmissionsDataError
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
        mock_get_grid_region.side_effect = EmissionsDataError("Could not determine grid region.")

        with patch('core.recommendations.get_realtime_emissions') as mock_get_realtime_emissions:
            mock_get_realtime_emissions.return_value = {"percent": 40}
            response = self.client.post('/api/recommendations/', {"lat": 14.5995, "lng": 120.9842}, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'error': 'EMISSIONS_DATA: Could not determine grid region.'})


    @patch('core.recommendations.get_grid_region')
    @patch('core.recommendations.get_realtime_emissions')
    def test_recommendations_view_no_emissions(self, mock_get_realtime_emissions, mock_get_grid_region):
        """Recommendations view returns an error message"""
        mock_get_grid_region.return_value = "PH"
        mock_get_realtime_emissions.side_effect = EmissionsDataError("Could not get real-time emissions data.")

        response = self.client.post('/api/recommendations/', {"lat": 14.5995, "lng": 120.9842}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'error': 'EMISSIONS_DATA: Could not get real-time emissions data.'})

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

    @patch('requests.get')
    def test_empty_response(self, mock_get):
        """Test empty response from WattTime API"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = ''
        with self.assertRaises(EmissionsDataError):
            from .watttime import get_grid_region
            get_grid_region(14.5995, 120.9842)

    @patch('requests.get')
    def test_400_response(self, mock_get):
        """Test 400 response from WattTime API"""
        mock_get.return_value.status_code = 400
        with self.assertRaises(EmissionsDataError):
            from .watttime import get_grid_region
            get_grid_region(14.5995, 120.9842)

    @patch('requests.get')
    def test_500_response(self, mock_get):
        """Test 500 response from WattTime API"""
        mock_get.return_value.status_code = 500
        with self.assertRaises(EmissionsDataError):
            from .watttime import get_grid_region
            get_grid_region(14.5995, 120.9842)

    @patch('requests.get')
    def test_non_json_response(self, mock_get):
        """Test non-JSON response from WattTime API"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'Content-Type': 'text/html'}
        with self.assertRaises(EmissionsDataError):
            from .watttime import get_grid_region
            get_grid_region(14.5995, 120.9842)

    @patch('requests.get')
    def test_missing_moer_field(self, mock_get):
        """Test missing 'moer' field in valid JSON from WattTime API"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'Content-Type': 'application/json'}
        mock_get.return_value.json.return_value = {}
        with self.assertRaises(EmissionsDataError):
            from .watttime import get_realtime_emissions
            get_realtime_emissions('PH')

    def test_invalid_coordinate_values(self):
        """Test invalid coordinate values"""
        with self.assertRaises(ValueError):
            from .watttime import get_grid_region
            get_grid_region(91, 120.9842)

        with self.assertRaises(ValueError):
            from .watttime import get_grid_region
            get_grid_region(14.5995, 181)
