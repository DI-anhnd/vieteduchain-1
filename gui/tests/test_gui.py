import unittest
from gui.app.main import create_app

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to VietEduChain', response.data)

    def test_educert_view(self):
        response = self.client.get('/educert')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EduCert', response.data)

    def test_eduid_view(self):
        response = self.client.get('/eduid')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EduID', response.data)

    def test_edupay_view(self):
        response = self.client.get('/edupay')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EduPay', response.data)

    def test_researchledger_view(self):
        response = self.client.get('/researchledger')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ResearchLedger', response.data)

    def test_eduadmission_view(self):
        response = self.client.get('/eduadmission')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EduAdmission', response.data)

if __name__ == '__main__':
    unittest.main()