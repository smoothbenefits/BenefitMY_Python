from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.models.company import Company
from app.models.company_user import CompanyUser
from app.service.hash_key_service import HashKeyService


class CompanyEnrollmentSummaryView(APIView):
    def __init__(self):
        self.hash_service = HashKeyService()

    def _retrieve_not_started_from_DB(self, company_id):
        with connection.cursor() as cursor:
            cursor.execute("""select distinct cu.user_id, COALESCE(p.first_name, u.first_name), COALESCE(p.last_name, u.last_name)
from app_companyuser cu
join app_authuser u on u.id = cu.user_id
left join app_person p on p.user_id=cu.user_id and p.relationship='self'
left join app_usercompanybenefitplanoption health on health.user_id = cu.user_id
left join app_usercompanylifeinsuranceplan basic on basic.user_id = cu.user_id
left join app_personcompsuppllifeinsuranceplan sp on sp.person_id = p.id
left join app_usercompanyltdinsuranceplan ltd on ltd.user_id = cu.user_id
left join app_usercompanystdinsuranceplan std on std.user_id=cu.user_id
left join app_usercompanywaivedbenefit hwaive on hwaive.user_id = cu.user_id
left join app_personcompanyhraplan hra on hra.person_id = p.id
left join app_fsa fsa on fsa.user_id = cu.user_id
left join app_personcompanygrouphsaplan hsa on hsa.person_id = p.id
where cu.company_id = %s
and cu.company_user_type = 'employee'
and (p.id is null
or
(health.id is null
 and basic.id is null
 and sp.id is null
 and ltd.id is null
 and std.id is null
 and hwaive.id is null
 and hra.id is null
 and fsa.id is null
 and hsa.id is null))""", [company_id])
            rows = cursor.fetchall()
            return self._convert_db_rows_to_list(rows)

    def _retrieve_started_from_DB(self, company_id):
        with connection.cursor() as cursor:
            cursor.execute("""select distinct cu.user_id, p.first_name, p.last_name
from app_companyuser cu
join app_person p on p.user_id=cu.user_id and p.relationship='self'
left join app_usercompanybenefitplanoption health on health.user_id = cu.user_id
left join app_usercompanylifeinsuranceplan basic on basic.user_id = cu.user_id
left join app_personcompsuppllifeinsuranceplan sp on sp.person_id = p.id
left join app_usercompanyltdinsuranceplan ltd on ltd.user_id = cu.user_id
left join app_usercompanystdinsuranceplan std on std.user_id=cu.user_id
left join app_usercompanywaivedbenefit hwaive on hwaive.user_id = cu.user_id
left join app_personcompanyhraplan hra on hra.person_id = p.id
left join app_fsa fsa on fsa.user_id = cu.user_id
left join app_personcompanygrouphsaplan hsa on hsa.person_id = p.id
where cu.company_id = %s
and cu.company_user_type = 'employee'
and (health.id is not null
     or basic.id is not null
     or sp.id is not null
     or ltd.id is not null
     or std.id is not null
     or hwaive.id is not null
     or hra.id is not null
     or fsa.id is not null
     or hsa.id is not null);""", [company_id])

            rows = cursor.fetchall()
            return self._convert_db_rows_to_list(rows)

    def _retrieve_completed_from_DB(self, company_id):
        with connection.cursor() as cursor:
            cursor.execute("""select distinct cu.user_id, p.first_name, p.last_name
from app_companyuser as cu
join app_person as p on p.user_id=cu.user_id and p.relationship='self'
join app_companygroupmember as cgm on cgm.user_id = cu.user_id
left join app_companygroupbenefitplanoption as compgrouphealth on compgrouphealth.company_group_id = cgm.company_group_id
left join app_companybenefitplanoption as comphealth on comphealth.id = compgrouphealth.company_benefit_plan_option_id
left join app_usercompanybenefitplanoption as health on health.user_id = cu.user_id and comphealth.id = health.benefit_id
left join app_companygroupbasiclifeinsuranceplan as compbasic on compbasic.company_group_id = cgm.company_group_id
left join app_usercompanylifeinsuranceplan as basic on basic.user_id = cu.user_id
left join app_companygroupsuppllifeinsuranceplan as compsup on compsup.company_group_id = cgm.company_group_id
left join app_personcompsuppllifeinsuranceplan as sp on sp.person_id = p.id
left join app_companyltdinsuranceplan as compltd on compltd.company_id = cu.company_id
left join app_usercompanyltdinsuranceplan as ltd on ltd.user_id = cu.user_id
left join app_companygroupstdinsuranceplan as compgstd on compgstd.company_group_id = cgm.company_group_id
left join app_usercompanystdinsuranceplan as std on std.user_id=cu.user_id
left join app_companyhraplan as comphra on comphra.company_id = cu.company_id
left join app_personcompanyhraplan as hra on hra.person_id = p.id
left join app_companyfsaplan as compfsa on compfsa.company_id = cu.company_id
left join app_fsa as fsa on fsa.user_id = cu.user_id
left join app_personcompanygrouphsaplan as hsa on hsa.person_id = p.id
left join app_companygrouphsaplan as comphsa on comphsa.company_group_id = cgm.company_group_id
left join app_usercompanywaivedbenefit as hwaive on hwaive.user_id = cu.user_id
where cu.company_id = %s
and cu.company_user_type = 'employee'
and (comphealth.id is null or health.id is not null or hwaive.id is not null)
and (compbasic.id is null or basic.id is not null)
and (compsup.id is null or sp.id is not null)
and (compltd.id is null or ltd.id is not null)
and (compstd.id is null or std.id is not null)
and (comphra.id is null or hra.id is not null)
and (compfsa.id is null or fsa.id is not null)
and (comphsa.id is null or hsa.id is not null);""", [company_id])
            rows = cursor.fetchall()
            return self._convert_db_rows_to_list(rows)

    def _convert_db_rows_to_list(self, rows):
        list = []
        for row in rows:
            list.append({"id": self.hash_service.encode_key(row[0]),
                         "firstName": row[1],
                         "lastName": row[2]})
        return list

    def get(self, request, comp_id, format=None):
        if not Company.objects.filter(pk=comp_id).exists():
            raise Http404
        not_started = self._retrieve_not_started_from_DB(comp_id)
        started = self._retrieve_started_from_DB(comp_id)
        completed = self._retrieve_completed_from_DB(comp_id)

        not_complete = []
        for start_user in started:
            if not start_user in completed:
                not_complete.append(start_user)

        totalCount = CompanyUser.objects.filter(company=comp_id, company_user_type='employee').count()

        response = {
            "enrollmentNotStarted": not_started,
            "enrollmentNotComplete": not_complete,
            "enrollmentCompleted": completed,
            "totalEmployeeCount": totalCount
        }

        return Response(response)
