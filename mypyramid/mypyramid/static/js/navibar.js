function navipage(index){
    var url = this.location.href.split('?')[0]
    this.location = url + '?page=' + index;
}
function navipageup(up){
    var qs = this.location.search.substr(1).split('&')[0];
    var cur = parseInt(qs.split('=')[1]);
    cur += (up == true ? 1:-1);
//    if (up == true ){alert( 'true');}
//    else {alert('false');}
    navipage(cur);
}
function navipageto(){
    navipage($("#curpage").val());
}

