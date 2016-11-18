var benefitmyService = angular.module('benefitmyService');
benefitmyService.factory('OpenEnrollmentDefinitionService',
  ['$http',
   '$q',
   'OpenEnrollmentDefinitionRepository',
   'DateTimeService',
   function($http, $q, OpenEnrollmentDefinitionRepository, DateTimeService){
      
      var mapToViewModel = function(dataModel){
        var viewModel = angular.copy(dataModel);
        var monthsInYear = DateTimeService.GetMonthsInYear();
        viewModel.start_month = _.findWhere(monthsInYear, {id: dataModel.start_month});
        viewModel.end_month = _.findWhere(monthsInYear, {id: dataModel.end_month});
        return viewModel;
      };

      var mapToDataModel = function(viewModel){
        var dataModel = {};
        dataModel.company = viewModel.company;
        dataModel.start_month = viewModel.start_month.id;
        dataModel.start_day = viewModel.start_day;
        dataModel.end_month = viewModel.end_month.id;
        dataModel.end_day = viewModel.end_day;
        return dataModel;
      };

      var Get = function(companyId){
        return OpenEnrollmentDefinitionRepository.ByCompany.get({comp_id:companyId})
        .$promise.then(function(openEnrollmentDef){
          return mapToViewModel(openEnrollmentDef);
        });
      };

      var testInOpenEnrollment = function(openEnrollmentDefinition){
        if(!openEnrollmentDefinition){
          return false;
        }
        var testDateStart = moment().month(openEnrollmentDefinition.start_month.id).date(openEnrollmentDefinition.start_day);
        var testDateEnd = moment().month(openEnrollmentDefinition.end_month.id).date(openEnrollmentDefinition.end_day);
        if (testDateEnd.isBefore(testDateStart)){
          // If the end is before the start on this period,
          // let's assume it's cross calendar year
          testDateEnd = testDateEnd.add(1, 'y');
        }
        return moment().isBefore(testDateEnd) && moment().isAfter(testDateStart);
      };

      var InOpenEnrollmentPeriod = function(companyId){
        return Get(companyId).then(function(openEnrollmentDef){
          return testInOpenEnrollment(openEnrollmentDef);
        });
      };

      var Save = function(openEnrollmentDef){
        var dataModel = mapToDataModel(openEnrollmentDef);
        if(openEnrollmentDef.id){
          return OpenEnrollmentDefinitionRepository.ByCompany.update(
            {comp_id:dataModel.company},
            dataModel
          ).$promise.then(function(openEnrollmentDef){
            return mapToViewModel(openEnrollmentDef);
          });
        }
        else{
          return OpenEnrollmentDefinitionRepository.ByCompany.save(
            {comp_id:dataModel.company},
            dataModel
          ).$promise.then(function(openEnrollmentDef){
            return mapToViewModel(openEnrollmentDef);
          });
        }
      };

      var Delete = function(companyId){
        return OpenEnrollmentDefinitionRepository.ByCompany.delete(
          {comp_id: companyId}
        ).$promise.then(function(){
          return null;
        });
      };

      return{
        Get: Get,
        Save: Save,
        Delete: Delete,
        InOpenEnrollmentPeriod: InOpenEnrollmentPeriod
      };
   }
]);
