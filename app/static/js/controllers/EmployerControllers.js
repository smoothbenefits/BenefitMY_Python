var employersController = angular.module('benefitmyApp.employers.controllers',[]);

var getDocumentType = function(documentTypeId){

    if (documentTypeId === 1){
      return "Offer Letter";
    }
    else if (documentTypeId === 2){
      return "Employment Agreement";
    }
    else if(documentTypeId === 3)
    {
      return "NDA";
    }
    return "";
};

var employerHome = employersController.controller('employerHome',
                                                  ['$scope',
                                                  '$location',
                                                  'employerRepository',
                                                  'currentUser',
                                                  'clientListRepository',
                                                  'documentRepository',
                                                  'templateRepository',
                                                  'employerWorkerRepository',
                                                  'benefitListRepository',
  function employerHome($scope,
                        $location,
                        employerRepository,
                        currentUser,
                        clientListRepository,
                        documentRepository,
                        templateRepository,
                        employerWorkerRepository,
                        benefitListRepository){

    $scope.employeeCount = 0;
    $scope.brokerCount = 0;
    $scope.benefitCount = 0;
    $scope.templateCountArray = [];


   var getDocumentTypes = function(company){
      documentRepository.type.get({companyId:company.Id}).$promise.then(function(response){
        $scope.documentTypes = response.document_types;
      });
    }
    var getTemplates = function(company){
      templateRepository.byCompany.get({companyId:company.id}).$promise.then(function(response){
        $scope.templateArray = response.templates;
      });
    }
    var getWorkerCount = function(company){
      employerWorkerRepository.get({companyId:company.id})
        .$promise.then(function(response){
            _.each(response.user_roles, function(role){
              if(role.company_user_type.toLowerCase()==='employee')
              {
                $scope.employeeCount++;
              }
              else if(role.company_user_type.toLowerCase()==='broker')
              {
                $scope.brokerCount++;
              }
            })
        });
    };

    var getBenefitCount = function(company){
      benefitListRepository.get({clientId:company.id})
        .$promise.then(function(response){
            var benefitNameArray = [];
            _.each(response.benefits, function(benefit){
              var name = _.findWhere(benefitNameArray, {benefit_name:benefit.benefit_name});
              if(!name){
                benefitNameArray.push(benefit);
              }
            });
            $scope.benefitCount = _.size(benefitNameArray);
        });
    };

    var getTemplateCount = function(company){
      templateRepository.byCompany.get({companyId:company.id})
        .$promise.then(function(response){
          _.each($scope.documentTypes, function(type){
            $scope.templateCountArray[type.name] = 0;
          });

          _.each(response.templates, function(template){
            $scope.templateCountArray[template.document_type.name] ++;
          });
        });
    };

    var userPromise = currentUser.get()
      .$promise.then(function(response)
         {
            $scope.curUser = response.user;
            return response.user;
         }
    );
    var clientPromise = userPromise.then(function(user){
      return clientListRepository.get({userId:user.id}).$promise;
    });

    clientPromise.then(function(clientListResponse){
      _.every(clientListResponse.company_roles, function(company_role)
        {
          if(company_role.company_user_type.toLowerCase() === 'admin')
          {
            $scope.company = company_role.company;
            getDocumentTypes($scope.company);
            getTemplates($scope.company);
            getWorkerCount($scope.company);
            getBenefitCount($scope.company);
            getTemplateCount($scope.company);
            return false;
          }
          return true;
        });
    });

    $scope.addBrokerClick = function(companyId)
    {
       $location.path('/admin/broker/add/'+ companyId);
    }

    $scope.viewBrokerClick = function(companyId)
    {
        $location.path('/admin/broker/' + companyId);
    }

    $scope.viewBenefitsClick = function(companyId)
    {
       $location.path('/admin/benefits/'+ companyId);
    }

    $scope.addEmployeeClick = function(companyId)
    {
       $location.path('/admin/employee/add/'+ companyId);
    }

    $scope.viewEmployeeClick = function(companyId)
    {
       $location.path('/admin/employee/'+ companyId);
    }

    $scope.templateClick = function(companyId, docType)
    {
       $location.search({type:docType.name}).path('/admin/generate_template/'+ companyId);
    }
  }
]);

