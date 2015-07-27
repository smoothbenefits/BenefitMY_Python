// broker spec
describe('brokerController', function() {

  var scope,
  controller;

  beforeEach(function(){
    angular.mock.module('BenefitMyApp')
  });

  describe('client controller', function(){
  	beforeEach(angular.mock.inject(function($rootScope, $controller){
  		scope = $rootScope.$new();
  		controller = $controller('clientsController', {$scope: scope});
  	}));

  	it('assign value to scope', function(){
      scope.name = 'hello';
  		expect(scope.name).toBe('hello');
  	});

  });

  describe('selected benefits Controller', function(){
    beforeEach(angular.mock.inject(function($rootScope, $controller){
      scope = $rootScope.$new();
      controller = $controller('selectedBenefitsController', {$scope: scope});
    }));

    it('verify setup state', function(){
      expect(scope.employeeList.length).toBe(0);
    });

  });
});
