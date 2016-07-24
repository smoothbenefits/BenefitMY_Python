BenefitMyApp.controller('ProjectPayableModalController', [
  '$scope',
  '$modalInstance',
  'ProjectService',
  'ContractorsService',
  'payable',
  'project',
  'contractors',
  function(
    $scope,
    $modalInstance,
    ProjectService,
    ContractorsService,
    payable,
    project,
    contractors) {

    $scope.editMode = payable;
    $scope.contractors = contractors;
    $scope.modalHeader = $scope.editMode ? 'Edit Payable Info' : 'Create a New Payable';
    $scope.payable = $scope.editMode
                        ? payable
                        : ProjectService.GetBlankProjectPayable(project._id);

    if ($scope.editMode) {
      $scope.payable.contractor = _.find(contractors, function(contractor) {
        return contractor._id === $scope.payable.contractor._id;
      });
    }

    $scope.$watch('payable', function(payable) {
      if (payable) {
        $scope.expiredInsurances = ProjectService.GetAllExpiredCertificatesOfRequiredInsurance(
          payable.contractor,
          payable.dateStart,
          payable.dateEnd,
          project
        );
      }
    }, true); // Equality watch (use angular.equals to determine changes)

    $scope.enableSave = function(payable) {
      if (moment(payable.dateStart).isAfter(moment(payable.dateEnd))) {
        return false;
      }

      if (!payable.amount || payable.amount <= 0) {
        return false;
      }

      return payable.contractor;
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };

    $scope.save = function() {
      ProjectService.SaveProjectPayable(project._id, $scope.payable)
        .then(function(savedPayable){
          $modalInstance.close(true);
        }, function(error){
          $modalInstance.close(false)
        });
    }
  }
]).controller('ProjectPayableManagerDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'ProjectService',
  'ContractorsService',
  'utilityService',
  'TimePunchCardService',
  function($scope,
           $state,
           $modal,
           $controller,
           ProjectService,
           ContractorsService,
           utilityService,
           TimePunchCardService){


    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    var PopulateEmployeePayables = function(companyId, project){
      TimePunchCardService.GetAllPunchCardsByCompany(companyId)
      .then(function(punchCardsByEmployee){
        $scope.employeePayments = [];
        for(employeeId in punchCardsByEmployee){
          var filteredPunchCardsByWeek = {};
          var employeePunchCards = punchCardsByEmployee[employeeId];
          _.each(employeePunchCards, function(punchCard){
            //Filter cards that maps to the current project.
            if(punchCard.attributes.project &&
               punchCard.attributes.project.id === project._id){
              //Calculate the week start date for the card.
              var weekStart = moment(punchCard.date).startOf('week').format(SHORT_DATE_FORMAT_STRING);
              if(!filteredPunchCardsByWeek[weekStart]){
                filteredPunchCardsByWeek[weekStart] = [];
              }
              //Construct the punch cards by week dictionary
              filteredPunchCardsByWeek[weekStart].push(punchCard);
            }
          });
          //Start calculate the employeePayments object
          for (weekStart in filteredPunchCardsByWeek){
            var punchCards = filteredPunchCardsByWeek[weekStart];
            var filteredForHoursCalculation = TimePunchCardService.FilteredCardsForTotalHours(punchCards);
            if (!filteredForHoursCalculation || filteredForHoursCalculation.length <= 0){
              continue;
            }
            var employeeFullName = filteredForHoursCalculation[0].employee.firstName + ' ' + filteredForHoursCalculation[0].employee.lastName;
            var amount = 0;
            _.each(filteredForHoursCalculation, function(employeeCard){
                 var duration = employeeCard.getDuration();
                 amount += duration * employeeCard.attributes.hourlyRate.value || 0;
            });
            var weekStartDate = Date.parse(weekStart);
            $scope.employeePayments.push({
              'employee': employeeFullName,
              'week': moment(weekStartDate).format(SHORT_DATE_FORMAT_STRING) + ' - ' + moment(weekStartDate).add(7, 'd').format(SHORT_DATE_FORMAT_STRING),
              'amount': amount.toFixed(2)
            });
          }
        }
      });
    };

    $scope.$watch('project', function(project) {
        if(project){
          $scope.companyId = utilityService.retrieveIdFromEnvAwareId(project.companyDescriptor);

          ContractorsService.GetContractorsByCompany($scope.companyId).then(function(contractors) {
            $scope.contractors = contractors;
          });

          PopulateEmployeePayables($scope.companyId, project);          
        }
    });

    $scope.openPayableModal = function(payable) {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/contractor/modal_project_payable.html',
        controller: 'ProjectPayableModalController',
        backdrop: 'static',
        size: 'lg',
        resolve: {
          payable: function() {
            return angular.copy(payable);
          },
          project: function() {
            return $scope.project;
          },
          contractors: function() {
            return angular.copy($scope.contractors);
          }
        }
      });

      modalInstance.result.then(function(success){
        if(success){
          var successMessage = "Project Payable saved successfully!";
          $scope.showMessageWithOkayOnly('Success', successMessage);
        }
        else{
          var message = "Project Payable save failed!";
          $scope.showMessageWithOkayOnly('Error', message);
        }
        $state.reload();
      });
    };

    $scope.hasPayablesMade = function() {
        return $scope.project
            && $scope.project.payables
            && $scope.project.payables.length > 0;
    };

    $scope.delete = function(payable) {
      ProjectService.DeletePayableByProjectPayable($scope.project._id, payable)
      .then(function(res){
        $state.reload();
      });
    };

    $scope.fileUploaded = function(uploadedFile, featureId){
      var payable = _.find($scope.project.payables, function(projectPayable){
        return projectPayable._id == featureId;
      });
      if(payable){
        createdWaiver = {
          id: uploadedFile.id,
          S3: uploadedFile.S3,
          file_name: uploadedFile.file_name,
          file_type: uploadedFile.file_type,
          uploaded_at: uploadedFile.uploaded_at
        };
        payable.lienWaivers.unshift(createdWaiver);
        ProjectService.SaveProjectPayable($scope.project._id, payable);
      }
    };

    $scope.fileDeleted = function(deletedFile, featureId){
      var payable = _.find($scope.project.payables, function(projectPayable){
        return projectPayable._id == featureId;
      });
      if(payable){
        payable.lienWaivers = _.without(payable.lienWaivers, deletedFile);
        ProjectService.SaveProjectPayable($scope.project._id, payable);
      }
    };
      
    $scope.downloadLienWaiver = function(payable) {
        var contractorId = payable.contractor._id;
        var url = ContractorsService.GetLienWaiverDownloadUrl($scope.companyId, contractorId);
        location.href = url;
    };
  }
]).directive('bmProjectPayableManager', function(){

    return {
        restrict: 'E',
        scope: {
            project: '='
        },
        templateUrl: '/static/partials/contractor/directive_project_payable_manager.html',
        controller: 'ProjectPayableManagerDirectiveController'
      };
});
