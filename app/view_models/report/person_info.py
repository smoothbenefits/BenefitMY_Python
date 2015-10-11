class PersonInfo(object):
    first_name = ''
    last_name = ''
    ssn = ''
    address1 = ''
    address2 = ''
    city = ''
    state = ''
    zipcode = ''
    country = 'USA'

    def __init__(self, person_model):
        if (person_model):
            self.first_name = person_model.first_name
            self.last_name = person_model.last_name
            self.ssn = person_model.ssn

            addresses = person_model.addresses.filter(address_type='home')
            if (len(addresses) > 0):
                address = addresses[0]
                self.address1 = address.street_1
                self.address2 = address.street_2
                self.city = address.city
                self.state = address.state
                self.zipcode = address.zipcode

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

    def get_country_and_zipcode(self):
        result = None
        if (self.country is not None):
            result = self.country
            if (self.zipcode is not None):
                result = result + ' ' + self.zipcode
        return result
