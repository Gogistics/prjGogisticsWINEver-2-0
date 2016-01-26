/*
 * front_page.js
 * 1. handle base template
 * 2. handle whole front-end templates routing
 * 
 * */
(function(){
    'use strict';
	/* Angular.js */
	// declare app level module which depends on filters, and services, and modify $interpolateProvider to avoid the conflict with jinja2' symbol
	window.front_page_app = window.front_page_app || angular.module('frontPageApp', [ 'angular-responsive', 'ui.router', 'ngAnimate' ], function($interpolateProvider) {
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');
	});

	// global values
	window.front_page_app.value('GLOBAL_VALUES',{
		EMAIL : 'gogistics@gogistics-tw.com'
	});

	// app-routing configuration
	window.front_page_app.config(function(responsiveHelperProvider, $stateProvider, $urlRouterProvider) {
		// templates dispatcher which redirect visitors to appropriate templates;
		// currently, there are desktop and mobile versions
        var device = responsiveHelperProvider.$get().isMobile() ? 'mobile' : 'desktop';
		
		// nested templates and routing
		$stateProvider
		.state('home', {
			templateUrl: '/my_ng_templates/my_ng_template_base.html',
		})
		.state('front_page', {
			url: '/',
			parent: 'home',
			templateUrl: '/my_ng_templates/my_ng_front.html',
			controller: 'frontPageCtrl'
		});

		$urlRouterProvider.otherwise('/'); // for defualt state routing; for current routing mechanism, it's not necessary
	});

	
	/* controllers */
	// dispatch controllers are used for building the connection between jinja templates and ng templates
	var frontPageDispatchController = function ($state, $scope, GLOBAL_VALUES) {
		$scope.email = GLOBAL_VALUES.EMAIL;
	    $state.transitionTo('front_page');
	}
	frontPageDispatchController.$injector = ['$state', '$scope', 'GLOBAL_VALUES'];
	window.front_page_app.controller('frontPageCtrl', frontPageDispatchController);
})();

