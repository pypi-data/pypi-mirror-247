import unittest
from unittest.mock import patch, Mock
from cmhlims.getSampleNames import get_sample_names

class TestGetSampleNames(unittest.TestCase):

    @patch('cmhlims.getSampleNames.connect_to_lims')
    @patch('cmhlims.getSampleNames.MetaData')
    @patch('cmhlims.getSampleNames.automap_base')
    @patch('cmhlims.getSampleNames.sessionmaker')
    def test_get_sample_names(self, mock_sessionmaker, mock_automap_base, mock_metadata, mock_connect_to_lims):
        # Set up mocks for necessary objects
        mock_engine = Mock()
        mock_session = Mock()
        mock_samples_query = Mock()

        # Configure the mocks
        mock_connect_to_lims.return_value = mock_engine
        mock_metadata.return_value = mock_metadata
        mock_automap_base.return_value = mock_automap_base
        mock_sessionmaker.return_value = mock_session
        mock_session.query.return_value = mock_samples_query
        mock_samples_query.all.return_value = [('Sample1',), ('Sample2',), ('Sample3',)]

        # Calling the function under test
        result = get_sample_names()

        # Assertions
        self.assertEqual(result, ['Sample1', 'Sample2', 'Sample3'])
        mock_connect_to_lims.assert_called_once()
        mock_metadata.reflect.assert_called_once_with(mock_engine, only=['samples'])
        mock_automap_base.prepare.assert_called_once_with(mock_engine)
        mock_sessionmaker.assert_called_once_with(bind=mock_engine)
        mock_session.query.assert_called_once_with(mock_automap_base.classes.samples.label)
        mock_samples_query.all.assert_called_once()
        mock_session.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
