/*
 * logs_monitor.js
 * */
(function(){
    'use strict';
	/* Angular.js */
	// declare app level module which depends on filters, and services, and modify $interpolateProvider to avoid the conflict with jinja2' symbol
	window.logs_monitor_app = window.logs_monitor_app || angular.module('logsMonitorApp', [ 'angular-responsive', 'ui.router', 'ngAnimate' ], function($interpolateProvider) {
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');
	});

	// global values
	window.logs_monitor_app.value('APP_VALUES',{
		EMAIL : 'gogistics@gogistics-tw.com'
	});

	// app-routing configuration
	window.logs_monitor_app.config(function(responsiveHelperProvider) {
		// templates dispatcher which redirect visitors to appropriate templates;
		// currently, there are desktop and mobile versions
        var device = responsiveHelperProvider.$get().isMobile() ? 'mobile' : 'desktop';

	});

	// controller
	window.logs_monitor_app.controller('logsMonitorCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout){
        var ctrl = this;
        ctrl.sorted_list = []; // latest 100 logs
        ctrl.get_logs = function(){
            $http({
                method : "GET",
                url : "https://www.scalyr.com/fake/getLiveTail?query=foo"
            }).then(function handle_success(response) {
                if( response.status === 200 &&
                    response.data &&
                    response.data.entries &&
                    response.data.entries.length > 0){
                    
                    var ary = response.data.entries.slice(0);
                    while(ary.length > 0){
                        var temp_elem = ary.pop();
                        ctrl.sorted_list = ctrl.binary_search(temp_elem, ctrl.sorted_list);
                    }
                    
                    while(ctrl.sorted_list.length > 100){
                        ctrl.sorted_list.shift();
                    }
                }
                // keep quering
                $timeout(function(){ctrl.get_logs()}, 5000);
            }, function handle_error(response) {
                // keep quering
                $timeout(function(){ctrl.get_logs()}, 5000);
            });
        }
        
        ctrl.binary_search= function(arg_searched_elem, arg_ary) {
            if(arg_ary.length === 0){
                arg_ary.push(arg_searched_elem);
                return arg_ary;
            }
            
            var min_index = 0;
            var max_index = arg_ary.length - 1;
            var current_index;
            var current_element;
         
            while (min_index <= max_index) {
                current_index = (min_index + max_index) / 2 | 0;
                current_element = arg_ary[current_index];
         
                if (current_element['timestamp'] < arg_searched_elem['timestamp']) {
                    min_index = current_index + 1;
                }
                else if (current_element['timestamp'] > arg_searched_elem['timestamp']) {
                    max_index = current_index - 1;
                }
                else {
                    arg_ary.splice(current_index, 0, arg_searched_elem);
                    return arg_ary;
                }
            }
            
            // if not found
            if(current_index === 0 && current_element['timestamp'] > arg_searched_elem['timestamp']){
                arg_ary.unshift(arg_searched_elem);
              return arg_ary;
            }else if(current_index === 0 && current_element['timestamp'] < arg_searched_elem['timestamp']){
                arg_ary.splice(0, 0, arg_searched_elem);
              return arg_ary;
            }else if(current_index > 0 && current_index <= arg_ary.length - 1 && current_element['timestamp'] < arg_searched_elem['timestamp']){
                arg_ary.splice(current_index + 1, 0, arg_searched_elem);
              return arg_ary;
            }else if(current_index > 0 && current_index <= arg_ary.length - 1 && current_element['timestamp'] > arg_searched_elem['timestamp']){
                arg_ary.splice(current_index, 0, arg_searched_elem);
              return arg_ary;
            }
        }
            
        // start to get logs
        ctrl.get_logs();
    }]);
})();

