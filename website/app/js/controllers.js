var androidControllers = angular.module('androidControllers', []);

androidControllers.controller('mainController', function($scope) {
	$scope.message = 'Home';
});

androidControllers.controller('dataController', function($scope) {
	$scope.message = 'Data';
});

androidControllers.controller('aboutController', function($scope) {
	$scope.message = 'About';
});