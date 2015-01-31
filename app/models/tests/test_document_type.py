from django.test import TestCase
from app.models.document_type import DocumentType

# Create your tests here.
class DemoTestCase(TestCase):
    fixtures = ['14_document_type']

    def test_get_type_exists(self):
        curType = DocumentType.objects.get(name='Offer Letter')
        self.assertIsNotNone(curType)
        self.assertEqual(curType.id, 1)
        self.assertEqual(curType.name, 'Offer Letter')
        self.assertIsNotNone(curType.default_content)
        
        curType = DocumentType.objects.get(name='Employment Agreement')
        self.assertIsNotNone(curType)
        self.assertEqual(curType.id, 2)
        self.assertEqual(curType.name, 'Employment Agreement')
        self.assertIsNotNone(curType.default_content)
        
        curType = DocumentType.objects.get(name='NDA')
        self.assertIsNotNone(curType)
        self.assertEqual(curType.id, 3)
        self.assertEqual(curType.name, 'NDA')
        self.assertIsNotNone(curType.default_content)

        curType = DocumentType.objects.get(name='COBRA')
        self.assertIsNotNone(curType)
        self.assertEqual(curType.id, 4)
        self.assertEqual(curType.name, 'COBRA')
        self.assertIsNotNone(curType.default_content)

        curType = DocumentType.objects.get(name='Employee Handbook')
        self.assertIsNotNone(curType)
        self.assertEqual(curType.id, 5)
        self.assertEqual(curType.name, 'Employee Handbook')
        self.assertIsNotNone(curType.default_content)

        curType = DocumentType.objects.get(name='Privacy Policy')
        self.assertIsNotNone(curType)
        self.assertEqual(curType.id, 6)
        self.assertEqual(curType.name, 'Privacy Policy')
        self.assertIsNotNone(curType.default_content)

    def test_get_type_non_exist(self):
        with self.assertRaises(DocumentType.DoesNotExist):
            curType = DocumentType.objects.get(name='non-existing-name')