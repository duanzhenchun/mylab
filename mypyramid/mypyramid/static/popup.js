$(function() {
	var cs = $("#cs"),
		en = $("#en");
	$( "#dialog-form" ).dialog({
		autoOpen: false,
		height: 300,
		width: 400,
		modal: true,
		buttons: {
			"Save": function() {
		        $.post("../worddict",
	            {cs:$("#cs").val(),en:$("#en").val(),}
                );
				$( this ).dialog( "close" );
				window.location.reload();
			},
			"Delete": function() {
			    $.ajax({
                url: '../worddict/'+en.val(),
                type: 'DELETE',
                success: function(result) {
                    window.location.reload();
                }
            });
                $( this ).dialog( "close" );
			},
			"Add": function() {
			    en.val("");
			    cs.val("");
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
	});
    $("a.edit-word").click(function(){
        en.val($(this).text());
        cs.val($(this).attr('title'));
		$( "#dialog-form" ).dialog( "open" );
		return false;
	});
});
