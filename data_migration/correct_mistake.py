import requests
from copy import deepcopy
from dateutil.parser import parse
import datetime
import sys

class CorrectMistake(object):

    # Disable the request warnings
    requests.packages.urllib3.disable_warnings()
    

    def __init__(self, comp_id, host_name):
        self.comp_id = comp_id
        self.host_name = host_name

    def execute(self):
        cards = self._get_company_users_time_punch_cards(self.comp_id)
        deleted = 0
        for card in cards:
            if not self._find_project_attribute(card['attributes']):
                deleted += 1
                result = self._delete_card(card)
                if not result:
                    break
                print deleted,
                sys.stdout.flush()
        print "deleted {} cards".format(deleted)

    def _find_project_attribute(self, attributes):
        project_exist = False
        for attr in attributes:
            if attr['name'] == 'Project' or attr['name'] == 'HourlyRate':
                project_exist = True
                print "project exists! "
                break
        return project_exist

    def _get_company_users_time_punch_cards(
        self,
        company_id
    ):
        user_punch_cards = []
        api_url = '{0}api/v1/company/{1}/time_punch_cards'.format(
            self.host_name,
            company_id)

        r = self.get(api_url)
        if r.status_code == 404:
            return user_punch_cards

        all_entries = r.json()
        for entry in all_entries:
            user_punch_cards.append(entry)

        return user_punch_cards

    def get(self, url):
        return requests.get(url, verify=False)

    def post(self, url, data_object):
        return requests.post(url, json=data_object, verify=False)

    def delete(self, url):
        return requests.delete(url, verify=False)

    def _delete_card(self, punch_card):
        api_url = '{0}api/v1/time_punch_cards/{1}'.format(self.host_name, punch_card['_id'])

        r = self.delete(api_url)

        if r.status_code == 200:
            return True
        else:
            print "ERROR {}".format(r.text)
            return False


if __name__ == "__main__":
    comp_id = 'production_BMHT_26_a695dcce7822e21e0e73a66e908e18fa'
    host_name = 'https://timetracking.workbenefits.me/'
    migration = CorrectMistake(comp_id, host_name)
    migration.execute()
    sys.exit(0)
