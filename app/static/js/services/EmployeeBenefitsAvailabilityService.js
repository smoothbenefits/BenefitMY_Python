var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EmployeeBenefitsAvailabilityService',
  ['$q',
   'EmployeeProfileService',
   'CompanyBenefitAvailabilityService',
   'CompanyFeatureService',
   function EmployeeBenefitsAvailabilityService(
     $q,
     EmployeeProfileService,
     CompanyBenefitAvailabilityService,
     CompanyFeatureService){

     var getEmployeeAvailableBenefits = function(companyId, userId){
        var deferred = $q.defer();
        //First we get the employee profile
        EmployeeProfileService.getEmployeeProfileForCompanyUser(companyId, userId)
        .then(function(employeeProfile){
            var isFullTime = EmployeeProfileService.isFullTimeEmploymentType(employeeProfile);
            CompanyFeatureService.getAllApplicationFeatureStatusByCompany(companyId)
            .then(function(allFeatureStatus){  
                if(isFullTime || !allFeatureStatus.isFeatureEnabled(CompanyFeatureService.AppFeatureNames.BenefitsForFullTimeOnly)){
                    CompanyBenefitAvailabilityService.getBenefitAvailabilityForUser(companyId, userId)
                    .then(function(companyBenefits) {
                        deferred.resolve(companyBenefits);
                    });
                }
                else{
                    deferred.resolve(null);
                }
            });  
        }, function(error){
            deferred.reject(error);
        });
        return deferred.promise;
     };

     return{
         getEmployeeAvailableBenefits : getEmployeeAvailableBenefits
     };
   }
]);

