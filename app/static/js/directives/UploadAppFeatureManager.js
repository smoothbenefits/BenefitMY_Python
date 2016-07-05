BenefitMyApp.directive('bmUploadAppFeatureManager', 
  function() {
    return {
      restrict: 'E',
      scope:{
        uploadMode: '@',
        hideType: '@',
        viewMode: '@',
        viewTitle: '@'
      },
      templateUrl: '/static/partials/common/directive_upload_app_feature.html',
      controller: ['$scope',
                   '$timeout',
                   '$attrs',
                   'UploadService',
          function($scope,
                   $timeout,
                   $attrs,
                   UploadService) {

            var init = function(){
              if($attrs.featureId && $attrs.uploadType){
                $attrs.$observe('featureId', function(){
                  $scope.featureId = $attrs.featureId;
                  UploadService.getUploadsByFeature($scope.featureId, $attrs.uploadType)
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
              if(featureId && $attrs.uploadType){
                UploadService.SetUploadApplicationFeature(uploadedFile.id, $attrs.uploadType, featureId)
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