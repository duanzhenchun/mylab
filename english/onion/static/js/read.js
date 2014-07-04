var pagesize=2000;  // about 20kb data post, suitable for http transfer
var page_plus = 20;
var max_wait = 3600*24*7;

var g_fname = 'sample';
var keybusy = false; //global

var g_contents = 'Sample:\nAlthough born to the ease of plantation life, waited on hand and foot since infancy, the faces of the three on the porch were neither slack nor soft. They had the vigor and alertness of country people who have spent all their lives in the open and troubled their heads very little with dull things in books. Life in the north Georgia county of Clayton was still new and, according to the standards of Augusta, Savannah and Charleston, a little crude. The more sedate and older sections of the South looked down their noses at the up-country Georgians, but here in north Georgia, a lack of the niceties of classical education carried no shame, provided a man was smart in the things that mattered. And raising good cotton, riding well, shooting straight, dancing lightly, squiring the ladies with elegance and carrying ones liquor like a gentleman were the things that mattered.\nIn these accomplishments the twins excelled, and they were equally outstanding in their notorious inability to learn anything contained between the covers of books. Their family had more money, more horses, more slaves than any one else in the County, but the boys had less grammar than most of their poor Cracker neighbors.\nIt was for this precise reason that Stuart and Brent were idling on the porch of Tara this April afternoon. They had just been expelled from the University of Georgia, the fourth university that had thrown them out in two years; and their older brothers, Tom and Boyd, had come home with them, because they refused to remain at an institution where the twins were not welcome. Stuart and Brent considered their latest expulsion a fine joke, and Scarlett, who had not willingly opened a book since leaving the Fayetteville Female Academy\n'

function like_word(s) {
    return /^[\w\d]+$/i.test(s);
}
function time_str(t){
    var m = Math.floor(t/60);
    var str ='';
    if (m>0){
        var h = Math.floor(m/60);
        m %= 60;
        if (h>0){
            var d = Math.floor(h/24);
            h %= 24;
            if(d>0){
                str+=d + ' days, ';
            }
            str += h + ' hours, ';
        }
    }
    str += m + ' mins'
    return str;
}

