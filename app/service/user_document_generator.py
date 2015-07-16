import re
import time
import string
from app.custom_authentication import AuthUser as User
from app.models.document import Document
from app.models.document_type import DocumentType
from app.models.template import Template
from app.models.company import Company
from app.models.company_user import CompanyUser
from app.serializers.user_serializer import UserSerializer
from app.service.template_service import TemplateService



class UserDocumentGenerator(object):
    '''This is a service class to help auto generate all documents 
    for a specific user based on context information'''
    def __init__(self, company, user):
        self.user = user
        self.company = company
        self.template_service = TemplateService()
        self.default_value_dict = {
            'companyname': self._get_company_name_from_context,
            'company': self._get_company_name_from_context,
            'date': self._get_current_date,
            'currentdate': self._get_current_date,
            'hr': self._get_hr,
            'ourhrname':self._get_hr,
            'hrperson': self._get_hr
        }


    def _get_company_name_from_context(self):
        return self.company.name

    def _get_current_date(self):
        return time.strftime("%x")

    def _get_user_full_name(self, user):
        if user:
            user_serialized = UserSerializer(user)
            return user_serialized.data['first_name'] + ' ' + user_serialized.data['last_name']
        else:
            return ''

    def _get_hr(self):
        com_users = CompanyUser.objects.filter(company=self.company, company_user_type='admin')
        if com_users:
            admin = com_users[0]
            return self._get_user_full_name(admin.user)
        else:
            return ''

    def get_all_template_fields(self):
        field_keys = []
        for d_type in DocumentType.objects.all():
            content = self.template_service.get_most_recent_content_by_doc_type(d_type, self.company)
            if content:
                field_keys += self.template_service.get_field_keys_from_template_content(content)

        fields = {}
        field_keys = self.template_service.dedupe_field_keys(field_keys)
        for key in field_keys:
            if key in self.default_value_dict:
                fields[key] = self.default_value_dict[key]()
            else:
                fields[key] = ''
        return fields

    def generate_all_document(self, field_values):
        for d_type in DocumentType.objects.all():
            # For each document type
            # We need to get the template associated with the document type
            content = self.template_service.get_most_recent_content_by_doc_type(d_type, self.company)
            if not content:
                # We cannot find the proper template, skip
                continue
            doc_name = "{} for employee".format(d_type.name) 
            content = self.template_service.populate_content_with_field_values(content, field_values)
            #Create a new document based on type
            doc = Document(company_id=self.company.id,
                           user_id=self.user.id,
                           document_type=d_type,
                           name=doc_name,
                           content=content,
                           signature=None
                          ) 
            doc.save()
