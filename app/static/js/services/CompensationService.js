var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
   'CompensationService',
   ['$q', 'CompensationRepository',
   function($q, CompensationRepository){

      var mapToViewModel = function(dataModel) {
         var viewModel = {
            company: dataModel.company,
            person: dataModel.person,
            salary: Number(dataModel.annual_base_salary).toFixed(2),
            increasePercentage: Number(dataModel.increase_percentage).toFixed(2),
            effectiveDate: moment(dataModel.effective_date).format(DATE_FORMAT_STRING),
            created: moment(dataModel.created_at).format(DATE_FORMAT_STRING)
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
          deferred.resolve(response);
        }).catch(function(error) {
          deferred.reject(error);
        });

        return deferred.promise;
      };

      var getCompensationByPerson = function(personId) {
        var deferred = $q.defer();

        CompensationRepository.ByPersonId.query({personId: personId}).$promise
        .then(function(response) {
          var benchMarkDate = new Date(0);
          var compensations = [];
          _.each(response, function(compensation) {
            var viewModel = mapToViewModel(compensation);
            var effectiveDate = moment(viewModel.effectiveDate);
            if (effectiveDate > benchMarkDate && effectiveDate < new Date()) {
              benchMarkDate = effectiveDate;
            }
            compensations.push(viewModel);
          });

          var current = _.findWhere(compensations, function(compensation) {
            return moment(compensation.effectiveDate) === benchMarkDate;
          });

          if (current) {
            current.isCurrent = true;
          }

          deferred.resolve(compensations);
        }, function(error) {
          deferred.reject(error);
        });

        return deferred.promise;
      };

      return{
         getCompensationByPerson: getCompensationByPerson,
         addCompensationByPerson: addCompensationByPerson,
         mapToViewModel: mapToViewModel
      };
   }
]);
