var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('WorkersCompService',
  ['$q',
   function WorkersCompService(
    $q) {
        var GetAllPhraseologys = function() {
            var allDepartments = [
                {
                    id: 'BMHT_1_b457df460695969e8960e3f1623a3ee7',
                    phraseology: 'FARM: NURSERY EMP & DRIVERS',
                    ma_code: '1001'
                },
                {
                    id: 'BMHT_2_7993906d4aa8fa48e7bb98f83d83b83c',
                    phraseology: 'COTTON BATTING,WADDING OR WASTE MFG',
                    ma_code: '2001'
                },
                {
                    id: 'BMHT_3_babf7c42f76af6f81486d76ff6e33505',
                    phraseology: 'GLOVE MFG-LEATHER OR TEXTILE',
                    ma_code: '3015'
                },
                {
                    id: 'BMHT_4_8e37f27ce2220e875bfb0b9815df0b0d',
                    phraseology: 'FEATHER PILLOW MFG',
                    ma_code: '5024'
                }
            ];

            var deferred = $q.defer();
            deferred.resolve(allDepartments);
            return deferred.promise;
        };

        var GetCompanyDepartments = function(companyId) {
            var allCompanyDepartments = [
                {
                    id: 'BMHT_1_b457df460695969e8960e3f1623a3ee7',
                    phraseology: {
                        id: 'BMHT_2_7993906d4aa8fa48e7bb98f83d83b83c',
                        phraseology: 'COTTON BATTING,WADDING OR WASTE MFG',
                        ma_code: '2001'
                    },
                    company: 'BMHT_1_b457df460695969e8960e3f1623a3ee7',
                    description: 'Cotton Batting'
                },
                {
                    id: 'BMHT_2_7993906d4aa8fa48e7bb98f83d83b83c',
                    phraseology: {
                        id: 'BMHT_3_babf7c42f76af6f81486d76ff6e33505',
                        phraseology: 'GLOVE MFG-LEATHER OR TEXTILE',
                        ma_code: '3015'
                    },
                    company: 'BMHT_1_b457df460695969e8960e3f1623a3ee7',
                    description: 'Glove Production'
                }
            ];

            var deferred = $q.defer();
            deferred.resolve(allCompanyDepartments);
            return deferred.promise;
        };

        return {
            GetAllPhraseologys: GetAllPhraseologys,
            GetCompanyDepartments: GetCompanyDepartments
        };
    }
]);
