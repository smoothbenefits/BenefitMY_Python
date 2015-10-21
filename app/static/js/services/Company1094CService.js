var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('Company1094CService',
    ['$q',
     'Company1095CService',
     'Company1094CDataRepository',
    function ($q,
              Company1095CService,
              Company1094CDataRepository){

      var _periods = null;
      var _1094cEligibilityCertification = null;

      var mapToModelObject = function(view1094CData, companyId){
        var modelMonthlyObj = [];
        _.each(view1094CData.monthly_info, function(dataItem){
          if(dataItem.minimum_essential_coverage || dataItem.fulltime_employee_count
             || dataItem.total_employee_count || dataItem.aggregated_group
             || dataItem.section_4980h_transition_relief
           ) {
            dataItem.company = companyId;
            modelMonthlyObj.push(dataItem);
          }
        });

        var memberInfo = angular.copy(view1094CData.member);
        memberInfo.company = companyId;

        return {member: memberInfo, monthly_info: modelMonthlyObj};
      };

      var mapToViewModel = function(model1094CData, periods){
        var sortedData = [];
        var monthlyData = model1094CData.monthly_info;
        _.each(periods, function(periodValue){
          var foundItem = _.findWhere(monthlyData, {period:periodValue});
          if(foundItem){
            sortedData.push(foundItem);
          }
          else{
            sortedData.push({period: periodValue,
                             aggregated_group: false,
                             minimum_essential_coverage: false,
                             section_4980h_transition_relief: false,
                             fulltime_employee_count: undefined,
                             total_employee_count: undefined
                           });
          }
        });

        var mappedValue = {
          member: model1094CData.member,
          monthly_info: sortedData
        };

        return mappedValue;
      };

      var getPeriods = function(){
        var deferred = $q.defer();
        if(_periods){
          deferred.resolve(_periods);
        }
        else{
          Company1095CService.getPeriods().then(function(periods){
            _periods = periods;
            deferred.resolve(_periods);
          });
        }
        return deferred.promise;
      };

      var get1094CEligibilityCertification = function(){
        var deferred = $q.defer();
        if(_1094cEligibilityCertification){
          deferred.resolve(_1094cEligibilityCertification);
        }
        else{
          Company1094CDataRepository.EligibilityCertification.query()
          .$promise.then(function(certifications){
            _1094cEligibilityCertification = certifications;
            deferred.resolve(_1094cEligibilityCertification);
          });
        }
        return deferred.promise;
      };

      var get1094CByCompany = function(companyId){
        var deferred = $q.defer();
        getPeriods().then(function(periods){
          Company1094CDataRepository.ByCompany.get({comp_id: companyId})
          .$promise.then(function(data){
            viewModel = mapToViewModel(data, periods);
            deferred.resolve(viewModel);
          }, function(error){
            deferred.reject(error);
          });
        });
        return deferred.promise;
      };

      var validate = function(form1094CData){
        if(!form1094CData)
        {
          return false;
        }
        _.each(form1094CData.monthly_info, function(dataItem){
          if(dataItem.fulltime_employee_count > dataItem.total_employee_count) {
            return false;
          }
        });
        return true;
      };

      var save1094CWithCompany = function(companyId, form1094CData){
        var deferred = $q.defer();
        if(!validate(form1094CData)){
          deferred.reject('The 1094C form data are invalid! Please try again');
        }
        else{
          modelData = mapToModelObject(form1094CData, companyId);
          Company1094CDataRepository.ByCompany.save({comp_id:companyId}, modelData,
            function(form1094CData){
              getPeriods().then(function(periods){
                viewModel = mapToViewModel(form1094CData, periods);
                deferred.resolve(viewModel);
              });
            }, function(error){
              deferred.reject(error);
            }
          );
        }
        return deferred.promise;
      };

      var getCompany1094CUrl = function(companyId) {
        return '/api/v1/company/' + companyId + '/forms/1094c';
      };

      return{
        GetPeriods: getPeriods,
        Get1094CByCompany: get1094CByCompany,
        Get1094CEligibilityCertification: get1094CEligibilityCertification,
        Save1094CWithCompany: save1094CWithCompany,
        Validate: validate,
        GetCompany1094CUrl: getCompany1094CUrl
      };
    }
]);
