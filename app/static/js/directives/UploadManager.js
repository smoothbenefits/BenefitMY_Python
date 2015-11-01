BenefitMyApp.directive('bmuploadmanager', 
  function() {
    return {
      restrict: 'E',
      scope: {
        // Call back when an upload is successfully uploaded
        onUploadAdded: '&',
        // Call back when and upload is deleted
        onUploadDeleted: '&',
        // Template ID to handle
        templateId: '=',
        // Document ID to handle
        documentId: '='
      },
      templateUrl: '/static/partials/common/upload.html',
      controller: ['$scope',
                   '$timeout',
                   '$attrs',
                   'UploadService',
                   'TemplateService',
          function($scope,
                   $timeout,
                   $attrs,
                   UploadService,
                   TemplateService) {

            // For the use case where either an existing template ID
            // or a document ID is given, don't actually delete the 
            // relevant uploads, as those could be shared with others
            $scope.hideAndNotDelete = $scope.templateId || $scope.documentId;

            $scope.uploadManager = {
              hideUploadArea: false,
              canManageUpload: true,
              hideTypeColumn: $attrs.hideType,
              uploadMode: $attrs.uploadMode || 'area',
              viewMode: $attrs.viewMode || 'table',
              viewTitle: $attrs.viewTitle,
              uploadedFiles: [],
              files:[],
              deleteS3File: function(file){
                // If indicated so, do not really delete the files, but rather hide from
                // from the view. 
                if ($scope.hideAndNotDelete) {
                    $scope.uploadManager.uploadedFiles = _.without($scope.uploadManager.uploadedFiles, file);
                    $scope.uploadManager.deleteSuccess = true;
                    if ('onUploadDeleted' in $attrs) {
                        $scope.onUploadDeleted({uploadId: file.id});
                    }
                    $timeout(function(){
                        $scope.uploadManager.deleteSuccess = false;
                    }, 5000);
                }
                else {
                    UploadService.deleteFile(file.id, file.S3).then(function(deletedFile){
                      $scope.uploadManager.uploadedFiles = _.without($scope.uploadManager.uploadedFiles, file);
                      $scope.uploadManager.deleteSuccess = true;
                      if ('onUploadDeleted' in $attrs) {
                        $scope.onUploadDeleted({uploadId: file.id});
                      }
                      $timeout(function(){
                        $scope.uploadManager.deleteSuccess = false;
                      }, 5000);
                    });
                }
              }}; 

            var handleUploadArea = function(files, uploadType){
              if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                  var file = files[i];
                  $scope.uploadManager.inProgress = {file:file};
                  UploadService.uploadFile(file, uploadType).then(
                    function(fileUploaded){
                      $scope.uploadManager.inProgress = undefined;
                      $scope.uploadManager.uploadedFiles.unshift(fileUploaded);
                      if ('onUploadAdded' in $attrs) {
                        $scope.onUploadAdded({uploadId: fileUploaded.id});
                      }
                      if($attrs.featureId){
                        UploadService.SetUploadApplicationFeature(fileUploaded.id, uploadType, $attrs.featureId)
                        .then(function(){
                        }, function(error){
                          alert(error);
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

            $scope.hideUploadArea = function() {
                return $scope.uploadManager.hideUploadArea 
                    || ($attrs.maxUploads 
                        && $scope.uploadManager.uploadedFiles
                        && $scope.uploadManager.uploadedFiles.length >= $attrs.maxUploads);
            };

            $scope.$watch('uploadManager.files', function(){
              handleUploadArea($scope.uploadManager.files, $attrs.uploadType);
            });

            if($attrs.featureId && $attrs.uploadType) {
              $attrs.$observe('featureId', function() {
                UploadService.getUploadsByFeature($attrs.featureId, $attrs.uploadType)
                .then(function(resp){
                  $scope.uploadManager.uploadedFiles = resp;
                });
              });
            } 
            else if ('templateId' in $attrs) {
                TemplateService.getTemplateById($scope.templateId)
                  .then(function(template){
                    if (template && template.upload) {
                        $scope.uploadManager.uploadedFiles.push(template.upload);
                    }
                  });
            }
            else if ('documentId' in $attrs) {

            }
            else {
              UploadService.getAllUploadsByCurrentUser().then(function(resp){
                $scope.uploadManager.uploadedFiles = resp;
              });
            }
          }]
    };
  });
