define(function(require, exports, modules){
	var $ = require('jquery');
	var disDiv = '<div id="disDiv"></div>';
	exports.active = function(obj){
		$(obj).html('处理中...').removeClass().addClass('btn disabled');
	};

	exports.cancel = function(id, ctx){
		$('#' + id).hide().fadeIn('slow').html(ctx);    
		return 1;
	};

	exports.cacheMain = function(){
		return $('#main').html();
	};

	exports.validAllNotEmpty = function(arr){
		for(var i = 0, j = arr.length; i < j; i++)
		{
			if(arr[i] == '')
				return false;
		}

		return true;
	};

	exports.alertErrorBox = function(id, msg, isClose){
		if($('#errorBoxDiv').length > 0)
			$('#errormsg').html(msg);

		var alerts = '<div id="errorBoxDiv" class="alert-message block-message error">'
		if(isClose == 1)
		{
			alerts += '<a class="close" href="javascript:;" id="errorbox">X</a>';
			$('#errorbox').live('click', function(){
				$(this).parent().fadeOut();
			});
		}
		alerts += '<strong>Error:</strong><span id="errormsg">' + msg + '</span>';
		alerts += '</div>';
		$('#'+id).before(disDiv);
		$('#disDiv').html(alerts);
	};
});