var employerUser = employersController.controller('employerUser',
                                                  ['$scope',
                                                  '$location',
                                                  '$routeParams',
                                                  'employerWorkerRepository',
                                                  'usersRepository',
                                                  'userDocument',
  function employerUser($scope,
                        $location,
                        $routeParams,
                        employerWorkerRepository,
                        usersRepository,
                        userDocument){
      var compId = $routeParams.company_id;
      $scope.employees=[];
      $scope.addUser = {};
      $scope.brokers = [];
      employerWorkerRepository.get({companyId:compId})
        .$promise.then(function(response){
            _.each(response.user_roles, function(role){
              if(role.company_user_type.toLowerCase()=='employee')
              {
                $scope.employees.push(role);
              }
              else if(role.company_user_type.toLowerCase()=='broker')
              {
                $scope.brokers.push(role);
              }
            })
        });

      var gotoUserView = function(userType){
        $location.path('/admin/' + userType.toLowerCase() + '/' + compId);
      }

      var mapToAPIUser = function(viewUser, userType){
        var apiUser = {};
        apiUser.company = compId;
        apiUser.company_user_type = userType;
        apiUser.user = {};
        apiUser.user.email = viewUser.email;
        apiUser.user.first_name = viewUser.first_name;
        apiUser.user.last_name = viewUser.last_name;
        if(viewUser.phone)
        {
            //input phone to the apiModel here
        }
        return apiUser;
      }

      var validateAddUser = function(addUser){
        if(addUser.first_name && addUser.last_name && addUser.email)
        {
          return true;
        }
        return false;
      }

      $scope.addLink = function(userType)
      {
        $location.path('/admin/'+ userType.toLowerCase() + '/add/'+compId);
      }

      $scope.createUser = function(userType){
        var sendEmail = $scope.addUser.send_email;
        if(validateAddUser($scope.addUser))
        {
          usersRepository.save(mapToAPIUser($scope.addUser, userType), function(){
              gotoUserView(userType);
            }, function(){
                $scope.saveSucceeded = false;
            });
        }
        else
        {
          $scope.validation_failed = true;
        }
      }
      $scope.gotoEmployerDashboardLink = function(){
        $location.path('/admin');
      }
      $scope.gotoUserViewLink = gotoUserView;

      $scope.documentLink = function(employeeId, docType)
      {
        userDocument.query({userId:employeeId})
        .$promise.then(function(response){
          var doc = _.filter(response, function(doc){return doc.document_type.id === docType});
          var pathKey = 'create_letter';
          if(doc && doc.length > 0)
          {
            pathKey='view_letter';
          }
          $location.search({type:getDocumentType(docType)}).path('/admin/' + pathKey + '/' +compId +'/'+employeeId);
        });

      }
  }
]);

var employerBenefits = employersController.controller('employerBenefits', ['$scope', '$location', '$routeParams', 'benefitListRepository',
  function employerBenefits($scope, $location, $routeParams, benefitListRepository){
    var compId = $routeParams.company_id;
    benefitListRepository.get({clientId:compId})
        .$promise.then(function(response){
            $scope.companyBenefitsArray = [];
            _.each(response.benefits, function(benefit){
                insertIntoBenefitArray($scope.companyBenefitsArray, benefit);
            });
        });
    var insertIntoBenefitArray = function(companyBenefitsArray, benefit)
    {
        var benefitType = benefit.benefit_plan.benefit_type.name;
        var array = _.findWhere(companyBenefitsArray, {type:benefitType});
        if(!array)
        {
            array = {type:benefitType, benefitList:[]};
            companyBenefitsArray.push(array);
        }
        var benefitName = benefit.benefit_plan.name;
        var sameBenefit = _.findWhere(array.benefitList, {name:benefitName})
        if(!sameBenefit)
        {
          var sameNameBenefit = {};
          sameNameBenefit.name = benefitName;
          sameNameBenefit.options = [];
          sameNameBenefit.options.push({
              optionType:benefit.benefit_option_type,
              totalCost:benefit.total_cost_per_period,
              employeeCost: benefit.employee_cost_per_period
            });
          array.benefitList.push(sameNameBenefit);
        }
        else
        {
          sameBenefit.options.push({
              optionType:benefit.benefit_option_type,
              totalCost:benefit.total_cost_per_period,
              employeeCost: benefit.employee_cost_per_period
          });
        }

    }
  }
]);

