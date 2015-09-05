import re
import time
import string

from app.models.document_type import DocumentType
from app.models.template import Template


class TemplateService(object):
    '''This is a service class that helps the system to
       process template related logic and data'''
    def dump_down_key_name(self, key_name):
        return key_name.lower().translate('_').replace(" ", "")

    def get_most_recent_content_by_doc_type(self, doc_type, company):
        templates = Template.objects.filter(document_type=doc_type, company=company).order_by('-id')
        if templates:
            return templates[0].content
        return None

    def get_field_keys_from_template_content(self, content):
        field_keys = []
        if content:
            field_keys += re.findall('{{(.*?)}}', content)
            return field_keys
        else:
            return None

    def dedupe_field_keys(self, field_keys):
        deduped_keys = []
        for key in field_keys:
            deduped_key = self.dump_down_key_name(key)
            if deduped_key not in deduped_keys:
                deduped_keys.append(deduped_key)
        return deduped_keys

    def populate_content_with_field_values(self, content, field_values):
        field_keys = self.get_field_keys_from_template_content(content)
        value = ""
        if field_values:
            for key in field_keys:
                for value_pair in field_values:
                    if self.dump_down_key_name(key) == self.dump_down_key_name(value_pair.key):
                        value = value_pair.value
                        break
                content = content.replace("{{%s}}" % key, value)
        return content
