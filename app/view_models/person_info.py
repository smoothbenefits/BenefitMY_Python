from app.service.compensation_service import CompensationService


class PersonInfo(object):
    first_name = ''
    middle_name = ''
    last_name = ''
    birth_date = ''
    gender = ''
    ssn = ''
    email = ''
    phones = []
    address1 = ''
    address2 = ''
    city = ''
    state = ''
    zipcode = ''
    country = 'USA'

    def __init__(self, person_model):
        if (person_model):
            if (person_model.first_name):
                self.first_name = person_model.first_name
            elif (person_model.user.first_name):
                self.first_name = person_model.user.first_name

            if (person_model.middle_name):
                self.middle_name = person_model.middle_name

            if (person_model.last_name):
                self.last_name = person_model.last_name
            elif (person_model.user.last_name):
                self.last_name = person_model.user.last_name

            if (person_model.ssn):
                self.ssn = person_model.ssn

            if (person_model.birth_date):
                self.birth_date = person_model.birth_date

            if (person_model.gender):
                self.gender = person_model.gender

            if (person_model.email):
                self.email = person_model.email
            elif (person_model.user.email):
                self.email = person_model.user.email

            self.phones = []
            for phone in person_model.phones.all():
                self.phones.append({
                    'type': phone.phone_type,
                    'number': phone.number})

            addresses = list(person_model.addresses.all())
            home_addresses = [a for a in addresses if a.address_type == 'home']
            if (len(home_addresses) > 0):
                address = home_addresses[0]
                self.address1 = address.street_1
                self.address2 = address.street_2
                self.city = address.city
                self.state = address.state
                self.zipcode = address.zipcode

    def get_full_name(self, include_middle_name=True):
        result = ''
        
        if (self.first_name):
            result = '{0}'.format(self.first_name)

        if (include_middle_name and self.middle_name):
            result = '{0} {1}'.format(result, self.middle_name)

        if (self.last_name):
            result = '{0} {1}'.format(result, self.last_name)
        
        return result

    def get_full_street_address(self):
        full_address = None
        if (self.address1 is not None):
            full_address = self.address1
            if (self.address2 is not None):
                full_address = full_address + ', ' + self.address2
        return full_address

    def get_city_state_zipcode(self):
        return self.city + ', ' + self.state + ' ' + self.zipcode

    def get_country_and_zipcode(self):
        result = None
        if (self.country is not None):
            result = self.country
            if (self.zipcode is not None):
                result = result + ' ' + self.zipcode
        return result

    def get_ssn_tokenized(self):
        if (not self.ssn):
            return [
                '',
                '',
                ''
            ]

        return [
            self.ssn[:3],
            self.ssn[3:5],
            self.ssn[5:]
        ]

    def get_zipcode_and_extension(self):
        if (not self.zipcode):
            return ['', '']

        tokens = self.zipcode.split('-')
        if (len(tokens) == 1):
            return [tokens[0], '']

        return tokens
