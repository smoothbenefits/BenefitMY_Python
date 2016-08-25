BenefitMyApp.controller('TimePunchCardAdminIndividualDirectiveController', [
    '$scope',
    '$modal',
    '$controller',
    'TimePunchCardService',
    'EmployeeProfileService',
    function TimePunchCardAdminIndividualDirectiveController(
      $scope,
      $modal,
      $controller,
      TimePunchCardService,
      EmployeeProfileService) {

        // Inherite scope from base
        $controller('modalMessageControllerBase', {$scope: $scope});

        var getWeekFromDate = function(){
          var theStartDate = moment($scope.dateOfWeek).startOf('week');
          var theEndDate = moment($scope.dateOfWeek).endOf('week');
          var selectedWeek = {
              weekStartDate: theStartDate,
              weekEndDate: theEndDate,
              weekDisplayText: theStartDate.format(SHORT_DATE_FORMAT_STRING)
                              + ' - '
                              + theEndDate.format(SHORT_DATE_FORMAT_STRING)
          };
          return selectedWeek;
        };

        var setDateOfWeek = function(dateToSet){
          if(!$scope.currentDate ||
             $scope.selectedDate &&
             $scope.currentDate.format(SHORT_DATE_FORMAT_STRING) !== moment($scope.selectedDate).format(SHORT_DATE_FORMAT_STRING)){
            $scope.dateOfWeek = dateToSet;
            $scope.selectedWeek = getWeekFromDate();
            $scope.selectedDate = 
              $scope.selectedWeek.weekStartDate.toDate();
            $scope.currentDate = moment($scope.selectedDate);
          }
        };

        var validateEmployee = function(employee){
          if(employee.id){
            $scope.userUpdated(
              {
                selectedUser: employee.person.user,
                weekDate: $scope.selectedWeek.weekStartDate
              }
            );
            $scope.employeeIsInvalid = false;
          }
          else{
            $scope.workPunchCard = null;
            $scope.employeeIsInvalid = true;
          }
        };

        $scope.init = function(){
          $scope.currentDate = null;
          $scope.$watchGroup(['user', 'company'], function(watchGroup) {
            if(watchGroup && watchGroup[0] && watchGroup[1]){
              // Populate the weeks for display
              if($scope.startDate){
                $scope.currentDate = moment($scope.startDate);
              }
              else{
                $scope.currentDate = moment();
              }
              setDateOfWeek($scope.currentDate);
              $scope.selectedEmployee = $scope.user;
              EmployeeProfileService.initializeCompanyEmployees($scope.company.id);
            }
          });

          $scope.$watch('selectedDate', function(){
            setDateOfWeek($scope.selectedDate);
          });

          $scope.$watch('selectedEmployee', function(employee){
            if(employee &&
               employee.person &&
               employee.person.user !== $scope.user.id){

              validateEmployee(employee);
            }
          });
        };


        $scope.matchAndSelect = function(){
          if(_.isString($scope.selectedEmployee)){
            $scope.employeeIsInvalid = false;
            if($scope.selectedEmployee === ''){
              $scope.selectedEmployee = $scope.user;
            }
            else{
              var resultEmployees = EmployeeProfileService.searchEmployees($scope.selectedEmployee);
              if(resultEmployees && resultEmployees.length === 1){
                $scope.selectedEmployee = resultEmployees[0];
              }
              else{
                $scope.employeeIsInvalid = true;
              }
            }
          }
        };

        $scope.prepareEmployeeSearch = function(){
          $scope.selectedEmployee = '';
        };

        $scope.getEmployees = EmployeeProfileService.searchEmployees;

        $scope.init();
    }
  ]
).directive('bmTimePunchCardAdminIndividual', function() {
  return {
    restrict: 'E',
    scope: {
        user: '=',
        company: '=',
        startDate: '=',
        userUpdated: '&'
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_admin_individual.html',
    controller: 'TimePunchCardAdminIndividualDirectiveController'
  };
});
