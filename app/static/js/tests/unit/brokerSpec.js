// broker spec
describe('brokerController', function() {

  var scope,
  controller;

  beforeEach(function(){
  	module('BenefitMyApp')
  });

  describe('client controller', function(){
  	beforeEach(inject(function($rootScope, $controller){
  		scope = $rootScope.$new();
  		controller = $controller('clientsController', {$scope: scope});
  	}));

  	it('test', function(){
  		expect(scope.name).toBe('');
  	});

  });
});
