seajs.config({
    alias:{
        'jquery':'jquery-1.7.1.min.js'
    }
});

define(function(require){
    var $ = require('jquery');
    var project = require('project');
    $(document).ready(function(){
        $('#createpro').click(function(){
            project.show('createpro');
        });
    });
});