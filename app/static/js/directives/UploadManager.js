BenefitMyApp.directive('bmuploadmanager', 
  function() {
    return {
      restrict: 'E',
      scope: {
        uploadedFiles: '=',
        fileUploaded: '&',
        fileDeleted: '&'
      },
      templateUrl: '/static/partials/common/directive_upload_manager.html',
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
              uploadMode: 'area',
              viewMode: 'table',
              files:[],
              deleteS3File: function(file){
                UploadService.deleteFile(file.id, file.S3).then(function(deletedFile){
                  $scope.uploadManager.uploadedFiles = _.without($scope.uploadManager.uploadedFiles, file);
                  $scope.uploadManager.deleteSuccess = true;
                  $timeout(function(){
                    $scope.uploadManager.deleteSuccess = false;
                  }, 5000);
                  if($scope.fileDeleted){
                    $scope.fileDeleted({
                      deletedFile: file,
                      featureId: $attrs.featureId
                    });
                  }
                });
              }
            };

            var handleUploadArea = function(files){
              if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                  var file = files[i];
                  $scope.uploadManager.inProgress = {file:file};
                  UploadService.uploadFile(file).then(
                    function(fileUploaded){
                      $scope.uploadManager.inProgress = undefined;
                      if($scope.fileUploaded){
                        $scope.fileUploaded({
                            uploadedFile: fileUploaded,
                            featureId: $attrs.featureId
                          });
                      }
                    },
                    function(error){
                      alert('upload error happened!');
                      $scope.uploadManager.inProgress = undefined;
                    },
                    function(evt){
                      $scope.uploadManager.inProgress.progress = (evt.loaded/evt.total)*100;
                    });
                }
              }
            };
            $scope.$watch('uploadManager.files', function(){
              handleUploadArea($scope.uploadManager.files);
            });
            $scope.$watch('uploadedFiles', function(){
              $scope.uploadManager.uploadedFiles = $scope.uploadedFiles;
            });
            $attrs.$observe('viewTitle', function(){
              $scope.uploadManager.viewTitle = $attrs.viewTitle;
            });
            $attrs.$observe('viewMode', function(){
              if($attrs.viewMode){
                $scope.uploadManager.viewMode = $attrs.viewMode;
              }
            });
            $attrs.$observe('uploadMode', function(){
              if($attrs.uploadMode){
                $scope.uploadManager.uploadMode = $attrs.uploadMode;
              }
            });
            $attrs.$observe('hideType', function(){
              $scope.uploadManager.hideTypeColumn = $attrs.hideType;
            });
        }]
    };
  });
