var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
   'CompensationService',
   ['$q', 'CompensationRepository',
   function($q, CompensationRepository){

      var mapToViewModel = function(dataModel) {
         var viewModel = {
            company: dataModel.company,
            person: dataModel.person,
            effectiveDate: dataModel.effective_date,
            created: dataModel.created_at
         };

         if (dataModel.annual_base_salary) {
           viewModel.salary = Number(dataModel.annual_base_salary).toFixed(2);
         }
         if (dataModel. increasePercentage) {
           viewModel.increasePercentage = Number(dataModel.increase_percentage).toFixed(2);
         }
         if (dataModel.hourly_rate) {
           viewModel.hourlyRate = Number(dataModel.hourly_rate).toFixed(2);
         }
         if (dataModel.projected_hour_per_month) {
           viewModel.projectedHourPerMonth = Number(dataModel.projected_hour_per_month).toFixed(2);
         }

         return viewModel;
      };

      var mapToDomainModel = function(viewModel) {
        var domainModel = {
          company: viewModel.company,
          person: viewModel.person,
          effective_date: viewModel.effective_date
        };

        if (viewModel.salary) {
          domainModel.annual_base_salary = Number(viewModel.salary).toFixed(2);
        }
        if (viewModel.increasePercentage) {
          domainModel.increase_percentage = Number(viewModel.increasePercentage).toFixed(2);
        }
        if (viewModel.hourly_rate) {
          domainModel.hourly_rate = Number(viewModel.hourly_rate).toFixed(4);
        }
        if (viewModel.projected_hour_per_month) {
          domainModel.projected_hour_per_month = Number(viewModel.projected_hour_per_month).toFixed(4);
        }

        return domainModel;
      };

      var formatDateTimeForView = function(compensations) {
        var mapped = angular.copy(compensations);
        _.each(mapped, function(compensation) {
          compensation.effectiveDate = moment(compensation.effectiveDate).format(DATE_FORMAT_STRING);
          compensation.create = moment(compensation.created).format(DATE_FORMAT_STRING);
        });

        return mapped;
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

      var getCurrentCompensationByPerson = function(personId){
        var compensations = getCompensationByPersonSortedByDate(personId, true);

        // Compensations for a person is pre-sorted descendingly by effective date
        // Just need to find out the first one that takes effects before today
        for (var i = 0; i < compensations.length; i++) {
          if (compensations[i].effectiveDate < new Date()) {
            return compensation[i];
          }
        }

        return null;
      };

      var getCurrentCompensationFromViewList = function(compensations) {
        if (compensations) {
          var current = _.findWhere(compensations, function(compensation) {
            return compensation.isCurrent;
          });

          return current;
        }
        return null;
      };

      var updateCompensationStatus = function(sortedRawCompensations) {
        var reversed = false;
        var benchMark = new Date();
        var updated = angular.copy(sortedRawCompensations);
        _.each(updated, function(compensation) {
          compensation.effectiveDate = new Date(compensation.effectiveDate);
        })

        // Make sure compensations is sorted descendingly by effective date
        if (updated.length > 1 &&
        (updated[1].effectiveDate > updated[0].effectiveDate)) {
          updated.reverse();
          reversed = true;
        }

        // Mark the closest past effective date as current record and update bench mark
        for (var i = 0; i < updated.length; i++) {
          if (updated[i].effectiveDate < benchMark) {
            benchMark = updated[i].effectiveDate;
            updated[i].isCurrent = true;
            break;
          }
        }

        // Provide detail status to all compensation records
        _.each(updated, function(compensation) {
          if (compensation.effectiveDate > benchMark) {
            compensation.status = 'PENDING';
          } else if (compensation.effectiveDate < benchMark) {
            compensation.status = 'EXPIRED';
          } else {
            compensation.status = 'CURRENT';
          }
        });

        // Restore original sorting
        if (reversed) {
          updated.reverse();
        }

        return updated;
      };

      var getCompensationByPersonSortedByDate = function(personId, descending) {
        var deferred = $q.defer();

        CompensationRepository.ByPersonId.query({personId: personId}).$promise
        .then(function(response) {
          var compensations = [];
          _.each(response, function(compensation) {
            var viewModel = mapToViewModel(compensation);
            compensations.push(viewModel);
          });

          _.sortBy(compensations, function(compensation) {
            return compensation.effectiveDate;
          });

          compensations = updateCompensationStatus(compensations);
          compensations = formatDateTimeForView(compensations);

          if (descending) {
            compensations = compensations.reverse();
          }

          deferred.resolve(compensations);
        }, function(error) {
          deferred.reject(error);
        });

        return deferred.promise;
      };

      return{
         getCompensationByPersonSortedByDate: getCompensationByPersonSortedByDate,
         addCompensationByPerson: addCompensationByPerson,
         mapToViewModel: mapToViewModel,
         getCurrentCompensationByPerson: getCurrentCompensationByPerson,
         getCurrentCompensationFromViewList: getCurrentCompensationFromViewList
      };
   }
]);
