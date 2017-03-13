class ConnectPayrollEmployeeDto(object):
    def __init__(self):
        # System Data
        self.companyId = ''
        self.payrollId = ''
        self.timeClockId = ''

        # Employee bio data and basic info
        self.ssn = ''
        self.firstName = ''
        self.middleName = ''
        self.lastName = ''
        self.suffix = ''
        self.dob = ''
        self.gender = ''
        self.martialStatus = ''
        self.address1 = ''
        self.address2 = ''
        self.address3 = ''
        self.city = ''
        self.county = ''
        self.country = ''
        self.state = ''
        self.zip = ''
        self.email = ''
        self.phone = '' 

        # Employment data
        self.payrollGroup = ''
        self.businessUnit = ''
        self.office = ''
        self.department = ''
        self.division = ''
        self.union = ''
        self.jobTitle = ''
        self.fullTime = ''
        self.statutoryClass = ''
        self.seasonal = ''
        self.hireDate = ''
        self.hiredOn = ''
        self.originalHireDate = ''
        self.employeeStatus = ''
        self.terminationDate = ''
        self.terminatedOn = ''
        self.terminationReason = ''

        # Salary data
        self.payEffectiveDate = ''
        self.annualBaseSalary = ''
        self.baseHourlyRate = ''
        self.hoursPerWeek = ''  

        # Other
        self.usCitizen = ''
        self.acaClassification = ''           
