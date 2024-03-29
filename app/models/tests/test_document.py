# test document
# tests can be kicked off by running "python manage.py test app/tests/"
from django.test import TestCase
from app.models.health_benefits.benefit_type import BenefitType
from app.models.health_benefits.benefit_plan import BenefitPlan

# Create your tests here.
class DemoTestCase(TestCase):
    fixtures = ['13_benefit_type']

    def setUp(self):
        benefitType = BenefitType.objects.get(name='Medical')
        BenefitPlan.objects.create(name='test', benefit_type=benefitType)

    def test_new_plan_created(self):
        newPlan = BenefitPlan.objects.get(name='test')
        self.assertEqual(newPlan.name, 'test')

    def test_get_a_plan(self):
        newPlan = BenefitPlan.objects.get(name='test')
        plan = BenefitPlan.objects.get(pk=newPlan.id)
        self.assertEqual(plan.benefit_type.name, 'Medical')
