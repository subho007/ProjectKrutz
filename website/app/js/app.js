var androidApp = angular.module('androidApp', [
	'ui.bootstrap',
	'ui.select',
	'ngSanitize',
	'ngRoute',
	'androidControllers'
]);

androidApp.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl	: 'partials/home.html',
				controller	: 'MainController'
			})

			.when('/data', {
				templateUrl	: 'partials/data.html',
				controller	: 'DataController'
			})

			.when('/about', {
				templateUrl	: 'partials/about.html',
				controller	: 'AboutController'
			});
	}]);