$(document).ready(function() {

var curpage = $("#curpage");
var cur_changed = false;
var totalpage = $("#totalpage"); 
var allnavis=[$("#navihome"),$("#naviend"),$("#naviup"),$("#navidown"),$("#navigoto")]
$("#search").prop('disabled', true);
var tshow=NaN;
var tinfo = NaN;
var lastword = '';

function repeat_word(w,yn){
    if (!w) {w=''}
    $.ajax({
        type: "POST",
        url: '../word_repeat',
        data:{w:w,yn:yn}, 
        success: function(data){
            $("#div_2study").html(data.unknown);
            var wait = parseInt(data.wait);
            wait = Math.ceil(wait/60)*60;
            if (wait>0){
                wait = Math.min(wait, max_wait);
                clearTimeout(tshow);
                tshow = setTimeout(repeat_word, wait*1000);
                $("#time2show").text(time_str(wait)+' to repeat');
            }
            if (wait>60){
                clearTimeout(tinfo);
                tinfo = setTimeout(function(){
                    $("#time2show").text('');    
                }, 59000);
            }
        }
    });
}

function rescue_word(w, yn){
    if (!w) {w=''}
    $.ajax({
        type: "POST",
        url: '../word_rescue',
        data:{w:w,yn:yn}, 
        success: function(data){
            $("#div_2study").html(data.forgotten);
        }
    });
}

// initial require
read_article();
repeat_word();

function getSelectedTextWithin(el) {
    var selectedText = "";
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection(), rangeCount;
        if ( (rangeCount = sel.rangeCount) > 0 ) {
            var range = document.createRange();
            for (var i = 0, selRange; i < rangeCount; ++i) {
                range.selectNodeContents(el);
                selRange = sel.getRangeAt(i);
                if (selRange.compareBoundaryPoints(range.START_TO_END, range) == 1 && selRange.compareBoundaryPoints(range.END_TO_START, range) == -1) {
                    if (selRange.compareBoundaryPoints(range.START_TO_START, range) == 1) {
                        range.setStart(selRange.startContainer, selRange.startOffset);
                    }
                    if (selRange.compareBoundaryPoints(range.END_TO_END, range) == -1) {
                        range.setEnd(selRange.endContainer, selRange.endOffset);
                    }
                    selectedText += range.toString();
                }
            }
        }
    } else if (typeof document.selection != "undefined" && document.selection.type == "Text") {
        var selTextRange = document.selection.createRange();
        var textRange = selTextRange.duplicate();
        textRange.moveToElementText(el);
        if (selTextRange.compareEndPoints("EndToStart", textRange) == 1 && selTextRange.compareEndPoints("StartToEnd", textRange) == -1) {
            if (selTextRange.compareEndPoints("StartToStart", textRange) == 1) {
                textRange.setEndPoint("StartToStart", selTextRange);
            }
            if (selTextRange.compareEndPoints("EndToEnd", textRange) == -1) {
                textRange.setEndPoint("EndToEnd", selTextRange);
            }
            selectedText = textRange.text;
        }
    }
    return selectedText;
}

function change_word(w, unknown, refresh){
    $.ajax({
        type: "POST",
        url: '../word_change',
        data:{ w:w, 
               unknown:unknown,
               txt: get_pagetxt(), //page txt should be updated after unknown words changed
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
$(".word_span").live("click", function (evt){ // live response everytime
    w = $(this).text();
    if(evt.ctrlKey) {
        if (w == lastword)return;   //avoid frequent request
        lastword = w;
        var yn = true;
    }else{
        var yn = confirm("生词? "+w)
        if (yn){
            if (w == lastword)return;
            lastword = w;
        }
    }
    change_word(w, yn, !yn);
});

$(".unknown_word").live("click", function (evt){ 
    w = $(this).text();
    if (evt.ctrlKey){
        var yn = true;
    }else{
        var yn = confirm("repeat? "+w);
    }
    repeat_word(w, yn);
});

$(".forgotten_word").live("click", function (evt){ 
    w = $(this).text();
    if (evt.ctrlKey){
        var yn = true;
    }else{
        var yn = confirm("rescue? "+w);
    }
    rescue_word(w, yn);
});

$("#rescue_word").click(function(){
    var shows = ['Rescue my words~','wait to repeat'];
    if ($(this).val() == shows[0]){
        $(this).val(shows[1]);
        rescue_word('', true);
    }else{
        $(this).val(shows[0]);
        repeat_word();
    }
});

function add_newword(){
    var s =getSelectedTextWithin(document.getElementById("div_article")).trim();
    if (s.length>1 & like_word(s)) {
        if(confirm("生词? "+s)) {
            change_word(s, true, true);
        }
    } 
}
$("#div_article").mouseup(function(evt){
    add_newword();
});
$("#div_article").live("touchend", function(evt){
    add_newword();
});
function navi(page){
    curpage.val(page);
    read_article(page);
};

function disable_navi(yn){
    keybusy = yn;
    for (var i in allnavis){
        allnavis[i].prop('disabled', yn);
    }
    $('#search').prop('disabled', yn);
};
$("#curpage").change(function(){ 
    cur_changed = true; 
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
function read_article(curpage){
    if (!curpage) curpage=0;
    disable_navi(true);
    $.ajax({
      type: "POST",
      url: 'read',
      data: {fname:g_fname,
             curpage:curpage,
             txt: get_pagetxt()
      },
      success: function(data){
        document.title = data.title;
        $("#div_article").html(data.article);
        $("#middle").animate({ scrollTop: 0 }, "fast");
        cur_changed = false;
      },
      complete: function(msg){
          disable_navi(false);
      },
    });
}

function lastpage_article(){
    var last = 0;
    $.ajax({
      type:"GET",
      url: 'lastpage',
      data:{fname:g_fname},
      success: function(data){
        last = parseInt(data.last);
        last = Math.min(last, totalpage.val())
        curpage.val(last);
        read_article()
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
    totalpage.val(Math.floor(g_contents.length/pagesize));
    lastpage_article();
  }
  var label = $("#file_encoding option:selected").text();
  r.readAsText(f, label);
});

$("#file_encoding").change(function(evt){
    $("#fileinput").change();
});

function get_pagetxt(){
    var res = page_start();
    var start0 = res[0];
    var start = res[1];
    var end = g_contents.indexOf("\n", start0 + pagesize);
    if (end<0){  //not found
      end = start0 + pagesize + page_plus;
    }
    //console.log('start:', start, 'end:', end);
    return g_contents.substr(start, end-start );
} 
function page_start(){
    var start0 = pagesize * curpage.val();
    var start = start0;
    if(curpage.val()>0){
        start = g_contents.indexOf("\n", start0); 
        if (start<0){  //not found
            start = start0 + page_plus;
        }else{
            start +=1;
        }
    }
    return [start0, start];
}
$("#search").click(function(){
    var s = $("#search_txt").val();
    if (s.length<1){return;}
    var start = page_start()[1] + pagesize;
    var pos = g_contents.indexOf(s, start);
    if (pos<0){return;}
    var pos_page = Math.floor(pos/pagesize);
    navi(pos_page);
});
});

$(document).keydown(function(evt){  
   if (keybusy)
       return;
   evt = evt || window.evt;
   if(evt.keyCode==37){ 
       $( "#naviup" ).trigger( "click" );
   };
   if(evt.keyCode==39){ 
       $( "#navidown" ).trigger( "click" );
   };
   if(evt.keyCode==13){ 
       $( "#navigoto" ).trigger( "click" );
   };
});
