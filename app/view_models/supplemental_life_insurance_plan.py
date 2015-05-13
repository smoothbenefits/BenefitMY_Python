from app.models.insurance.supplemental_life_insurance_plan import \
    SupplementalLifeInsurancePlan
from app.models.insurance.supplemental_life_insurance_plan_rate import \
    SupplementalLifeInsurancePlanRate

class SupplementalLifeInsurancePlanViewModel():

    def __init__(self, plan, plan_rates):

        self.plan = plan
        self.plan_rates = plan_rates
