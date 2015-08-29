from app.view_models.view_model_base import ViewModelBase

class EmployeeAccountCreationInfo(ViewModelBase):
    user_id = None
    company_id = None
    company_user_type = None
    first_name = None
    last_name = None
    email = None
    employment_type = None
    compensation_info = None
    send_email = None
    password = None
    new_employee = None
    create_docs = None
    doc_fields = None
    annual_base_salary = None

    def __init__(self,
        user_id=None, company_id=None, company_user_type=None,
        first_name=None, last_name=None, email=None, employment_type=None,
        compensation_info=None, send_email=None, password=None,
        new_employee=None, create_docs=None, doc_fields=None,
        validation_issues=None):
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
        self.create_docs = create_docs
        self.doc_fields = doc_fields
        self.validation_issues = validation_issues
