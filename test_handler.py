import unittest
import warnings

from src.handler import process

class TestHandler(unittest.TestCase):
    
    ENCRYPTED_PDF_FILE_URL = 'https://tradecred-website-assets.s3.ap-south-1.amazonaws.com/encrypted-asset.pdf'
    # ENCRYPTED_PDF_FILE_URL = 'https://tradecred-website-assets.s3.ap-south-1.amazonaws.com/decrypted-asset.pdf'
    PASSWORD = 'PART1998'
    # PASSWORD = None
    FORMAT = 'image'
    # FORMAT = 'pdf'

    def test_process(self):
        warnings.simplefilter("ignore", ResourceWarning)
        warnings.simplefilter("ignore", DeprecationWarning)

        return_msg, return_flag, return_service = process(self.ENCRYPTED_PDF_FILE_URL,self.PASSWORD,self.FORMAT)
        print('\n',return_msg, return_flag, return_service)
        # self.assertEqual(''.join(return_msg['aadhaar_numbers']),'580281721851', 'Wrong aadhaar number identified')
        # self.assertEqual(''.join(return_msg['phone_numbers']),'9837827300', 'Wrong phone number identified')

if __name__ == '__main__':
    unittest.main()
