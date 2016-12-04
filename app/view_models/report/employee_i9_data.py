from app.models.employment_authorization import (
    WORKER_TYPE_CITIZEN,
    WORKER_TYPE_NONCITIZEN,
    WORKER_TYPE_PERM_RESIDENT,
    WORKER_TYPE_AAW
)

class EmployeeI9Data(object):

    def __init__(self, employee_authorization):
        self.citizen_data = None
        self.non_citizen_data = None
        self.perm_resident_data = None
        self.authorized_worker_data = None
            
        if (employee_authorization):
            if (employee_authorization.worker_type == WORKER_TYPE_CITIZEN):
                self.citizen_data = {}
            elif(employee_authorization.worker_type == WORKER_TYPE_NONCITIZEN):
                self.non_citizen_data = {}
            elif(employee_authorization.worker_type == WORKER_TYPE_PERM_RESIDENT):
                self.perm_resident_data = {
                    'uscis_number': employee_authorization.uscis_number
                }
            elif(employee_authorization.worker_type == WORKER_TYPE_AAW):
                expiration_date = 'N/A'
                if (employee_authorization.expiration_date):
                    expiration_date = employee_authorization.expiration_date.strftime('%m/%d/%Y')
                self.authorized_worker_data = {
                    'expiration_date': expiration_date,
                    'uscis_number': employee_authorization.uscis_number,
                    'i94_number': employee_authorization.i_94,
                    'passport_number': employee_authorization.passport,
                    'country_of_issuance': employee_authorization.country
                }
            else:
                raise ValueError("Given employee has a worker type that is not recognized!") 

            self.signature_date = employee_authorization.signature.created_at.strftime('%m/%d/%Y')
