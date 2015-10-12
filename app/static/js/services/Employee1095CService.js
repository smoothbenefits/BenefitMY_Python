var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('Employee1095CService', [
  '$q', 'Employee1095CDataRepository', 'Company1095CService',
  function ($q, Employee1095CDataRepository, Company1095CService){

    var PASS_VALIDATION = 'PASSED';

    var mapToModelObject = function(view1095CData, personId, companyId){
      modelObj = [];
      _.each(view1095CData, function(dataItem){
        if(dataItem.safe_harbor){
          dataItem.company = companyId;
          dataItem.person = personId;
          modelObj.push(dataItem);
        }
      });
      return modelObj;
    };

    var mapToViewModel = function(model1095CData, periods){
      var sortedData = [];
      _.each(periods, function(periodValue){
        var foundItem = _.findWhere(model1095CData, {period:periodValue});
        if(foundItem){
          sortedData.push(foundItem);
        }
        else{
          sortedData.push({period: periodValue,
                           safe_harbor:''});
        }
      });
      return sortedData;
    };

    var get1095CByPersonCompany = function(companyId, personId){
        var deferred = $q.defer();
        Company1095CService.getPeriods().then(function(periods){
          Employee1095CDataRepository.ByPersonCompany
          .query({companyId: companyId, personId: personId}).$promise
          .then(function(data){
            viewModel = mapToViewModel(data, periods);
            deferred.resolve(viewModel);
          }, function(error){
              deferred.reject(error);
          });
        });
        return deferred.promise;
    };

    var validate = function(form1095CData){
      if(!form1095CData)
      {
        return 'No data is provided.';
      }

      var allYearCode = _.findWhere(form1095CData, function(item) {
        return item.period === 'All 12 Months';
      });
      var monthlyCodes = _.filter(form1095CData, function(item) {
        return item.period != 'All 12 Months';
      });
      var anyMonthlyCode = _.some(monthlyCodes, function(item) { return item.safe_harbor; });
      var hasAllMonthlyCodes = _.every(monthlyCodes, function(item) { return item.safe_harbor; });

      if (allYearCode.safe_harbor && anyMonthlyCode) {
        return 'Please enter either All 12 Months code or monthly codes.';
      }

      if (!allYearCode.safe_harbor && !hasAllMonthlyCodes) {
        return 'Values for all month are required, from Jan. to Dec.';
      }

      return PASS_VALIDATION;
    };

    var save1095CForEmployee = function(personId, companyId, form1095CData){
      var deferred = $q.defer();
      var validateResult = validate(form1095CData);
      if(validateResult != PASS_VALIDATION){
        deferred.reject(validateResult);
      }
      else{
        modelData = mapToModelObject(form1095CData, personId, companyId);
        Employee1095CDataRepository.ByPersonCompany.save({companyId: companyId, personId: personId},
          modelData,
          function(saved1095CData){
            Company1095CService.getPeriods().then(function(periods){
              viewModel = mapToViewModel(saved1095CData.saved, periods);
              deferred.resolve(viewModel);
            });
          }, function(error){
            deferred.reject(error);
          }
        );
      }
      return deferred.promise;
    };

    return{
        Get1095CByPersonCompany: get1095CByPersonCompany,
        Save1095CForEmployee: save1095CForEmployee,
        Validate: validate
    };
  }
]);
