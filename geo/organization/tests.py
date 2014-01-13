from django.test import TestCase

from models import Organization


class OrganizationTestCase(TestCase):

    def setUp(self):
        Organization.objects.create(
            title='Organization 1',
        )

        Organization.objects.create(
            title='Organization 2',
            )

    def test_organization_can_exist(self):
        """Organizations are there"""
        org1 = Organization.objects.filter(title="Organization 1")
        org2 = Organization.objects.filter(title="Organization 2")
        self.assertNotEqual(org1, None)
        self.assertNotEqual(org2, None)


#City.objects.filter(geom__distance_lte=(j.geom, D(mi=3)))