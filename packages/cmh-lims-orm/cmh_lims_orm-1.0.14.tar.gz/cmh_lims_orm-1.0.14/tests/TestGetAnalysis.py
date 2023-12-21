import unittest
from unittest.mock import patch, Mock
from cmhlims.getAnalysis import get_analysis

class TestGetAnalysis(unittest.TestCase):
    @patch('cmhlims.getAnalysis.connect_to_lims')
    @patch('cmhlims.getAnalysis.MetaData')
    @patch('cmhlims.getAnalysis.automap_base')
    @patch('cmhlims.getAnalysis.sessionmaker')
    def setUp(self, mock_sessionmaker, mock_automap_base, mock_metadata, mock_connect_to_lims):
        # Mocking the necessary objects
        self.mock_engine = Mock()
        self.mock_session = Mock()
        self.mock_query = Mock()

        mock_connect_to_lims.return_value = self.mock_engine
        mock_metadata.return_value = mock_metadata
        mock_automap_base.return_value = Mock()
        mock_sessionmaker.return_value = self.mock_session

    def test_get_analysis(self):
        # Mocking the behavior of the Session.query().all() method
        self.mock_session.query.return_value = self.mock_query
        self.mock_query.all.return_value = [('cmh000514', 1, 'Analysis1', '/path/to/analysis', '2023-01-01', 'Type1', 'Type2', 'GRCh38')]

        # Calling the function
        result = get_analysis(["cmh000514"], "GRCh38")

        # Assertions
        expected_columns = ['sample_name', 'analysis_id', 'analysis_name', 'analysis_dir', 'analysis_date', 'sequence_type', 'analysis_type', 'reference_genome']
        #expected_result = [('cmh000514', 1, 'Analysis1', '/path/to/analysis', '2023-01-01', 'Type1', 'Type2', 'GRCh38')]
        self.assertEqual(result.columns.tolist(), expected_columns)
        #self.assertEqual(result.values.tolist(), expected_result)

        #self.mock_connect_to_lims.assert_called_once()
        #self.mock_metadata.reflect.assert_called_once_with(self.mock_engine, only=['samples', 'downstream_analyses', 'downstream_analysis_types', 'sequence_types', 'reference_genomes'])
        #self.mock_automap_base.prepare.assert_called_once_with(self.mock_engine)
        #self.mock_sessionmaker.assert_called_once_with(bind=self.mock_engine)
        #self.mock_session.query.assert_called_once()
        #self.mock_session.query().all.assert_called_once()
        #self.mock_session.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
