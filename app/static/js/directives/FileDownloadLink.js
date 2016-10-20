BenefitMyApp.directive('bmFileDownloadLink', 
  function() {
    var controller = [
      '$scope',
      '$http',
      'FileSaver',
      'Blob',
      function FamilyMemberManagerDirectiveController(
        $scope,
        $http,
        FileSaver,
        Blob) {

        var getFileNameFromContentDisposition = function(contentDisposition){
          var startPos = contentDisposition.indexOf('=');
          var fileName = contentDisposition.substring(startPos+1, contentDisposition.length);
          //Also trim away all quotes characters
          fileName = fileName.replace(new RegExp('"', 'g'), '');
          return fileName;
        };

        $scope.getFile = function(){
          if($scope.linkHref){
            var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
            if (isSafari){
              window.location = $scope.linkHref;
            }
            else{
              $http.get($scope.linkHref, {responseType: 'arraybuffer'})
                .then(function successCallback(response) {
                  var fileName = getFileNameFromContentDisposition(
                    response.headers('Content-Disposition'));

                  var contentType = response.headers('Content-Type');
                  
                  var data = new Blob([response.data], { type: contentType});
                  FileSaver.saveAs(data, fileName, false);
                }, function errorCallback(response) {
                  console.log("Error happened during download!");
                  console.log(response);
                });
            }
          }
        };
      }
    ];
    return {
      restrict:'E',
      scope:{
          linkHref: '=',
          linkName: '@'
      },
      templateUrl: '/static/partials/common/directive_file_download_link.html',
      controller: controller
    }
  }
);