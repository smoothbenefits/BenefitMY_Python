BenefitMyApp.directive('bmuploadviewer', 
  function() {
    return {
      restrict: 'E',
      scope: {},
      templateUrl: '/static/partials/common/upload.html',
      controller: ['$scope', 
                   '$attrs', 
                   'UploadService', 
          function($scope, 
                   $attrs,
                   UploadService) {
            $scope.uploadManager = {
              hideUploadArea: true,
              canManageUpload: false,
              uploadedFiles: [],
              files: []
            };
            UploadService.getAllUploadsByCurrentUser().then(function(resp){
              $scope.uploadManager.uploadedFiles = resp;
            });
          }]
    };
  });