BenefitMyApp.controller('TimePunchCardEditModalController', [
  '$scope',
  '$modalInstance',
  'TimePunchCardService',
  'UsStateService',
  'punchCard',
  function(
    $scope,
    $modalInstance,
    TimePunchCardService,
    UsStateService,
    punchCard){
    $scope.headerText = punchCard ? 'Edit Punch Card' : 'Create Punch Card';

    $scope.punchCard = punchCard;

    $scope.cardTypes = TimePunchCardService.GetAvailablePunchCardTypes();
    $scope.allStates = UsStateService.GetAllStates();

    $scope.allProjects = [
        '205 Aloha Avenue',
        'The Universal Tower',
        'Harland Street Rework'
    ];

    $scope.selectedState = null;
    $scope.selectedProject = null;

    $scope.save = function(){
        $modalInstance.close();
    }
    $scope.cancel = function() {
        $modalInstance.dismiss();
    };
  }
]).controller('TimePunchCardWeeklyViewController', [
    '$scope',
    '$attrs',
    '$modal',
    '$controller',
    'TimePunchCardService',
    function TimePunchCardWeekDirectiveController(
      $scope,
      $attrs,
      $modal,
      $controller,
      TimePunchCardService) {

        $scope.weekdayNums = [0, 1, 2, 3, 4, 5, 6];

        $scope.init = function(){
          $scope.$watch('week', function(weekSelected){
            if(weekSelected){
              var startDate = weekSelected.weekStartDate;
              $scope.datesOfWeek = [];
              for (var i=0; i<7; i++){
                var weekDate = moment(startDate).add(i, 'days');
                $scope.datesOfWeek[i] = {
                    'weekdayName': weekDate.format('ddd'),
                    'displayDate': weekDate.format(SHORT_DATE_FORMAT_STRING_NO_YEAR),
                    'date': weekDate
                };
              }

              $scope.weeklyPunchCards = TimePunchCardService.GetWeeklyPunchCardsByEmployeeUser(null, null, null); 
            }
          });
        };

        $scope.init();

        $scope.getDisplayTime = function(dateTime) {
            var time = moment(dateTime);
            return time.format('hh:mm');
        };

        var showEditModal = function(punchCard) {
            $modal.open({
                templateUrl: '/static/partials/time_punch_card_new/modal_edit_time_punch_card.html',
                controller: 'TimePunchCardEditModalController',
                size: 'md',
                backdrop: 'static',
                resolve: {
                  'punchCard': function() {
                    return punchCard;
                  }
                }
            });
        };

        $scope.createPunchCard = function(date) {
            var punchCard = TimePunchCardService.GetBlankPunchCardForEmployeeUser(
                    $scope.user,
                    $scope.company,
                    date);
            showEditModal(punchCard);
        };

        $scope.editPunchCard = function(punchCard) {
            showEditModal(angular.copy(punchCard));
        };

        $scope.deletePunchCard = function(punchCard) {
            TimePunchCardService.DeletePunchCard(punchCard);
            $scope.weeklyPunchCards = TimePunchCardService.GetWeeklyPunchCardsByEmployeeUser(null, null, null);
        };
    }
  ]
).directive('bmTimePunchCardWeeklyView', function() {
  return {
    restrict: 'E',
    scope: {
        week: '=',
        user: '=',
        company: '='
    },
    templateUrl: '/static/partials/time_punch_card_new/directive_time_punch_card_weekly_view.html',
    controller: 'TimePunchCardWeeklyViewController'
  };
});
