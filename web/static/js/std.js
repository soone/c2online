define(function(require, exports, modules){
	var $ = require('jquery');
	var disDiv = '<div id="disDiv"></div>';
	var activeObj = {};
	exports.active = function(objId){
		activeObj[objId] = $('#' + objId).clone();
		$('#' + objId).replaceWith('<a href="javascript:;" class="btn disabled" id="_actioning_' + objId + '">处理中...</a>');
	};

	exports.resetActive = function(objId){
		$('#_actioning_' + objId).replaceWith(activeObj[objId]);
	};

	exports.cancel = function(id, ctx){
		$('#' + id).hide().fadeIn('slow').html(ctx);    
		return true;
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
		{
			$('#errormsg').html(msg);
			$('#disDiv').fadeOut(600).fadeIn(600);
			return;
		}

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

	exports.getJson = function(type, url, data, callback){
		$.ajax({type: type, url: url, data:data, dataType: 'json', success:callback});
	};

	exports.getLocalTime = function(nS){
		if(!parseInt(nS)) return '';
		return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/时|分/g, ":").replace(/秒/g, "").replace(/日|星期.*\ /g, '');
	};

	//返回页码的开始和结束
	exports.setPage = function(page, max, sep)
	{
		if(!sep) sep = 2;
		var maxPage = sep*2+1;
		var prev = page - sep;
		var next = page + sep;
		var min = max - maxPage + 1;
		if((prev <= 0 && next >= max) || (prev > 0 && next >= max))
			return min > 0 ? [min, max] : [1, max];

		if(prev <= 0 && next < max)
			return min > 0 ? [1, maxPage] : [1, max];

		if(prev > 0 && next < max)
			return min > 0 ? [prev, next] : [prev, max];
	};

	//返回url的QueryString
	exports.queryString = function()
	{
		var str = location.href;
		var start = str.indexOf('?');
		var qStr = str.substr(start + 1);
		var qStrArr = qStr.split('&');
		var resArr = {};
		for(i = 0, j = qStrArr.length; i < j; i++)
		{
			var tempArr = qStrArr[i].split("=");
			if(i == 0 && tempArr.length == 1)
				return qStr;

			resArr[tempArr[0]] = tempArr[1];
		}

		return resArr;
	};
});
