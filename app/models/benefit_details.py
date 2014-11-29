from django.db import models
from benefit_policy_key import BenefitPolicyKey
from benefit_policy_type import BenefitPolicyType
from company_benefit_plan_option import CompanyBenefitPlanOption

class BenefitDetails(models.Model):
    value = models.CharField(max_length=1024)

    benefit_policy_key = models.ForeignKey(BenefitPolicyKey,
        related_name="benefit_details",
        blank=True,
        null=True)
    benefit_policy_type = models.ForeignKey(BenefitPolicyType,
        related_name="benefit_details",
        blank=True,
        null=True)

    benefit_plan = models.ForeignKey(CompanyBenefitPlanOption,
                                     related_name="benefit_details",
                                     blank=True,
                                     null=True)
