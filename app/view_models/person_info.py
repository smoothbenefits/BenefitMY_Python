from app.service.compensation_service import CompensationService


class PersonInfo(object):
    first_name = ''
    last_name = ''
    birth_date = ''
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

            if (person_model.last_name):
                self.last_name = person_model.last_name
            elif (person_model.user.last_name):
                self.last_name = person_model.user.last_name

            self.ssn = person_model.ssn
            self.birth_date = person_model.birth_date

            if (person_model.email):
                self.email = person_model.email
            elif (person_model.user.email):
                self.email = person_model.user.email

            self.phones = []
            for phone in person_model.phones.all():
                self.phones.append({
                    'type': phone.phone_type,
                    'number': phone.number})

            addresses = person_model.addresses.filter(address_type='home')
            if (len(addresses) > 0):
                address = addresses[0]
                self.address1 = address.street_1
                self.address2 = address.street_2
                self.city = address.city
                self.state = address.state
                self.zipcode = address.zipcode

            # initialize compensation service for use later
            self.compensation_service = CompensationService(person_model.id)

    def get_full_name(self):
        if self.first_name is not None and self.last_name is not None:
            return self.first_name + ' ' + self.last_name
        return None

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

    def get_current_compensation(self):
        result = ''
        curr_salary = self.compensation_service.get_current_annual_salary()
        if (curr_salary):
            result = "$%.2f" % curr_salary
        return result

    def get_current_hourly_rate(self):
        result = self.compensation_service.get_current_hourly_rate()
        if (result):
            result = round(result, 2)
        return result

    def get_ssn_tokenized(self):
        if (not self.ssn):
            return None

        return [
            self.ssn[:3],
            self.ssn[3:5],
            self.ssn[5:]
        ]
