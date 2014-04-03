var androidControllers = angular.module('androidControllers', []);

androidControllers.controller('NavController', function($scope, $location) {
	$scope.isCollapsed = true;
	$scope.$on('$routeChangeSuccess', function() {
		$scope.isCollapsed = true;
	});

	$scope.getClass = function(path) {
		if (path === '/') {
			if ($location.path() === '/') {
				return 'active';
			} else {
				return '';
			}
		}

		if ($location.path().substr(0, path.length) === path) {
			return 'active';
		} else {
			return '';
		}
	}
});

androidControllers.controller('MainController', function($scope) {
	$scope.message = 'Home';
});

androidControllers.controller('DataController', function($scope) {
	$scope.message = 'Data';
});

androidControllers.controller('AboutController', function($scope) {
	$scope.message = 'About';
});