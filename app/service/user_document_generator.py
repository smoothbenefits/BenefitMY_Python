import re
import time
import string
from app.models.user import User
from app.models.document import Document
from app.models.document_type import DocumentType
from app.models.template import Template
from app.models.company import Company


class UserDocumentGenerator(object):
    '''This is a service class to help auto generate all documents 
    for a specific user based on context information'''
    def __init__(self, company, user):
        self.user = user
        self.company = company
        self.default_value_dict = {
            'companyname': self._get_company_name_from_context,
            'date': self._get_current_date,
        }


    def _get_company_name_from_context(self):
        return self.company.name

    def _get_current_date(self):
        return time.strftime("%x")

    def _get_latest_template_content_by_doc_type(self, doc_type):
        templates = Template.objects.filter(document_type=doc_type).order_by('-id')
        if templates:
            return templates[0].content
        return doc_type.default_content

    def get_all_template_fields(self):
        field_keys = []
        for d_type in DocumentType.objects.all():
            content = self._get_latest_template_content_by_doc_type(d_type)
            field_keys += re.findall('{{(.*?)}}', content)

        fields = {}
        for key in field_keys:
            processed_key = key.lower().translate('_')
            if processed_key in self.default_value_dict:
                fields[key] = self.default_value_dict[processed_key]()
            else:
                fields[key] = ''
        return fields


    def generate_all_document(self, field_values):
        print "Calling in create all docs"
        for d_type in DocumentType.objects.all():
            print "start to create document for {}".format(d_type.name)
            # For each document type
            # We need to get the template associated with the document type
            content = self._get_latest_template_content_by_doc_type(d_type)
            doc_name = "{} for {}".format(d_type.name, self.user.email) 
            field_names = re.findall('{{(.*?)}}', content)
            value = ""
            for field_key in field_names:
                for value_pair in field_values:
                    if field_key == value_pair['key']:
                        value = value_pair['value']
                        break
                content = content.replace("{{%s}}" % field_key, value)
            print "Finished replacing all the content: {}".format(content)
            #Create a new document based on type
            doc = Document(company_id=self.company.id,
                           user_id=self.user.id,
                           document_type=d_type,
                           name=doc_name,
                           content=content,
                           signature=None
                          ) 
            doc.save()
            print "document saved!"
