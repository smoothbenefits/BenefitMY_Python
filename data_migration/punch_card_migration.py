import requests
from copy import deepcopy
from dateutil.parser import parse
import datetime
import sys

class TimePunchCardMigration(object):

    # Disable the request warnings
    requests.packages.urllib3.disable_warnings()
    
    week_day_map = {
        'sunday': 0,
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6
    }

    def __init__(self, comp_id, host_name):
        self.comp_id = comp_id
        self.host_name = host_name

    def execute(self):
        worksheets = self._get_company_users_time_punch_cards(self.comp_id)
        punch_cards = self._process_time_cards(worksheets)
        cards_count = len(punch_cards)
        print "Migrating {} punch cards".format(cards_count)
        for i in range(cards_count):
            print "{}".format(i),
            sys.stdout.flush()
            result = self._create_punch_card(punch_cards[i])
            if not result:
               break

    def get(self, url):
        return requests.get(url, verify=False)

    def post(self, url, data_object):
        return requests.post(url, json=data_object, verify=False)

    def _get_company_users_time_punch_cards(
        self,
        company_id
    ):
        user_punch_cards = []
        api_url = '{0}api/v1/company/{1}/work_timesheets'.format(
            self.host_name,
            company_id)

        r = self.get(api_url)
        if r.status_code == 404:
            return user_punch_cards

        all_entries = r.json()
        for entry in all_entries:
            user_punch_cards.append(entry)

        return user_punch_cards

    def _create_punch_card(self, punch_card):
        api_url = '{0}api/v1/time_punch_cards'.format(self.host_name)

        r = self.post(api_url, punch_card)

        if r.status_code == 200:
            return True
        else:
            print "ERROR {}".format(r.text)
            return False

    def _get_punch_card(self, date, employee, state, record_type, start, end, created, updated):
        punch_card = {}
        punch_card['employee'] = employee
        punch_card['date'] = date
        punch_card['start'] = start
        punch_card['end'] = end
        punch_card['recordType'] = self._map_record_type(record_type)
        punch_card['createdTimestamp'] = created
        punch_card['updatedTimestamp'] = updated
        punch_card['attributes'] = []
        punch_card['attributes'].append({'name': 'State' , 'value': state})
        return punch_card

    def _map_record_type(self, record_type):
        if record_type == 'Work Day':
            return 'Work Time'
        else:
            return record_type


    def _process_time_cards(self, worksheets):
        punch_cards = []
        for worksheet in worksheets:
            week_start_date = parse(worksheet['weekStartDate'])
            created = worksheet['createdTimestamp']
            updated = worksheet['updatedTimestamp']
            for timecard in worksheet['timecards']:
                state = timecard['tags'][0]['tagContent']
                for day_key in timecard['workHours']:
                    day_card = timecard['workHours'][day_key]
                    record_type = day_card.get('recordType', None)
                    start = day_card['timeRange']['start']
                    end = day_card['timeRange']['end']
                    if (record_type == 'Not a Work Day') or (not record_type and start == end):
                        continue
                    if not record_type:
                        record_type = 'Work Day'
                    # need to calculate date
                    # Add the week day delta
                    # Pad with 6 hours to count for UTC
                    date = week_start_date + datetime.timedelta(days=self.week_day_map[day_key]) + datetime.timedelta(hours=6)
                    record_type = day_card.get('recordType', 'Work Day')
                    punch_card = self._get_punch_card(
                        date.isoformat(),
                        deepcopy(worksheet['employee']),
                        state,
                        record_type,
                        start,
                        end,
                        created,
                        end)
                    punch_cards.append(punch_card)
        return punch_cards



if __name__ == "__main__":
    comp_id = 'production_BMHT_25_8e8541ac0b25ea272d9c586b21f40c49'
    host_name = 'https://timetracking.workbenefits.me/'
    migration = TimePunchCardMigration(comp_id, host_name)
    migration.execute()
    sys.exit(0)
