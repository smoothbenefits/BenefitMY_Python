from django.conf import settings
from django.contrib.auth import get_user_model

from app.service.hash_key_service import HashKeyService
from app.service.web_request_service import WebRequestService

PROJECT_STATUS_ACTIVE = 'Active'
PROJECT_STATUS_INACTIVE = 'Inactive'

User = get_user_model()


API_URL_COI = '{0}{1}'.format(
    settings.COI_SERVICE_URL,
    'api/v1'
)


class ProjectService(object):

    hash_key_service = HashKeyService()
    request_service = WebRequestService()

    def get_projects_by_company(self, company_id, active_only=False):
        api_url = '{0}/company/{1}/projects'.format(
                        API_URL_COI,
                        self.hash_key_service.encode_key_with_environment(company_id))

        # Make the request and parse the response as json
        r = self.request_service.get(api_url)
        projects = r.json()

        if (active_only):
            filtered = []
            for project in projects:
                if (project['status'] == PROJECT_STATUS_ACTIVE):
                    filtered.append(project)
            projects = filtered

        view_models = []

        for project in projects:
            view_models.append(self._map_domain_to_view_model(project))

        return view_models

    def _map_domain_to_view_model(self, domain_model):
        return {
            'project_id': domain_model['_id'],
            'name': domain_model['name'],
            'status': domain_model['status']
        }
