var app = angular.module('signit', ['ngResource'])
.factory('wordsResource', ['$resource', function($resource){
	return $resource('http://localhost:8080/test',{},{})	
}])
.controller('WordCtrl', ['$scope', 'wordsResource', function($scope, wordsResource){
	$scope.words = wordsResource.query();
}]);