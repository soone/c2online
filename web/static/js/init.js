seajs.config({
    alias:{
        'jquery':'jquery-1.7.1.min.js',
    }
});

define(function(require){
	var $ = require('jquery');
    $(document).ready(function(){
		require('project').init();
    });
});
