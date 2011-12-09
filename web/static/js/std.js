define(function(require, exports, modules){
	var $ = require('jquery');
	var disDiv = '<div id="disDiv"></div>';
	var activeObj;
	exports.active = function(obj){
		activeObj = $(obj).clone();
		$(obj).html('处理中...').removeClass().addClass('btn disabled');
		$(obj).off();
	};

	exports.cancel = function(id, ctx){
		$('#' + id).hide().fadeIn('slow').html(ctx);    
		return 1;
	};

	exports.cacheMain = function(){
		return $('#main').html();
	};

	exports.validAllNotEmpty = function(obj){
		for(var pro in obj)
		{
			if(obj[pro] == '') return false;
		}

		return true;
	};

	exports.alertErrorBox = function(id, msg, isClose){
		if($('#errorBoxDiv').length > 0)
			return $('#errormsg').html(msg);

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
		$('#disDiv').html(alerts).fadeOut(600).fadeIn(600);
	};

	exports.resetActive = function(obj){
		alert(activeObj);
		$(obj).removeClass().html(activeObj.html()).addClass(activeObj.attr('class'));
		$(obj).attr('disabled', false);
	};

	exports.getJson = function(type, url, data, callback){
		$.ajax({type: type, url: url, data:data, dataType: 'json', success:callback});
	};
});