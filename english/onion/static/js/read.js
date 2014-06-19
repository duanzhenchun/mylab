var pagesize=2000;  // about 20kb data post, suitable for http transfer
var page_plus = 20;
var max_wait = 3600*24*7;

var g_fname = 'sample';
var g_contents = 'Sample:\nAlthough born to the ease of plantation life, waited on hand and foot since infancy, the faces of the three on the porch were neither slack nor soft. They had the vigor and alertness of country people who have spent all their lives in the open and troubled their heads very little with dull things in books. Life in the north Georgia county of Clayton was still new and, according to the standards of Augusta, Savannah and Charleston, a little crude. The more sedate and older sections of the South looked down their noses at the up-country Georgians, but here in north Georgia, a lack of the niceties of classical education carried no shame, provided a man was smart in the things that mattered. And raising good cotton, riding well, shooting straight, dancing lightly, squiring the ladies with elegance and carrying ones liquor like a gentleman were the things that mattered.\nIn these accomplishments the twins excelled, and they were equally outstanding in their notorious inability to learn anything contained between the covers of books. Their family had more money, more horses, more slaves than any one else in the County, but the boys had less grammar than most of their poor Cracker neighbors.\nIt was for this precise reason that Stuart and Brent were idling on the porch of Tara this April afternoon. They had just been expelled from the University of Georgia, the fourth university that had thrown them out in two years; and their older brothers, Tom and Boyd, had come home with them, because they refused to remain at an institution where the twins were not welcome. Stuart and Brent considered their latest expulsion a fine joke, and Scarlett, who had not willingly opened a book since leaving the Fayetteville Female Academy\n'
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
    if (!w) {w=''}
    $.ajax({
        type: "POST",
        url: '../word_repeat',
        data:{w:w,
            }, 
        success: function(data){
            $("#div_unknown_txt").html(data.unknown);
            var wait = parseInt(data.wait);
            console.log('time2wait:', wait);
            if (wait>0){
                wait = Math.min(wait, max_wait);
                setTimeout(repeat_word, wait*1000);
            }
        }
    });
}

// initial require
read_article();
repeat_word('');

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
               txt: get_pagetxt(),
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
$(".word_span ").live("click", function (evt){ // live response everytime
//    evt.preventDefault();
    w = $(this).text();
    yn = confirm("生词? "+w)
    change_word(w, yn, !yn);
});

$(".unknown_word").live("click", function (evt){ 
    w = $(this).text();
    if (confirm("重复? "+w)){
        repeat_word(w);
    }
});
function add_newword(){
    var s = selectText().trim();
    if (s.length>0 & like_word(s)) {
        if(confirm("生词? "+s)) {
            change_word(s, true, true);
        }
    } 
}
$("#div_article").mouseup(function(evt){
    add_newword();
});
$("#div_article").live( "touchend", function(evt){
    add_newword();
});
function navi(page){
    curpage.val(page);
    read_article();
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

function checkSupport(){    //http://caniuse.com/filereader
    if (window.File && window.FileReader && window.FileList && window.Blob) {
      return true;
    } else {
      alert('The File APIs are not fully supported by your browser.');
      return false;
    }
}
function read_article(){
    disable_navi(true);
    $.ajax({
      type: "POST",
      url: 'read',
      data: {fname:g_fname,
             txt: get_pagetxt()
      },
      success: function(data){
        document.title = data.title;
        $("#div_article").html(data.article);
        cur_changed = false;
      },
      complete: function(msg){
          disable_navi(false);
      },
    });
}
// main interaction happens here
$("#fileinput").change(function(evt){
  if (!checkSupport())return; 
  var f = evt.target.files[0]; 
  if (!f) return;

  var r = new FileReader();
  r.onload = function(evt){   //file loaded successfuly
    g_fname=f.name;
    g_contents = evt.target.result;
    curpage.val(0);
    read_article();
  }
  var label = $("#file_encoding option:selected").text();
  r.readAsText(f, label);
});

$("#file_encoding").change(function(evt){
    $("#fileinput").change();
});

function get_pagetxt(){
    totalpage.val(Math.floor(g_contents.length/pagesize));
    var start0 = pagesize * curpage.val();
    var end = g_contents.indexOf("\n", start0 + pagesize);
    var start = start0;
    if(curpage.val()>0){
        start = g_contents.indexOf("\n", start0); 
        if (start<0){  //not found
            start=start0+page_plus;
        }else{
            start+=1;
        }
    }
    if (end<0){  //not found
      end = start0 + pagesize + page_plus;
    }
    console.log('start:', start, 'end:', end);
    return g_contents.substr(start, end-start );
} 
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
