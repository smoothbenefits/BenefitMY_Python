BenefitMyApp.directive('bmuploadmanager', 
  function() {
    return {
      restrict: 'E',
      scope: {},
      templateUrl: '/static/partials/common/upload.html',
      controller: ['$scope', 
                   '$timeout', 
                   '$attrs', 
                   'UploadService', 
          function($scope, 
                   $timeout, 
                   $attrs,
                   UploadService) {
            $scope.uploadManager = {
              hideUploadArea: false,
              canManageUpload: true,
              uploadedFiles: [],
              files:[],
              deleteS3File: function(file){
                UploadService.deleteFile(file.id, file.S3).then(function(deletedFile){
                  $scope.uploadManager.uploadedFiles = _.without($scope.uploadManager.uploadedFiles, file);
                  $scope.uploadManager.deleteSuccess = true;
                  $timeout(function(){
                    $scope.uploadManager.deleteSuccess = false;
                  }, 5000);
                });
              }};
            $scope.$watch('uploadManager.files', function(){
              UploadService.handleUploadArea($scope.uploadManager.files, $attrs.uploadType, $scope.uploadManager.uploadedFiles);
            });
            UploadService.getAllUploadsByCurrentUser().then(function(resp){
              $scope.uploadManager.uploadedFiles = resp;
            });
          }]
    };
  });