var employerLetterTemplate = employersController.controller('employerLetterTemplate', ['$scope', '$location', '$route', '$routeParams', 'templateRepository',
  function employerLetterTemplate($scope, $location, $route, $routeParams, templateRepository){
    $scope.documentType = $routeParams.type;
    $scope.addMode = $routeParams.add;
    $scope.companyId = $routeParams.company_id;
    $scope.viewTitle = 'Create ' + $scope.documentType + ' Template';
    $scope.showEditButton = false;
    $scope.existingTemplateList = [];

    $scope.isInAddMode = function(){
      return _.isEmpty($scope.existingTemplateList) || $scope.addMode === 'true';
    };

    var updateWithExistingTemplate = function(template)
    {
      if(template)
      {
        $scope.templateContent = template.content;
        $scope.templateName = template.name;
        $scope.showCreateButton = false;
        $scope.showEditButton = true;
      }
    }
    if(!$scope.addMode || $scope.addMode === 'false')
    {
      templateRepository.byCompany.get({companyId:$routeParams.company_id})
        .$promise.then(function(response){
          $scope.existingTemplateList = _.sortBy(
            _.filter(response.templates,
              function(template){
                return template.document_type.name === $scope.documentType;
            }),
            function(elm){return elm.id;}
          ).reverse();

          if(!_.isEmpty($scope.existingTemplateList))
          {
            $scope.viewTitle = 'Manage ' + $scope.documentType + ' Template';
          }
          else
          {
            $location.search({type:$scope.documentType, add:'true'});
          }
        });
    };
    $scope.modifyExistingTemplate = function(template){
      updateWithExistingTemplate(template);
    };
    $scope.saveTemplateChanges = function(){
      var template = {};
      template.name = $scope.templateName;
      template.content = $scope.templateContent;
      template.document_type = $scope.documentType;
      templateRepository.create.save({company: $scope.companyId, template: template}, function(response){
        updateWithExistingTemplate(response.template);
        $location.search({add:'false', type: $scope.documentType})
      }, function(response){
        $scope.templateCreateFailed = true;
      })
    }
    $scope.addOfferTemplate = function(){
      $location.search({type:$scope.documentType, add:'true'});
    };
    $scope.viewDashboard = function(){
      $location.path('/admin');
    };
    $scope.createTemplate = function(){
      if($scope.templateName && $scope.templateContent)
      {
        var newTemplate = {};
        newTemplate.document_type = $scope.documentType;
        newTemplate.name = $scope.templateName;
        newTemplate.content = $scope.templateContent;
        var postObj = {company:$scope.companyId, template:newTemplate};
        templateRepository.create.save(postObj, function(response){
          updateWithExistingTemplate(response.template);
          $scope.justCreated = true;
          $location.search({add:'false', type:$scope.documentType})
        }, function(response){
          $scope.templateCreateFailed = true;
        });
      }
    }
  }
]);

var employerCreateLetter = employersController.controller('employerCreateLetter',
                                                          ['$scope',
                                                          '$location',
                                                          '$routeParams',
                                                          'documentRepository',
                                                          'templateRepository',
  function employerCreateLetter($scope,
                                $location,
                                $routeParams,
                                documentRepository,
                                templateRepository){
    $scope.companyId = $routeParams.company_id;
    var employeeId = $routeParams.employee_id;
    $scope.newDoc = {};


    $scope.documentType = $routeParams.type;

    templateRepository.byCompany.get({companyId:$scope.companyId})
      .$promise.then(function(response){
        $scope.templateArray = [];

        _.each(response.templates, function(template){
          if (template.document_type.name === $scope.documentType){
            $scope.templateArray.push(template);
          }
        });

        _.sortBy($scope.templateArray, function(template){
          return template.name;
        });
      });

    $scope.getTemplateFields = function(sTemplate){
      if(sTemplate)
      {
        var fieldList = _.uniq(sTemplate.fields, false, function(field){
          return field.name;
        });
        return fieldList;
      }
      else
      {
        return [];
      }
    };

    $scope.doCreateLetter = function()
    {
      var curTemplate = $scope.selectedTemplate;
      $scope.newDoc.fields = curTemplate.fields;
      _.each($scope.newDoc.fields, function(field){
        if(!field.value){
          var foundValue = _.findWhere($scope.newDoc.fields, {name:field.name});
          if(foundValue){
            field.value = foundValue.value;
          }
        }
      });
      $scope.newDoc.document_type = $scope.documentType;
      var postObj={company:$scope.companyId, user:employeeId, template:curTemplate.id, signature:'', document:$scope.newDoc};
      documentRepository.create.save(postObj, function(response){
        $location.search({type:$scope.documentType}).path('/admin/view_letter/' + $scope.companyId + '/' + employeeId);
      }, function(errResponse){
        $scope.createFailed = true;
      });
    }
  }]);

var employerViewLetter = employersController.controller('employerViewLetter',
                                                          ['$scope',
                                                          '$location',
                                                          '$routeParams',
                                                          'documentRepository',
  function employerViewLetter($scope,
                              $location,
                              $routeParams,
                              documentRepository){
    $scope.companyId = $routeParams.company_id;
    var employeeId = $routeParams.employee_id;
    $scope.documentType = $routeParams.type;
    $scope.documentList = [];
    $scope.activeDocument = {};


    documentRepository.byUser.query({userId:employeeId})
      .$promise.then(function(response){

        var unsortedDocumentList = _.filter(
            response,
            function(doc){
              return doc.document_type.name === $scope.documentType
            });
        $scope.documentList = _.sortBy(unsortedDocumentList, function(elm){return elm.id;}).reverse();
      });

    $scope.anyActiveDocument = function(){
      return typeof $scope.activeDocument.name !== 'undefined';
    }

    $scope.viewExistingLetter = function(doc){
      $scope.activeDocument = doc;
    };

    $scope.createNewLetter = function(){
      $location.search({type:$scope.documentType}).path('/admin/create_letter/'+ $scope.companyId +'/' + employeeId);
    };

    $scope.viewEmployeesLink = function(){
      $location.path('/admin/employee/' + $scope.companyId);
    };
  }]);
