var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('PTOService',
  ['$q',
   'PTORepository',
   function PTOService(
     $q,
     PTORepository){
         var GetPTOsByRequestor = function(){
        
         };

         return {
             GetPTOsByRequestor: GetPTOsByRequestor
         };
     }
]);