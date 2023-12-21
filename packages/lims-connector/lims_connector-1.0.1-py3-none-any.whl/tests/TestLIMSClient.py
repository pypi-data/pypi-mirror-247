import unittest
from unittest.mock import patch, mock_open, MagicMock
from lims_connector.connectToLIMS import connect_to_lims

class TestConnectToLIMS(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='config_file: example_config.yaml\nenvironment: test')
    @patch('lims_connector.connectToLIMS.get_config', return_value={'config_file': 'example_config.yaml', 'environment': 'test'})
    @patch('yaml.safe_load', return_value={'test': {'username': 'user', 'password': 'pass', 'host': 'localhost', 'database': 'testdb', 'sslca': 'ssl_certificate'}})
    @patch('sqlalchemy.create_engine')
    def test_connect_to_lims(self, mock_create_engine, mock_safe_load, mock_get_config, mock_open):
        # Mocking the necessary objects
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        # Calling the function
        db_engine = connect_to_lims()

        # Assertions
        #mock_get_config.assert_called_once()
        mock_open.assert_called_once_with('example_config.yaml', 'r')
        mock_safe_load.assert_called_once_with(mock_open())
        mock_create_engine.assert_called_once_with('mysql+pymysql://user:pass@localhost/testdb', connect_args={'ssl': {'ssl_ca': 'ssl_certificate'}})

        self.assertEqual(db_engine, mock_engine)

if __name__ == '__main__':
    unittest.main()
