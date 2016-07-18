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
  function($scope,
           $state,
           $modal,
           $controller,
           ProjectService,
           ContractorsService,
           utilityService){

    /**
        #########################
        # Fake Data Begins
        #########################
    */

    $scope.employeePayments = [];
    var employees = [
        {
            'fullName': 'Simon Cowell'
        }, 
        {
            'fullName': 'Audrea White'
        }, 
        {
            'fullName': 'Simpson Fleet'
        } 
    ];

    var getListOfWeeks = function() {

        // Configuration of the view window of weeks to include
        var preWeeks = 10;
        var postWeeks = 5;

        var weeks = [];

        // Get the start date of the current week as reference
        var today = moment();
        var startDateOfCurrentWeek = moment(today).startOf('week');

        // Construct the list of weeks and massage the data ready for
        // display
        for (var i = -preWeeks; i <= postWeeks; i++) {
            var weekStartDate = moment(startDateOfCurrentWeek).add(i, 'weeks');
            var weekEndDate = moment(weekStartDate).endOf('week');
            var weekItem = {
                weekStartDate: weekStartDate,
                weekDisplayText: weekStartDate.format(SHORT_DATE_FORMAT_STRING)
                                + ' - '
                                + weekEndDate.format(SHORT_DATE_FORMAT_STRING)
            };

            weeks.push(weekItem);
        }

        return weeks;
    };

    var weeks = getListOfWeeks();

    for (i = 0; i < employees.length; i++) {
        for (j = 0; j < weeks.length; j++) {
            var amount = Math.floor((Math.random() * 2000) + 1);;
            $scope.employeePayments.push(
                {
                    'employee': employees[i],
                    'week': weeks[j].weekDisplayText,
                    'amount': amount.toLocaleString()
                }
            );
        }
    }

    /**
        #########################
        # Fake Data Ends
        #########################
    */

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('project', function(project) {
        if(project){
          $scope.companyId = utilityService.retrieveIdFromEnvAwareId(project.companyDescriptor);

          ContractorsService.GetContractorsByCompany($scope.companyId).then(function(contractors) {
            $scope.contractors = contractors;
          });
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
