var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
   'CompensationService',
   ['$q', 'CompensationRepository',
   function($q, CompensationRepository){

      var mapToViewModel = function(dataModel) {
         var viewModel = {
            company: dataModel.company,
            person: dataModel.person,
            salary: dataModel.annual_base_salary,
            increasePercentage: dataModel.increase_percentage,
            effectiveDate: dataModel.effective_date,
            created: dataModel.created_at
         };

         return viewModel;
      };

      var mapToDomainModel = function(viewModel) {
        var domainModel = {
          company: viewModel.company,
          person: viewModel.person,
          annual_base_salary: viewModel.salary,
          increase_percentage: viewModel.increasePercentage,
          effective_date: viewModel.effectiveDate
        };

        return domainModel;
      };

      var addCompensationByPerson = function(compensation, personId, companyId) {
        var deferred = $q.defer();

        compensation.person = personId;
        compensation.company = companyId;
        var toSave = mapToDomainModel(compensation);
        CompensationRepository.ByCompensationId.save({id: personId}, toSave)
        .$promise.then(function(response){
          return personId;
        }).then(function(personId) {
          getCompensationByPerson(personId).then(function(response) {
            deferred.resolve(response);
          });
        }).catch(function(error) {
          deferred.reject(error);
        });

        return deferred.promise;
      };

      var getCompensationByPerson = function(personId) {
        var deferred = $q.defer();

        CompensationRepository.ByPersonId.query({personId: personId}).$promise
        .then(function(response) {
          var compensations = [];
          _.each(response, function(compensation) {
            var viewModel = mapToViewModel(compensation);
            compensations.push(viewModel);
          });

          deferred.resolve(compensations);
        }, function(error) {
          deferred.reject(error);
        });

        return deferred.promise;
      };

      return{
         getCompensationByPerson: getCompensationByPerson,
         addCompensationByPerson: addCompensationByPerson
      };
   }
]);
