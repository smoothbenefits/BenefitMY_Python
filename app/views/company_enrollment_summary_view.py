from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from app.service.hash_key_service import HashKeyService
from django.db import connection

from app.views.company_benefit_availability_view import CompanyBenefitAvailabilityView

from app.models.person import Person
from app.models.company_user import CompanyUser
from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.models.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.models.fsa.fsa import FSA
from app.models.hra.person_company_hra_plan import PersonCompanyHraPlan
from app.models.insurance.person_comp_suppl_life_insurance_plan import \
    PersonCompSupplLifeInsurancePlan
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.insurance.user_company_ltd_insurance_plan import \
    UserCompanyLtdInsurancePlan
from app.models.insurance.user_company_std_insurance_plan import \
    UserCompanyStdInsurancePlan

from app.serializers.person_serializer import PersonSerializer
from app.serializers.user_company_benefit_plan_option_serializer import \
    UserCompanyBenefitPlanOptionSerializer
from app.serializers.user_company_waived_benefit_serializer import \
    UserCompanyWaivedBenefitSerializer
from app.serializers.fsa.fsa_serializer import FsaSerializer
from app.serializers.hra.person_company_hra_plan_serializer import \
    PersonCompanyHraPlanSerializer
from app.serializers.insurance.person_company_supplemental_life_insurance_plan_serializer import \
    PersonCompanySupplementalLifeInsurancePlanSerializer
from app.serializers.insurance.user_company_life_insurance_serializer import \
    UserCompanyLifeInsuranceSerializer
from app.serializers.insurance.user_company_ltd_insurance_serializer import \
    UserCompanyLtdInsuranceSerializer
from app.serializers.insurance.user_company_std_insurance_serializer import \
    UserCompanyStdInsuranceSerializer

class CompanyEnrollmentSummaryView(APIView):
    def __init__(self):
        self.hash_service = HashKeyService()

    def _retrieve_started_count_from_DB(self, company_id):
        with connection.cursor() as cursor:
            cursor.execute("""select count(distinct cu.user_id) from app_companyuser cu 
left join app_person p on p.user_id=cu.user_id 
left join app_usercompanybenefitplanoption health on health.user_id = cu.user_id 
left join app_usercompanylifeinsuranceplan basic on basic.user_id = cu.user_id 
left join app_personcompsuppllifeinsuranceplan sp on sp.person_id = p.id 
left join app_usercompanyltdinsuranceplan ltd on ltd.user_id = cu.user_id 
left join app_usercompanystdinsuranceplan std on std.user_id=cu.user_id 
left join app_usercompanywaivedbenefit hwaive on hwaive.user_id = cu.user_id
left join app_personcompanyhraplan hra on hra.person_id = p.id
left join app_fsa fsa on fsa.user_id = cu.user_id
where cu.company_id = %s
and cu.company_user_type = 'employee' 
and p.id is not null 
and (health.id is not null 
     or basic.id is not null 
     or sp.id is not null 
     or ltd.id is not null 
     or std.id is not null 
     or hwaive.id is not null 
     or hra.id is not null 
     or fsa.id is not null);""", [company_id])

            row = cursor.fetchone()
            return row[0]

    def _retrieve_completed_count_from_DB(self, company_id): 
        with connection.cursor() as cursor:
            cursor.execute("""select count(distinct cu.user_id) from app_companyuser as cu 
left join app_person as p on p.user_id=cu.user_id
left join app_companybenefitplanoption as comphealth on comphealth.company_id = cu.company_id
left join app_usercompanybenefitplanoption as health on health.user_id = cu.user_id and comphealth.id = health.benefit_id
left join app_companylifeinsuranceplan as compbasic on compbasic.company_id = cu.company_id
left join app_usercompanylifeinsuranceplan as basic on basic.user_id = cu.user_id and basic.company_life_insurance_id = compbasic.id
left join app_compsuppllifeinsuranceplan as compsup on compsup.company_id = cu.company_id
left join app_personcompsuppllifeinsuranceplan as sp on sp.person_id = p.id and sp.company_supplemental_life_insurance_plan_id = compsup.id
left join app_companyltdinsuranceplan as compltd on compltd.company_id = cu.company_id
left join app_usercompanyltdinsuranceplan as ltd on ltd.user_id = cu.user_id and compltd.id = ltd.company_ltd_insurance_id
left join app_companystdinsuranceplan as compstd on compstd.company_id = cu.company_id
left join app_usercompanystdinsuranceplan as std on std.user_id=cu.user_id and compstd.id = std.company_std_insurance_id
left join app_companyhraplan as comphra on comphra.company_id = cu.company_id
left join app_personcompanyhraplan as hra on hra.person_id = p.id and hra.company_hra_plan_id = comphra.id
left join app_companyfsaplan as compfsa on compfsa.company_id = cu.company_id
left join app_fsa as fsa on fsa.user_id = cu.user_id and compfsa.id = fsa.company_fsa_plan_id
left join app_usercompanywaivedbenefit as hwaive on hwaive.user_id = cu.user_id
where cu.company_id = %s
and cu.company_user_type = 'employee' 
and p.id is not null 
and (comphealth.id is null or health.id is not null or hwaive.id is not null)
and (compbasic.id is null or basic.id is not null)
and (compsup.id is null or sp.id is not null)
and (compltd.id is null or ltd.id is not null)
and (compstd.id is null or std.id is not null)
and (comphra.id is null or hra.id is not null)
and (compfsa.id is null or fsa.id is not null);""", [company_id])
            row = cursor.fetchone()
            return row[0]

    def get(self, request, comp_id, format=None):

        started_count = self._retrieve_started_count_from_DB(comp_id)
        completed_count = self._retrieve_completed_count_from_DB(comp_id)

        response = {
            "enrollmentStarted": started_count,
            "enrollmentcompleted": completed_count
        }

        return Response(response)