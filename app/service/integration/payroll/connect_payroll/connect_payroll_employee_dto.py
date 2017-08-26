class ConnectPayrollEmployeeDto(object):
    def __init__(self):
        # System Data
        self.companyId = None
        self.payrollId = None

        # Employee bio data and basic info
        self.ssn = None
        self.firstName = None
        self.middleName = None
        self.lastName = None
        self.dob = ''
        self.gender = None
        self.martialStatus = None
        self.address1 = None
        self.address2 = None
        self.city = None
        self.country = None
        self.state = None
        self.zip = None
        self.email = None
        self.phone = None

        # Employment data
        self.department = None
        self.division = None
        self.union = None
        self.jobTitle = None
        self.fullTime = None
        self.seasonal = None
        self.hireDate = None
        self.originalHireDate = None
        self.employeeStatus = None
        self.terminationDate = None

        # Salary data
        self.payEffectiveDate = None
        self.annualBaseSalary = None
        self.baseHourlyRate = None          
