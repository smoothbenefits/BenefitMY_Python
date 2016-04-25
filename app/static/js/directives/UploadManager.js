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
              hideTypeColumn: $attrs.hideType,
              uploadMode: $attrs.uploadMode || 'area',
              viewMode: $attrs.viewMode || 'table',
              viewTitle: $attrs.viewTitle,
              uploadedFiles: $scope.uploadedFiles || [],
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
                      uploadType: $attrs.uploadType,
                      featureId: $attrs.featureId
                    });
                  }
                });
              }};

            var handleUploadArea = function(files){
              if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                  var file = files[i];
                  $scope.uploadManager.inProgress = {file:file};
                  UploadService.uploadFile(file).then(
                    function(fileUploaded){
                      $scope.uploadManager.inProgress = undefined;
                      if(_.isUndefined($scope.uploadedFiles)){
                        $scope.uploadManager.uploadedFiles.unshift(fileUploaded);
                      }
                      if($attrs.featureId){
                        if($scope.fileUploaded){
                          $scope.fileUploaded({
                              uploadedFile: fileUploaded,
                              uploadType: $attrs.uploadType,
                              featureId: $attrs.featureId
                            });
                        }
                        else{
                          UploadService.SetUploadApplicationFeature(fileUploaded.id, $attrs.uploadType, $attrs.featureId)
                          .then(function(){
    
                          }, function(error){
                            alert(error);
                          });
                        }
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

            var loadUploadedFilesByUploadType = function(){
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
            };

            if (_.isUndefined($scope.uploadedFiles)){
              loadUploadedFilesByUploadType();
            }
            
          }]
    };
  });
