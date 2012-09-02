$(function() {
    
var bar = $('.bar');
var percent = $('.percent');
var status = $('#status');
   
$('#uploadform').ajaxForm({
    beforeSend: function() {
        status.empty();
        var percentVal = '0%';
        bar.width(percentVal)
        percent.html(percentVal);
		$("#text_div").html('waiting for response...');
    },
    uploadProgress: function(event, position, total, percentComplete) {
        var percentVal = percentComplete + '%';
        bar.width(percentVal)
        percent.html(percentVal);
		//console.log(percentVal, position, total);
    },
//	complete: function(xhr) {
//	},
	success: function( data) { 
	    $("#text_div").html(data);
    } 
}); 

});  
