var androidApp = angular.module('androidApp', [
	'ui.bootstrap',
	'ngRoute',
	'androidControllers'
]);

androidApp.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl	: 'partials/home.html',
				controller	: 'mainController'
			})

			.when('/data', {
				templateUrl	: 'partials/data.html',
				controller	: 'dataController'
			})

			.when('/about', {
				templateUrl	: 'partials/about.html',
				controller	: 'aboutController'
			});
	}]);