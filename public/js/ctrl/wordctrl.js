var app = angular.module('signit', ['ngResource'])
.factory('wordsResource', ['$resource', function($resource){
	return $resource('http://signit.brazilsouth.cloudapp.azure.com/test',{},{})	
}])
.controller('WordCtrl', ['$scope', 'wordsResource', function($scope, wordsResource){
	$scope.words = wordsResource.query();
}]);