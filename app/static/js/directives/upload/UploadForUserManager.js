BenefitMyApp.directive('bmUploadForUserManager', 
  function() {
    return {
      restrict: 'E',
      scope:{
        uploadMode: '@',
        hideType: '@',
        viewMode: '@',
        viewTitle: '@'
      },
      templateUrl: '/static/partials/upload/directive_upload_for_user.html',
      controller: ['$scope',
                   '$timeout',
                   '$attrs',
                   'UploadService',
          function($scope,
                   $timeout,
                   $attrs,
                   UploadService) {

            var init = function(){
              if($attrs.forUserId){
                $attrs.$observe('forUserId', function(){
                  $scope.forUserId = $attrs.forUserId;
                  UploadService.getUploadsForUser($attrs.forUserId)
                  .then(function(resp){
                    $scope.uploadedFiles = resp;
                  });
                });
              }
              else{
                UploadService.getAllUploadsByCurrentUser().then(function(resp){
                  $scope.uploadedFiles = resp;
                });
              }
            };

            $scope.fileUploaded = function(uploadedFile, featureId){
              if($attrs.forUserId){
                UploadService.setUploadForUser(uploadedFile.id, $scope.forUserId)
                  .then(function(){
                    $scope.uploadedFiles.unshift(uploadedFile);
                  }, function(error){
                    alert(error);
                  });
              }
              else{
                $scope.uploadedFiles.unshift(uploadedFile);
              }
            };

            $scope.fileDeleted = function(deletedFile, featureId){
              $scope.uploadedFiles = _.without($scope.uploadedFiles, deletedFile);
            };

            init();
          }
      ]
    };
  }
);