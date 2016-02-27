/*
 * index_page.js
 * 1. handle base template
 * 2. handle whole front-end templates routing
 * 
 * */
(function(){
    'use strict';
	/* Angular.js */
	// declare app level module which depends on filters, and services, and modify $interpolateProvider to avoid the conflict with jinja2' symbol
	window.index_page_app = window.index_page_app || angular.module('indexPageApp', [ 'angular-responsive', 'ui.router', 'ngAnimate' ], function($interpolateProvider) {
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');
	});

	// global values
	window.index_page_app.value('GLOBAL_VALUES',{
		EMAIL : 'gogistics@gogistics-tw.com'
	});

	// app-routing configuration
	window.index_page_app.config(function(responsiveHelperProvider, $stateProvider, $urlRouterProvider) {
		// templates dispatcher which redirect visitors to appropriate templates;
		// currently, there are desktop and mobile versions
        var device = responsiveHelperProvider.$get().isMobile() ? 'mobile' : 'desktop';
		
		// nested templates and routing
		$stateProvider
		.state('home', {
			templateUrl: '/my_ng_templates/my_ng_template_base.html',
		})
		.state('index_page', {
			parent: 'home',
			templateUrl: '/my_ng_templates/my_ng_index.html',
			controller: 'indexPageCtrl'
		})
        .state('search_wine', {
			url : '/search_wine',
			parent : 'index_page',
			templateUrl : '/my_ng_templates/my_ng_index_search_wine.html'
		})
        .state('my_favorites', {
			url : '/my_favorites',
			parent : 'index_page',
			templateUrl : '/my_ng_templates/my_ng_index_favorites.html'
		});

		$urlRouterProvider.otherwise('/search_wine'); // for defualt state routing; for current routing mechanism, it's not necessary
	});

	// controllers are used for building the connection between jinja templates and ng templates
	var indexPageController = function ($state, $scope, GLOBAL_VALUES) {
		$scope.email = GLOBAL_VALUES.EMAIL;
	    $state.transitionTo('search_wine'); // set init view
        var ctrl = this;
        ctrl.selected = $state.current.name;
        
        // toggle views
        ctrl.is_list_open = false;
        ctrl.toggle_list = function(){
			ctrl.is_list_open = !ctrl.is_list_open;
			if($("#list_block").hasClass( "fadeOutLeft") && ctrl.is_list_open){
				$("#list_block").removeClass('fadeOutLeft');
				$("#list_detail").removeClass('list_display_none');
				$("#list_block").addClass('list_block_show fadeInLeft');
				
			}else{
				$("#list_block").removeClass('fadeInLeft');
				$("#list_block").addClass(' fadeOutLeft');
				
				if(!ctrl.is_list_open){
					$("#list_block").removeClass('list_block_show');
					$("#list_detail").addClass('list_display_none');
				}
			}
		};
        
        // selector
        ctrl.select_topic = function(arg_selected_tag){
            // set selected page name
            ctrl.selected = arg_selected_tag;
            $state.transitionTo(ctrl.selected);
            ctrl.toggle_list();
        }
        ctrl.is_selected = function(arg_selected_tag){
            // check if selected tag name
            return (ctrl.selected === arg_selected_tag);
        }
	}
	indexPageController.$injector = ['$state', '$scope', 'GLOBAL_VALUES'];
	window.index_page_app.controller('indexPageCtrl', indexPageController);
    
    var wineInfoQueryController = function ($state, $scope, $http, GLOBAL_VALUES) {
		$scope.email = GLOBAL_VALUES.EMAIL;
        var ctrl = this;
        ctrl.has_query_result = false;
        ctrl.query_keywords = '';
        ctrl.snooth_query_result_list = [];
        
        // save
        ctrl.save = function(arg_key, arg_info, event){
            //
        }
        
        ctrl.is_info_saved = function(arg_key, arg_info, event){
            //
            return 'Save';
        }
        
        ctrl.open_url = function(arg_url){
            //
        }
        
        //
        ctrl.search_wine_info = function(){
            // popup loader gif
			$("#preloader").css({ display : "block"});
			
			// check if query str is empty
			if(ctrl.query_keywords.trim().length <= 0){
				//
				alert("query string is empty!");
				$("#preloader").css({ display : "none"});
				return false;
			}
			
			// query string for average price
			var query_data = $.param({ query_info : ctrl.query_keywords.trim()});
			console.log(query_data);
			var req = {
					 method: 'POST',
					 url: '/query/search_wine_info',
					 headers: {
					   'Content-Type': 'application/x-www-form-urlencoded',
					 },
					 data: query_data,
				};
			$http(req)
			.success(function(data, status, headers, config){
                // start to build lists
                ctrl.has_query_result = false;
                ctrl.snooth_query_result_list = [];
                ctrl.wine_searcher_result_list = [];
                ctrl.vivno_result_list = [];
                var snooth_query_result = data.snooth_query_result,
                    wine_searcher_query_result = data.wine_searcher_query_result,
                    vivino_query_result = data.vivino_query_result;
                    
                // Snooth
                if(snooth_query_result.meta.staus === 0){
                    // popup error message
                    alert(snooth_query_result.meta.errmsg);
                    return false;
                }
                if(snooth_query_result.wines){
                    ctrl.has_query_result = true;
                    // append info
                    ctrl.snooth_query_result_list = snooth_query_result.wines;
                }else{
                    //
                    alert('No result from Snooth');
                }
                
                // wine searcher
                if(wine_searcher_query_result && wine_searcher_query_result.length > 0){
                    ctrl.has_query_result = true;
                    // append info
                    ctrl.wine_searcher_result_list = wine_searcher_query_result;
                    console.log(wine_searcher_query_result);
                }else{
                    //
                    alert('No result from Wine Searcher');
                }
                
                // vivino
                if(vivino_query_result && vivino_query_result.length > 0){
                    //
                    ctrl.has_query_result = true;
                    ctrl.vivno_result_list = vivino_query_result;
                    console.log(vivino_query_result);
                }else{
                    alert('No result from Vivino');
                }
                
                $("#preloader").css({ display : "none"});
			})
            .error(function(data, status, headers, config){
                alert('Server is busy; please try later');
                $("#preloader").css({ display : "none"});
            });
        }
        ctrl.search_wine_info_of_keyup = function(event){
            if(event.keyCode === 13){
                ctrl.search_wine_info();
            }
        }
        
        // check if result is empty
        ctrl.replace_empty_str = function(arg_str){
            arg_str = (arg_str === null || arg_str === '') ? 'NA' : arg_str;
            return arg_str;
        }
	}
	wineInfoQueryController.$injector = ['$state', '$scope', '$http', 'GLOBAL_VALUES'];
	window.index_page_app.controller('wineInfoQueryCtrl', wineInfoQueryController);
})();

