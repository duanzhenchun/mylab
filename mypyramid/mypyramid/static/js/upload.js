$(function() {
    var maxtxt=1000000; 
    $("#enf_input").change(function(evt){
          var f = evt.target.files[0]; 
          if (!f) {
            return;
          }
          console.log(f.name);
          var r = new FileReader();
          r.onload = function(e){
            var contents = e.target.result;
            console.log('len of contents:', contents.length);
            if (contents.length > maxtxt){
                alert('max txt length reached!');
                return;
            }
            $.ajax({
              type: "POST",
              url: 'upload_enfile',
              data: {fname:f.name,"txt":contents},
              success: function(data){
                ;  
              }
            });
          }
          r.readAsText(f);
        });
    });
});
