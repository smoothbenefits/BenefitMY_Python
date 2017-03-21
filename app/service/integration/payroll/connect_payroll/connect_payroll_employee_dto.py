class ConnectPayrollEmployeeDto(object):
    def __init__(self):
        # System Data
        self.companyId = None
        self.payrollId = None
        self.timeClockId = None

        # Employee bio data and basic info
        self.ssn = None
        self.firstName = None
        self.middleName = None
        self.lastName = None
        self.suffix = None
        self.dob = ''
        self.gender = None
        self.martialStatus = None
        self.address1 = None
        self.address2 = None
        self.address3 = None
        self.city = None
        self.county = None
        self.country = None
        self.state = None
        self.zip = None
        self.email = None
        self.phone = None

        # Employment data
        self.payrollGroup = None
        self.businessUnit = None
        self.office = None
        self.department = None
        self.division = None
        self.union = None
        self.jobTitle = None
        self.fullTime = None
        self.statutoryClass = None
        self.seasonal = None
        self.hireDate = None
        self.hiredOn = None
        self.originalHireDate = None
        self.employeeStatus = None
        self.terminationDate = None
        self.terminatedOn = None
        self.terminationReason = None

        # Salary data
        self.payEffectiveDate = None
        self.annualBaseSalary = None
        self.baseHourlyRate = None
        self.hoursPerWeek = None  

        # Other
        self.usCitizen = None
        self.acaClassification = None           
