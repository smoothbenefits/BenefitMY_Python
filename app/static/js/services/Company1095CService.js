var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('Company1095CService',
    ['$q',
     'Company1095CDataRepository',
    function ($q,
             Company1095CDataRepository){

        var _1095cPeriods = null;

        var get1095CPeriods = function(){
            var deferred = $q.defer();
            if(_1095cPeriods){
                deferred.resolve(_1095cPeriods);
            }
            else{
                Company1095CDataRepository.Periods.query()
                .$promise.then(function(periods){
                    _1095cPeriods = periods;
                    deferred.resolve(_1095cPeriods);
                })
            }
            return deferred.promise;
        };

        var get1095CByCompany = function(companyId){
            var deferred = $q.defer();
            get1095CPeriods().then(function(periods){
                Company1095CDataRepository.ByCompany.query({comp_id: companyId})
                .$promise.then(function(data){
                    var sortedData = [];
                    _.each(periods, function(periodValue){
                        var foundItem = _.findWhere(data, {period:periodValue});
                        if(foundItem){
                          sortedData.push(foundItem);
                        }
                        else{
                          sortedData.push({period: periodValue,
                                           employee_share: '',
                                           safe_harbor:'',
                                           offer_of_coverage: ''});
                        }
                      });
                    deferred.resolve(sortedData);
                }, function(error){
                    deferred.reject(error);
                });
            });
            return deferred.promise;
        };

        var validate = function(form1095CData){
            var valid = false;
            _.each(form1095CData, function(dataItem){
                if(!valid){
                    valid = dataItem.offer_of_coverage && dataItem.employee_share;
                }
            });
            return valid;
        };

        var save1095CWithCompany = function(companyId, form1095CData){
            var deferred = $q.defer();
            _.each(form1095CData, function(dataItem){
                dataItem.company = companyId;
                dataItem.offer_of_coverage = dataItem.offer_of_coverage.toUpperCase();
            });
            if(!validate(form1095CData)){
                deferred.reject('The 1095C form data are invalid! Please try again');
            }
            else{
                Company1095CDataRepository.ByCompany.save({comp_id:companyId}, form1095CData, 
                    function(saved1095CData){
                        deferred.resolve(saved1095CData.saved);
                    }, function(error){
                        deferred.reject(error);
                });
            }
            return deferred.promise;
        };

        return{
            get1095CByCompany: get1095CByCompany,
            getPeriods: get1095CPeriods,
            save1095CWithCompany: save1095CWithCompany
        };
    }
]);