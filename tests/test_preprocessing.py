from crawler.preprocessing import PreProcessing
import json
from utils.logger import Logger

logger = Logger.get_logger()

class TestPreprocessing:
    def test_remove_html_tag(self):
        with open('tests/test_input/test_input_processing.json') as file:
            test = json.load(file)

        legal_text = test['input']
        expected_result = test['expected_result']
        preprocessor = PreProcessing()
        logger.info(f'Raw text:\n {legal_text}')
        removed_text = preprocessor.remove_html_tag(legal_text)
        logger.info(f'Processed text:\n {removed_text}')

        assert legal_text == expected_result
