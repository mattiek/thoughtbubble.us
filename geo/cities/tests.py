from django.test import TestCase

from models import City


class CityTestCase(TestCase):
    pass

    # def setUp(self):
    #     Organization.objects.create(
    #         title='Organization 1',
    #         )
    #
    #     Organization.objects.create(
    #         title='Organization 2',
    #         )
    #
    # def test_organization_can_exist(self):
    #     """Organizations are there"""
    #     org1 = Organization.objects.filter(title="Organization 1")
    #     org2 = Organization.objects.filter(title="Organization 2")
    #     self.assertNotEqual(org1, None)
    #     self.assertNotEqual(org2, None)