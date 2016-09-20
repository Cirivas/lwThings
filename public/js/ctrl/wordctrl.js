var app = angular.module('signit', ['ngResource'])
.factory('wordsResource', ['$resource', function($resource){
	return $resource('http://191.235.92.8/test',{},{})	
}])
.controller('WordCtrl', ['$scope', 'wordsResource', function($scope, wordsResource){
	$scope.words = wordsResource.query();
}]);