class CompanyInfo(object):
    company_name = ''
    ein = ''
    address1 = ''
    address2 = ''
    city = ''
    state = ''
    zipcode = ''
    contact_phone = ''
    country = 'USA'
    offer_of_coverage_code = ''

    def __init__(self, company_model):
        if (company_model):
            self.company_name = company_model.name
            self.ein = company_model.ein
            self.offer_of_coverage_code = company_model.offer_of_coverage_code

            addresses = company_model.addresses.filter(address_type='main')
            if (len(addresses) > 0):
                address = addresses[0]
                self.address1 = address.street_1
                self.address2 = address.street_2
                self.city = address.city
                self.state = address.state
                self.zipcode = address.zipcode

            contacts = company_model.contacts.all()
            if (len(contacts) > 0):
                contact = contacts[0]
                phones = contact.phones.filter(phone_type='work')
                if (len(phones) > 0):
                    self.contact_phone = phones[0].number

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
