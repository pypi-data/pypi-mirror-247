import os
import unittest
from mindhive.brainstem import get_current_timestamp, get_mindhive_path, log_status, peek_at_memory
from mindhive.core_cortex import MemoryType


# Test the path to the mindhive directory
class TestGetMindhivePath(unittest.TestCase):
    def test_get_mindhive_path(self):
        self.assertTrue(os.path.exists(get_mindhive_path()))

    def test_get_current_timestamp(self):
        self.assertIsNotNone(get_current_timestamp())

    def test_log_status(self):
        log_status('Test log status')  # Just make sure it doesn't crash

    def test_peek_at_memory(self):
        peek_at_memory(MemoryType.EPHEMERAL,memory= 'Fake Memory')

if __name__ == '__main__':
    unittest.main()



