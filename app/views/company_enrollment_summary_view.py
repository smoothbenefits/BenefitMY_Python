from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.models.company import Company


class CompanyEnrollmentSummaryView(APIView):

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
        if not Company.objects.filter(pk=comp_id).exists():
            raise Http404

        started_count = self._retrieve_started_count_from_DB(comp_id)
        completed_count = self._retrieve_completed_count_from_DB(comp_id)

        response = {
            "enrollmentStarted": started_count,
            "enrollmentcompleted": completed_count
        }

        return Response(response)
