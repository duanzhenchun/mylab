$(document).ready(function(){       //$(function() {
    var pagesize=5000;  // about 20kb data post, suitable for http transfer
    var curpage = $("#curpage");
    var totalpage = $("#totalpage"); 
    
    function navi(page){
        curpage.val(page);
        $("#fileinput").change();
    };
    $("#navigoto").click(function(){
        var cur = parseInt(curpage.val());
        if(cur >= totalpage.val() || cur <0 ){return;}
        navi(cur);
    });
    $("#navidown").click(function(){
        var cur = parseInt(curpage.val());
        if(cur >= totalpage.val()){return;}
        navi(cur+1);
    });
    $("#naviup").click(function(){
        var cur = parseInt(curpage.val());
        if(cur <= 0){return;}
        navi(cur -1);
    });
    $("#navihome").click(function(){
        navi(0);
    });
    $("#naviend").click(function(){
        navi(totalpage.val());
    });
    function checkSupport(){
        if (window.File && window.FileReader && window.FileList && window.Blob) {
          return true;
        } else {
          alert('The File APIs are not fully supported by your browser.');
          return false;
        }
    }
    $("#fileinput").change(function(evt){
      if (!checkSupport()) {return; }
      var f = evt.target.files[0]; 
      if (!f) {return;}
      console.log(f.name);
      var r = new FileReader();
      r.onload = function(e){
        $("#filename").val(f.name);
        var contents = e.target.result;
        totalpage.val(Math.floor(contents.length/pagesize));
        var startpos = pagesize * curpage.val();
        var endpos = contents.indexOf("\n", pagesize + startpos);
        if (endpos<0){
          endpos = contents.length;
        }
        console.log('start:', startpos, 'endpos:', endpos);
        var txt = contents.substr(startpos, endpos-startpos );
        console.log('len of txt:', txt.length);
        $.ajax({
          type: "POST",
          url: 'reader',
          data: {fname:f.name,"txt":txt},
          success: function(data){
            $("#text_div").html(data);
          }
        });
      }
      r.readAsText(f);
    });
});
