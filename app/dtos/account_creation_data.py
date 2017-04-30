class AccountCreationData(object):
    def __init__(self,
        user_id=None, company_id=None, company_user_type=None,
        first_name=None, last_name=None, email=None, employment_type=None,
        compensation_info=None, send_email=None, password=None,
        new_employee=None, start_date=None, benefit_start_date=None, create_docs=None, doc_fields=None,
        group_id=None, group_name=None, manager_id=None, manager_first_name=None,
        manager_last_name=None, employee_number=None, pin=None):
        self.user_id = user_id
        self.company_id = company_id
        self.company_user_type = company_user_type
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.employment_type = employment_type
        self.compensation_info = compensation_info
        self.send_email = send_email
        self.password = password
        self.new_employee = new_employee
        self.start_date = start_date
        self.benefit_start_date = benefit_start_date
        self.create_docs = create_docs
        self.doc_fields = doc_fields
        self.group_id = group_id
        self.group_name = group_name
        self.manager_id = manager_id
        self.manager_first_name = manager_first_name
        self.manager_last_name = manager_last_name
        self.employee_number = employee_number
        self.pin = pin
