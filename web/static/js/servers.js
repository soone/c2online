define(function(require, exports, module){
    var $ = require('jquery');
	var std = require('std');
	var main = std.cacheMain();//主框架缓存变量
    var createser = '<ul class="breadcrumb"><li><a href="/servers">服务器管理</a><span class="divider">/</span></li><li class="active">创建服务器</li></ul><form class="form-stacked" id="serform"><fieldset><div class="clearfix"><label for="pid">所属项目*</label><div class="input"><select name="pid" id="pid"><option value="">请选择</option></select></div></div><div class="clearfix"><label for="sname">名称*</label><div class="input"><input type="text" id="sname" class="xlarge" size="30" name="sname" /></div></div><div class="clearfix"><label for="pdir">在线物理地址*</label><div class="input"><input type="text" id="pdir" class="span8" size="256" name="pdir" /><span class="help-block">比如：/data/wwwV2/</span></div></div><div class="clearfix"><label for="pdir">在线备份地址*</label><div class="input"><input type="text" id="bdir" class="span8" size="256" name="bdir" /><span class="help-block">比如：/data/release/</span></div></div><div class="clearfix"><label for="spath">Host地址*</label><div class="input"><input type="text" id="spath" class="span8" size="256" name="spath" /><span class="help-block">比如：192.168.1.253</span></div></div><div class="clearfix"><label for="suser">用户名*</label><div class="input"><input type="text" id="suser" name="suser" /></div></div><div class="clearfix"><label for="spass">密码*</label><div class="input"><input type="password" id="spass" name="spass" /></div></div><div class="clearfix"><label for="vpnpro">vpn网关</label><div class="input"><select name="vpnpro" class="mini"><option value="1">PPTP</option></select>&nbsp;<input type="text" placeholder="192.168.1.253" id="svpn" class="span5" size="256" name="svpn" /></div></div><div class="clearfix"><label for="vpnname">vpn帐号</label><div class="input"><input type="text" id="vpnname" name="vpnname" /></div></div><div class="clearfix"><label for="vpnpass">vpn密码</label><div class="input"><input type="password" id="vpnpass" name="vpnpass" /></div></div></fieldset><div class="actions"><button class="btn primary" id="sersubmit">提交</button>&nbsp;<button class="btn" id="cancel">取消</button></div></form>';

	exports.init = function(){
		//显示创建表单
        $('#createser').live('click', function(){
			$('#main').hide().fadeIn('slow').html(createser);
			//取得项目列表
			$.getJSON('/project/shortlist/', function(data){
				if(data['res'] == 1)
				{
					for(var i = 0, j = data['list'].length; i < j; i++)
					{
						$('#pid').append('<option value="' + data['list'][i].p_id + '">' + data['list'][i].p_name + '</option>');
					}
				}
				else
					std.alertErrorBox('serform', data['msg']);
			});
		});
		//点击取消按钮
		$('#cancel').live('click', function(){var cancel = std.cancel('main', main);});
		//提交创建表单
		$('#serform').live('submit', function(){
			std.active($('#sersubmit'));
			$('#sersubmit').attr('disabled', true);
			var postData ={};
			postData.sname = $('#sname').val();
			postData.pdir = $('#pdir').val();
			postData.bdir= $('#bdir').val();
			postData.spath = $('#spath').val();
			postData.suser = $('#suser').val();
			postData.spass = $('#spass').val();
			postData.pid = $('#pid').val();
			if(std.validAllNotEmpty(postData) == false)
			{
				std.alertErrorBox('serform', '带*号不能为空');
				std.resetActive($('#sersubmit'));
				return false;
			}

			postData.svpn = $('#svpn').val();
			postData.svpnname = $('#svpnname').val();
			postData.svpnpass = $('#svpnpass').val();

			std.getJson('post', '/servers/create/', postData, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('serform', data['msg']);
					std.resetActive($('#sersubmit'));
					return false;
				}
				else
				{
					location.href = "/servers/";
					return false;
				}
			});

			return false;
		});

		//设置项目列表信息为可编辑
		$('td[id^="vcs"]').live('dblclick', function(){
			var val = $(this).text();
			var id = $(this).attr('id');
			$(this).html('<input type="text" value="' + val + '" id="edit_' + id + '" />');
			$('#edit_' + id).focus();
		});

		//保存项目列表编辑项
		$('input[id^="edit_"]').live('blur', function(){
			var val = $(this).val();
			var id = $(this).attr('id');
			if(!val){
				std.alertErrorBox('tlist', '该值不能为空');
				return false;
			}

			var p = id.split('_');
			std.getJson('post', '/project/update/', {name: p[1], id: p[2], val: val}, function(data){
				if(!data['res'])
					std.alertErrorBox('tlist', data['msg']);
				else
					$('#'+id).parent().html(val);
			});
		});

		//项目列表状态修改函数
		function changeStatus(obj, status){
			std.active(obj);
			var checkboxs = $('input[name="pcheck[]"]:checked');
			if(!checkboxs.length)
			{
				std.alertErrorBox('tlist', '请至少选择一项1');
				std.resetActive(obj);
				return false;
			}

			var sValues = new Array();
			checkboxs.each(function(){sValues.push($(this).val());});
			std.getJson('post', '/project/change/', {checkboxs: sValues.join('|'), status: status}, function(data){
				if(!data['res'])
				{
					std.alertErrorBox('tlist', data['msg']);
					std.resetActive(obj);
				}
				else
					location.href = "/project/";
			});
		};

		//项目状态开启关闭操作
		$('#popen').live('click', function(){changeStatus(this, 1)});
		$('#pclose').live('click', function(){changeStatus(this, 2)});

		//显示打包操作
		$('a[id^="package_"]').live('click', function(){
			var pInfo = $(this).attr('id').split('_');
			main = std.cacheMain();
			$('#main').hide().fadeIn('slow').html(goPack);
			$('#pname').html(pInfo[2]);
			$("#pcurid").val(pInfo[1]);
		});

		//根据版本号显示项目打包的文件信息
		$('#govcs').live('click', function(){
			std.active(this);
			var vIds = $('#vids').val();
			var vIdsArr = vIds.split(',');
			var vIdLen = vIdsArr.length;
			var pro = $('#pcurid').val();
			if(!vIdLen)
			{
				std.alertErrorBox('vids', '请输入版本号，多个版本号用半角逗号隔开');
				std.resetActive(this);
				return false;
			}

			for(var i = 0; i < vIdLen; i++)//判断版本合法性
			{
				if(isNaN(vIdsArr[i]))
				{
					std.alertErrorBox('vids', '请输入纯数字版本号');
					std.resetActive(this);
					return false;
				}
			}

			vIds = vIds.split(',').join('|');
			std.getJson('post', '/project/vcslist/', {pro: pro, vids: vIds}, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('vids', data['msg']);
					std.resetActive($('#govcs'));
					return false;
				}
				else
				{
					if($('#main > table').length == 0) $('#main').append(listTable);
					$('#main > table > tbody').html('');
					var tbodys = [];
					for(var i = 0, j = data['logs'].length; i < j; i++)
					{
						var files = [];
						for(var x = 0, y = data['logs'][i][1].length; x < y; x++)
						{
							files.push('<li><input type="checkbox" name="vf[]" id="vf_' + data['logs'][i][0] + '_' + x + '" value="' + data['logs'][i][0] + '::' + data['logs'][i][1][x][0] + '::' + data['logs'][i][1][x][1] + '"/><span class="help-inline">' + data['logs'][i][1][x][0] + ' ' +  data['logs'][i][1][x][1] + '</span></li>');
						}

						$('#main > table > tbody').append('<tr><td><input type="checkbox" id="total_' + data['logs'][i][0] + '" name="all" /></td><td><p>r' + data['logs'][i][0] + '</p></td><td><ul class="unstyled packhide">' + files.join('') + '</ul></td></tr>');
					}

					std.resetActive($('#govcs'));
				}
			});
		});

		//项目打包文件选项操作开始
		$('input[id^="total_"]').live('click', function(){
			var id = $(this).attr('id').split('_')[1];
			var val = $(this).attr('checked');
			var checked = val == 'checked' ?  true : false;
			$('input[id^="vf_'+id+'"]').each(function(){$(this).attr('checked', checked)});
		});

		$('#alltotal').live('click', function(){
			var val = $(this).attr('checked');
			var checked = val == 'checked' ?  true : false;
			$('input[id^="total_"]').each(function(){$(this).attr('checked', checked)});
			$('input[id^="vf_"]').each(function(){$(this).attr('checked', checked)});
		});

		$('input[id^="vf_"]').live('click', function(){
			var id = $(this).attr('id');
			var idArr = id.split('_');
			var totalId = 'total_' + idArr[1];
			var vfIds = idArr[0] + '_' + idArr[1];
			var val = $(this).attr('checked');
			if(val != 'checked')
			{
				$('#' + totalId).attr('checked', false);
				$('#alltotal').attr('checked', false);
			}
			else if($('input[id^="' + vfIds + '"]:checked').length == $('input[id^="' + vfIds + '"]').length)
					$('#' + totalId).attr('checked', true);
		});
		//项目打包文件选项操作结束

		//打版本号操作
		$('#startpack').live('click', function(){
			var isSub = $(this).attr('class').indexOf('disabled');
			std.active(this);
			var checkboxs = $('input[id^="vf_"]:checked');
			var version = $('#version').val();
			if(!checkboxs.length || !version)
			{
				std.alertErrorBox('version', '请填写版本号并且至少选择一个文件');
				std.resetActive(this);
				return false;
			}

			if(isSub > -1) return false;
			//组织数据发送服务器
			var pro = $('#pcurid').val();
			var cVals = [];
			checkboxs.each(function(){cVals.push($(this).val())});
			alert(cVals.join('|'));
			std.getJson('post', '/project/package/', {verno : version, pro : pro, vals : cVals.join('|')}, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('version', data['msg']);
					std.resetActive($('#startpack'));
					return false;
				}
				else
					showPackList($('#pname').text(), pro);
			});
		});

		//显示项目已经打包的列表
		$('a[id^="packlist_"]').live('click', function(){
			var pInfo = $(this).attr('id').split('_');
			showPackList(pInfo[2], pInfo[1]);
		});

		//页码按钮事件
		$('a[id^="p_page_"]').live('click', function(){
			var id = $(this).attr('id').split('_')[2];
			var curPage = parseInt($('a[id^="p_page_"]').parent('.active').text());
			if(id ==curPage) return false;

			if(id == 'prev' && curPage == 1) return false;
			if(id == 'prev' && curPage > 1)
				return getPackageList($('#pcurid').val(), curPage-1);

			if(id == 'next') 
			{
				if($(this).parent('.disabled').get(0))
					return false
				else
					return getPackageList($('#pcurid').val(), curPage+1);
			}

			getPackageList($('#pcurid').val(), parseInt($(this).text()));
		});

		//点击包名称显示详细
		$('a[id^="p_detail_"]').live('click', function(){
			var id = $(this).attr('id').split('_')[2];
			if($('#detail_' + id).length == 1) return $('#detail_' + id).parent().remove();
			var detail = '<tr><td id="detail_' + id + '" colspan="7">正在读取...</td></tr>';
			$(this).parents('tr').after(detail);
			$.getJSON('/project/packdetail/' + id, function(data){
				var dListTr = '';
				if(data['res'] == 1)
				{
					var dls = data['list'];
					dListTr = '<ol>';
					for(var i = 0, j = dls.length; i < j; i++)
					{
						dListTr += '<li>r' + dls[i].f_ver + '&nbsp;&nbsp;' + dls[i].f_path + '</li>';
					}

					dListTr += '</ol>';
				}
				else
					dListTr = 'Oops... 读取失败';

				$('#detail_' + id).html(dListTr);
			});
		});

		//点击设置删除包
		$('a[id^="p_chastatus_"]').live('click', function(){
			if($(this).hasClass('disabled')) return false;

			var idArr = $(this).attr('id').split('_');
			var type = idArr[2];
			var id = idArr[3];
			std.active(this);
			$.getJSON('/project/packstatus/' + type + '/' + id, function(data){
				if(data['res'] == 1)
				{
					if(type == 2)
					{
						$('#status_' + id).html('<span class="label warning">已删除</span>');
						$('#p_chastatus_' + type + '_' + id).parent().html('<a href="javascript:;" id="p_chastatus_1_' + id + '" class="btn">设置为待发布</a>');
					}
					else
					{
						$('#status_' + id).html('<span class="label important">待发布</span>');
						$('#p_chastatus_' + type + '_' + id).parent().html('<a href="javascript:;" id="p_chastatus_2_' + id + '" class="btn">删除</a>');
					}
				}
				else
					$('#p_chastatus_' + type + '_' + id).parent().html('<span class="label warning">Oops..' + data['msg'] + '</span>');
			});
		});

		function getPackageList(pId, page)
		{
            page = !page ? 1 : page;
			$('#listtable').ready(function(){
				$('#listtable > tbody').html('<tr><td colspan="7" style="text-align:center">正在读取,请稍候...</td></tr>');
				$.getJSON('/project/packlist/' + pId + '/' + page, function(data){
					if(data['res'] == 1)
					{
						var ls = data['list'];
						var listTr = '';
						for(var i = 0, j = ls.length; i < j; i++)
						{
							listTr += '<tr><td><input type="checkbox" name="package" value="' + ls[i].r_id + '"/></td>';
							listTr += '<td><a href="javascript:;" id="p_detail_' + ls[i].r_id + '">' + ls[i].r_no + '</a></td>';
							listTr += '<td>' + getLocalTime(ls[i].r_cdateline) + '</td><td id="status_' + ls[i].r_id + '">';
							if(ls[i].r_status == 1)
								listTr += '<span class="label important">待发布</span>';
							else if(ls[i].r_status == 2)
								listTr += '<span class="label warning">已删除</span>';
							else if(ls[i].r_status == 3)
								listTr += '<span class="label notice">已发布</span>';
							
							listTr += '</td><td>' + ls[i].s_name + '</td>';
							listTr += '<td>' + getLocalTime(ls[i].r_dateline) + '</td><td>';
							if(ls[i].r_status == 1) 
								listTr += '<a href="javascript:;" class="btn" id="p_chastatus_2_' + ls[i].r_id + '">删除</a>';
							else if(ls[i].r_status == 2)
								listTr += '<a href="javascript:;" id="p_chastatus_1_' + ls[i].r_id + '" class="btn">设置为待发布</a>';
							listTr += '</td></tr>';
						}

						$('#listtable > tbody').html(listTr);
                        var pageRange = setPage((!page ? 1 : page), data['maxPage'], 2);
                        var pl = '<li class="prev ' + (page == 1 ? 'disabled' : '') + '" id="pagepre"><a href="javascript:;" id="p_page_prev">&larr; Previous</a></li>';
						if(pageRange[1] - data['maxPage'] >= 0 && data['maxPage'] > 5) pl += '<li><a href="javascript:;" id="p_page_1">1</li><li><a href="javascript:;">...</a></li>';
                        for(var i = pageRange[0]; i <= pageRange[1]; i++)
                        {
                            pl += '<li ' + (i == page ? 'class="active"' : '') + '><a href="javascript:;" id="p_page_' + i + '">' + i + '</a></li>';
                        }

                        if(data['maxPage'] > pageRange[1]) pl += '<li><a href="javascript:;">...</a></li><li><a href="javascript:;" id="p_page_' + data['maxPage'] + '">' + data['maxPage'] + '</li>';
						pl += '<li class="next ' + (page == data['maxPage'] ? 'disabled' : '') + '"><a href="javascript:;" id="p_page_next">Next &rarr;</a></li>';
                        $('#pagebar > ul').html(pl);
						return false;
					}
					else
						$('table[id="listtable"] > tbody > tr > td').html(data['msg']);
				});
			});
		}

		function showPackList(pName, pId, page)
		{
			$('#main').hide().fadeIn('slow').html(packList);
			$('#pname').html(pName);
			$('#pcurid').val(pId);
			getPackageList(pId, page);
			//取得服务器列表
		}

		function getLocalTime(nS)
		{
			if(!parseInt(nS)) return '';
			return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/时|分/g, ":").replace(/秒/g, "").replace(/日|星期.*\ /g, '');
		}

        //返回页码的开始和结束
        function setPage(page, max, sep)
        {
            if(!sep) sep = 2;
            var maxPage = sep*2+1;
            var prev = page - 2;
            var next = page + 2;
            var min = max - maxPage + 1;
            if((prev <= 0 && next >= max) || (prev > 0 && next >= max))
                return min > 0 ? [min, max] : [1, max];

            if(prev <= 0 && next < max)
                return min > 0 ? [1, maxPage] : [1, max];

            if(prev > 0 && next < max)
                return min > 0 ? [prev, next] : [prev, max];
        }
	};
});
