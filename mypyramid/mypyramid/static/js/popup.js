$(document).ready(function(){   
	var cs = $("#cs"),
		en = $("#en");
	$("#dialog-form").dialog({
		autoOpen: false,
		height: 300,
		width: 400,
		modal: true,
		buttons: {
			"Save": function(){
		        $.ajax({
                    type: "POST",
                    url: 'worddict',
                    data:{cs:$("#cs").val(),en:$("#en").val(),},
                    success: function(){
                        $("#fileinput").change();
                    }
                });
				$( this ).dialog( "close" );
//				window.location.reload();
			},
			"Delete": function() {
			    $.ajax({
                url: 'worddict/'+en.val(),
                type: 'DELETE',
                success: function(result) {
                    $("#fileinput").change();
                }
            });
                $( this ).dialog( "close" );
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
	});
	$("#div_txt").on('click', 'a.edit-word', function(){
        en.val($(this).text());
        cs.val($(this).attr('title'));
		$( "#dialog-form" ).dialog( "open" );
		return false;
	});
});
