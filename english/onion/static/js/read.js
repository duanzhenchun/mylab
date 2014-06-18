var pagesize=2000;  // about 20kb data post, suitable for http transfer
var page_txt = ''
var keybusy = false; //global

function like_word(s) {
    return /^[\w\d]+$/i.test(s);
}

$(document).ready(function() {
var curpage = $("#curpage");
var cur_changed = false;
var totalpage = $("#totalpage"); 
var allnavis=[$("#navihome"),$("#naviend"),$("#naviup"),$("#navidown"),$("#navigoto")]

function repeat_word(w){
    $.ajax({
        type: "POST",
        url: '../word_repeat',
        data:{
                w:w,
            }, 
        success: function(data){
            $("#div_unknown_txt").html(data);
        }
    });
}
function selectText(){
    if(document.selection){
        return document.selection.createRange().text;// IE
    }else{
        return 	window.getSelection().toString(); //标准
    }
}
function change_word(w, unknown, refresh){
    $.ajax({
        type: "POST",
        url: '../word_mark',
        data:{ w:w, 
               unknown:unknown,
               txt:page_txt
            },
        success: function(data){
            if (refresh){
            var ph='<p class="p_txt">';
            txt = ph + data.lines.join('</p>'+ph)+ '</p>';
                $("#div_article").html(txt);
            }
        }
    });
}
$(".word_span ").live("click", function (){ // live response everytime
    w = $(this).text();
    yn = confirm("生词? "+w)
    change_word(w, yn, !yn);
});

$(".unknown_word").live("click", function (){ 
    w = $(this).text();
    if (confirm("重复? "+w)){
        repeat_word(w);
    }
});

$("#div_article").mouseup(function(){
    var s = selectText().trim();
    if (s.length>0 & like_word(s)) {
        if(confirm("生词? "+s)) {
            change_word(s, true, true);
        }
    } 
});
function navi(page){
    curpage.val(page);
    $("#fileinput").change();
};

function disable_navi(yn){
    keybusy = yn;
    for (var i in allnavis){
        if(yn){
            allnavis[i].attr('disabled','disabled');
        }else{
            allnavis[i].removeAttr('disabled');
        }
    }
};
$("#curpage").change(function(){ 
    cur_changed = true; 
    console.log('cur_changed:', cur_changed);
});

$("#navigoto").click(function(){
    if(!cur_changed){return;}
    var cur = parseInt(curpage.val());
    if(cur >= totalpage.val() || cur <=0 ){return;}
    navi(cur);
});
$("#naviup").click(function(){
    var cur = parseInt(curpage.val());
    if(cur <= 0){return;}
    navi(cur-1);
});
$("#navihome").click(function(){
    var cur = parseInt(curpage.val());
    if(cur <= 0){return;}
    navi(0);
});
$("#naviend").click(function(){
    var cur = parseInt(curpage.val());
    if (cur >= totalpage.val()) {return;}
    navi(totalpage.val());
});
$("#navidown").click(function(){
    var cur = parseInt(curpage.val());
    if(cur >= totalpage.val()){return;}
    navi(cur+1);
});

function checkSupport(){
    if (window.File && window.FileReader && window.FileList && window.Blob) {
      return true;
    } else {
      alert('The File APIs are not fully supported by your browser.');
      return false;
    }
}
// main interaction happens here
$("#fileinput").change(function(evt){
  if (!checkSupport())
    return; 
  var f = evt.target.files[0]; 
  if (!f) 
    return;

  var r = new FileReader();
  r.onload = function(e){
   // curpage.val(0);
    var contents = e.target.result;
    totalpage.val(Math.floor(contents.length/pagesize));
    var startpos = pagesize * curpage.val();
    var endpos = contents.indexOf("\n", pagesize + startpos);
    if (endpos<0){
      endpos = contents.length;
    }
    console.log('start:', startpos, 'endpos:', endpos);
    page_txt = contents.substr(startpos, endpos-startpos );
    
    disable_navi(true);
    $.ajax({
      type: "POST",
      url: 'read',
      data: {fname:f.name,"txt":page_txt},
      success: function(data){
        $("#div_article").html(data.article);
        cur_changed = false;
        console.log('cur_changed:', cur_changed);
      },
      complete: function(msg) {
          disable_navi(false);
      },
    });
  }
  r.readAsText(f);
});
});

$(document).keydown(function(event){  
   if (keybusy)
       return;
   event = event || window.event;
   if(event.keyCode==37){ 
       $( "#naviup" ).trigger( "click" );
   };
   if(event.keyCode==39){ 
       $( "#navidown" ).trigger( "click" );
   };
   if(event.keyCode==13){ 
       $( "#navigoto" ).trigger( "click" );
   };
});

