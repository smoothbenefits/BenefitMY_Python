var benefitmyDomainModelFactories = angular.module('benefitmyDomainModelFactories', ['ngResource']);

// FSA domain repo
benefitmyDomainModelFactories.factory('FsaRepository', ['$resource',
  function ($resource){
    return {
      ByUser: $resource('/api/v1/fsa/:userId', {userId:'@user_id'}),
      ById: $resource('/api/v1/fsa/:id', {userId:'@id'}, { 
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);