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
              viewMode: $attrs.viewMode || 'table',
              viewTitle: $attrs.viewTitle,
              uploadedFiles: [],
              files: []
            };
            
            if($attrs.featureId && $attrs.uploadType){
              $attrs.$observe('featureId', function(){
                UploadService.getUploadsByFeature($attrs.featureId, $attrs.uploadType)
                .then(function(resp){
                  $scope.uploadManager.uploadedFiles = resp;
                });  
              });  
            }
            else{
              UploadService.getAllUploadsByCurrentUser().then(function(resp){
                $scope.uploadManager.uploadedFiles = resp;
              });
            }
          }]
    };
  });