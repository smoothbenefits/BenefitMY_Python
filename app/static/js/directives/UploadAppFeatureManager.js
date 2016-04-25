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
              $scope.uploadMode = $attrs.uploadMode;
              if($attrs.featureId && $attrs.uploadType){
                $attrs.$observe('featureId', function(){
                  UploadService.getUploadsByFeature($attrs.featureId, $attrs.uploadType)
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

            $scope.fileUploaded = function(uploadedFile, uploadType, featureId){
              if($attrs.featureId && $attrs.uploadType){
                UploadService.SetUploadApplicationFeature(uploadedFile.id, uploadType, featureId)
                  .then(function(){

                  }, function(error){
                    alert(error);
                  });
              }
            };

            init();
          }
      ]
    };
  }
);