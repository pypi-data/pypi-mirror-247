import unittest
from unittest.mock import patch, Mock
from cmhlims.getAnalysisFiles import get_analysis_files
import pandas as pd

class TestGetAnalysisFiles(unittest.TestCase):
    @patch('cmhlims.getAnalysis.connect_to_lims')
    @patch('cmhlims.getAnalysis.MetaData')
    @patch('cmhlims.getAnalysis.automap_base')
    @patch('cmhlims.getAnalysis.sessionmaker')
    def test_get_analysis_files(self, mock_sessionmaker, mock_automap_base, mock_metadata, mock_connect_to_lims):
        # Mocking the necessary objects
        mock_engine = Mock()
        mock_session = Mock()
        mock_analysis_files_class = Mock()
        mock_analysis_file_types_class = Mock()
        mock_downstream_analyses_class = Mock()

        mock_connect_to_lims.return_value = mock_engine
        mock_metadata.return_value = mock_metadata
        mock_automap_base.return_value = mock_analysis_files_class
        mock_sessionmaker.return_value = mock_session

        # Mocking the behavior of the query
        mock_result = [('file1.txt', 2287, 'Label1', 'Abbrev1'), ('file2.txt', 2287, 'Label2', 'Abbrev2')]
        mock_session.query().all.return_value = mock_result

        # Calling the function
        result = get_analysis_files(analysis_ids=["2287"])

        # Assertions
        expected_df = pd.DataFrame(mock_result, columns=['file_path', 'analysis_id', 'file_type_label', 'file_type_abbrev'])
        #pd.testing.assert_frame_equal(result, expected_df)

        #mock_connect_to_lims.assert_called_once()
        #mock_metadata.reflect.assert_called_once_with(mock_engine, only=['downstream_analysis_files', 'downstream_analysis_file_types', 'downstream_analyses'])
        #mock_automap_base.prepare.assert_called_once_with(mock_engine)
        #mock_sessionmaker.assert_called_once_with(bind=mock_engine)
        #mock_session.query.assert_called_once()
        #mock_session.query().all.assert_called_once()
        #mock_session.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()