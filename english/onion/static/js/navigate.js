$(document).ready(function() {
	var page_count = $('#pagecount').val();
	function isNumber(oNum) {
		if (!oNum)
			return false;
		var strP = /^\d+(\.\d+)?$/;
		if (!strP.test(oNum))
			return false;
		try {
			if (parseFloat(oNum) != oNum)
				return false;
		} catch (ex) {
			return false;
		}
		return true;
	}
	$('a#Goto').live('click',function(){
		var page_i = $('#page_i').val();
		if (!isNumber(page_i)) {
			alert("请输入正确数字");
        } else if ( $('#curpage').text() == page_i ){
            return;
		} else if (parseInt(page_i) > parseInt(page_count)
				|| parseInt(page_i) < 1) {
			alert("页数超出范围");
		} else {
			window.location = window.location.pathname + '?&page=' + page_i;
		}
	});
});
