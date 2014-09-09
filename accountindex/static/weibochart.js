function pie_chart(task, type, renderid, alldata){
    var chart;
    var datalength = alldata.length
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: renderid,
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            exporting:{
                buttons: {  
                printButton: {enabled:false,},
                exportButton:{enabled:false, align:'right', type:'image/jpg'}
                },
                //url:'/download/',
                enabled:false,
            },
            title: {
                //text: task+ type +'比例'
                text:' '
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage}%</b>',
                percentageDecimals: 1
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false,
                    },
                    showInLegend: true
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -30,
                y: 65 + (4-datalength)*10,
                //floating: true,
                borderWidth: 1,
                backgroundColor: '#FFFFFF',
                shadow: false,
                itemMarginTop:5
            },
            series: [{
                type: 'pie',
                name: type +'比例',
                data: alldata
            }]
        });
    });
    return chart;
};

function bar_chart(task, type, renderid, xdata, ydata){
    var chart;
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: renderid,
                type: 'bar',

                reflow:'500',
                zoomType:'x',
            },
            exporting:{
                buttons: {  
                printButton: {enabled:false,},
                exportButton:{enabled:false, align:'right', type:'image/jpg'}
                },
                //url:'/download/',
                enabled:false,
            },
            title: {
                //text: task + type +'排名' 
                text:' '
            },
            xAxis: {
                categories: xdata.slice(0, 10),
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: null,
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                }
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.x +': '+ this.y;
                }
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            legend: {
                enabled: false,
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -50,
                y: 200,
                floating: true,
                borderWidth: 1,
                backgroundColor: '#FFFFFF',
                shadow: true
            },
            credits: {
                enabled: false
            },
            series: [{
                name: type,
                data: ydata.slice(0, 10)
            }]
        });
    });
    return chart;
};

function date_chart(task, renderid, startdate, alldate){
    var chart;
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: renderid,
                zoomType: 'x',
                spacingRight: 20
            },
            exporting:{
                buttons: {  
                printButton: {enabled:false,},
                exportButton:{enabled:false, align:'right', type:'image/jpg'}
                },
                //url:'/download/',
                enabled:false,
            },
            title: {
                //text: task + '时间流线图' 
                text: ' '
            },
            xAxis: {
                type: 'datetime',
                //maxZoom: 18 * 24 * 3600000, // fourteen days
                title: {
                    text: null
                }
            },
            yAxis: {
                title: {
                    text: null
                },
                showFirstLabel: false
            },
            tooltip: {
                shared: true
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, 'rgba(2,0,0,0)']
                        ]
                    },
                    lineWidth: 1,
                    marker: {
                        enabled: false,
                        states: {
                            hover: {
                                enabled: true,
                                radius: 5
                            }
                        }
                    },
                    shadow: false,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            series: [{
                type: 'area',
                name: task + '数',
                //设置间隔时间
                pointInterval: 3600 * 1000,
                pointStart: startdate,
                data: alldate
            }, 
            ]
        });
    });
    return chart
};

function cloud_chart(cloudid, cswords){

//对数据进行排序 出现次数多的在前面 少的在后面
cswords.sort(function(x,y){return x.value - y.value;}).reverse();
try{
var fill = d3.scale.category20b();}
catch(e){return null;}
var w = 1200,
    h = 700
    //最多显示词组数量
    max = 500;

var words = [],
    max ,
    scale = 1,
    complete = 0,
    keyword = "",
    tags,
    fontSize,
    maxLength = 30,
    statusText = d3.select("#status");

var layout = d3.layout.cloud()
    .timeInterval(10)
    .size([w, h])
    .fontSize(function(d) { return fontSize(+d.value); })
    .text(function(d) { return d.key; })
    .on("word", progress)
    .on("end", draw);

var svg = d3.select("#"+cloudid).append("svg")
    .attr("width", w)
    .attr("height", h);

var background = svg.append("g"),
    vis = svg.append("g")
    .attr("transform", "translate(" + [w >> 1, h >> 1] + ")");

function parseText(text) {
  tags = text
  generate();
}

function generate() {
  layout
    .font("Impact")
    .spiral("archimedean");
    //.fontSize(function(d) { return d.value; });
  fontSize = d3.scale["log"]().range([20, 80]);
  //取最大词组数量和最小的 算出合适的大小
  if (tags.length) fontSize.domain([+tags[tags.length - 1].value || 1, +tags[0].value]);
  complete = 0;
  statusText.style("display", null);
  words = [];
  layout.stop().words(tags.slice(0, max = Math.min(tags.length, +max))).start();
}

function progress(d) {
  statusText.text(++complete + "/" + max);
}

function draw(data, bounds) {
  statusText.style("display", "none");
  scale = bounds ? Math.min(
      w / Math.abs(bounds[1].x - w / 2),
      w / Math.abs(bounds[0].x - w / 2),
      h / Math.abs(bounds[1].y - h / 2),
      h / Math.abs(bounds[0].y - h / 2)) / 2 : 1;
  words = data;
  var text = vis.selectAll("text")
      .data(words, function(d) { return d.text.toLowerCase(); });
  text.transition()
      .duration(1000)
      .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
      .style("font-size", function(d) { return d.size + "px"; });
  text.enter().append("text")
      .attr("text-anchor", "middle")
      .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
      .style("font-size", function(d) { return d.size + "px"; })
      .on("click", function(d) {
        load(d.text, cswords);
      })
      .style("opacity", 1e-6)
    .transition()
      .duration(1000)
      .style("opacity", 1);
  text.style("font-family", function(d) { return d.font; })
   //指定字体颜色
      .style("fill", function(d) { return fill(d.text.toLowerCase()); })
      .text(function(d) { return d.text; });
  var exitGroup = background.append("g")
      .attr("transform", vis.attr("transform"));
  var exitGroupNode = exitGroup.node();
  text.exit().each(function() {
    exitGroupNode.appendChild(this);
  });
  exitGroup.transition()
      .duration(1000)
      .style("opacity", 1e-6)
      .remove();
  vis.transition()
      .delay(1000)
      .duration(750)
      .attr("transform", "translate(" + [w >> 1, h >> 1] + ")scale(" + scale + ")");
}

function load(d, f) {
  f = f || fetcher;
  fetcher = f;
  parseText(fetcher);
}


(function() {
  var r = 40.5,
      px = 35,
      py = 20;

  var angles = d3.select("#angles").append("svg")
      .attr("width", 2 * (r + px))
      .attr("height", r + 1.5 * py)
    .append("g")
      .attr("transform", "translate(" + [r + px, r + py] +")");

  angles.append("path")
      .style("fill", "none")
      .attr("d", ["M", -r, 0, "A", r, r, 0, 0, 1, r, 0].join(" "));

  angles.append("line")
      .attr("x1", -r - 7)
      .attr("x2", r + 7);

  angles.append("line")
      .attr("y2", -r - 7);

  angles.selectAll("text")
      .data([-90, 0, 90])
    .enter().append("text")
      .attr("dy", function(d, i) { return i === 1 ? null : ".3em"; })
      .attr("text-anchor", function(d, i) { return ["end", "middle", "start"][i]; })
      .attr("transform", function(d) {
        d += 90;
        return "rotate(" + d + ")translate(" + -(r + 10) + ")rotate(" + -d + ")translate(2)";
      })
      .text(function(d) { return d + "°"; });

  var radians = Math.PI / 180,
      from,
      to,
      count,
      scale = d3.scale.linear(),
      arc = d3.svg.arc()
        .innerRadius(0)
        .outerRadius(r);

  getAngles();
  
  function getAngles() {
  //设置词组显示的角度
    count = + 2;
    from = Math.max(-90, Math.min(90, + -90));
    to = Math.max(-90, Math.min(90, + 0));
    update();
  }

  function update() {
    scale.domain([0, count - 1]).range([from, to]);
    var step = (to - from) / count;

    var path = angles.selectAll("path.angle")
        .data([{startAngle: from * radians, endAngle: to * radians}]);
    path.enter().insert("path", "circle")
        .attr("class", "angle")
        .style("fill", "#fc0");
    path.attr("d", arc);

    var line = angles.selectAll("line.angle")
        .data(d3.range(count).map(scale));
    line.enter().append("line")
        .attr("class", "angle");
    line.exit().remove();
    line.attr("transform", function(d) { return "rotate(" + (90 + d) + ")"; })
        .attr("x2", function(d, i) { return !i || i === count - 1 ? -r - 5 : -r; });

    var drag = angles.selectAll("path.drag")
        .data([from, to]);
    drag.enter().append("path")
        .attr("class", "drag")
        .attr("d", "M-9.5,0L-3,3.5L-3,-3.5Z")
        .call(d3.behavior.drag()
          .on("drag", function(d, i) {
            d = (i ? to : from) + 90;
            var start = [-r * Math.cos(d * radians), -r * Math.sin(d * radians)],
                m = [d3.event.x, d3.event.y],
                delta = ~~(Math.atan2(cross(start, m), dot(start, m)) / radians);
            d = Math.max(-90, Math.min(90, d + delta - 90)); // remove this for 360°
            delta = to - from;
            if (i) {
              to = d;
              if (delta > 360) from += delta - 360;
              else if (delta < 0) from = to;
            } else {
              from = d;
              if (delta > 360) to += 360 - delta;
              else if (delta < 0) to = from;
            }
            update();
          })
          .on("dragend", generate));
    drag.attr("transform", function(d) { return "rotate(" + (d + 90) + ")translate(-" + r + ")"; });
    layout.rotate(function(d) {
     return scale(1);
    //if (getByteLen(d.key)<9) return scale(~~(Math.random() * count));
    //else return scale(1);
    });
    d3.select("#angle-count").property("value", count);
    d3.select("#angle-from").property("value", from);
    d3.select("#angle-to").property("value", to);
  }
  
  function getByteLen(val) {
            var len = 0;
            for (var i = 0; i < val.length; i++) {
               var length = val.charCodeAt(i);
               if(length>=0&&length<=128)
                {len += 1;}
                else
                { len += 2;}}
                return len;}
        
  function cross(a, b) { return a[0] * b[1] - a[1] * b[0]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1]; }
  
  //初始化显示
  load("",   cswords);
})();

}

Date.prototype.format = function(format){ 
var o = { 
"M+" : this.getUTCMonth()+1, //month 
"d+" : this.getUTCDate(), //day 
"h+" : this.getUTCHours(), //hour 
"m+" : this.getUTCMinutes(), //minute 
"s+" : this.getUTCSeconds(), //second 
"q+" : Math.floor((this.getUTCMonth()+3)/3), //quarter 
"S" : this.getUTCMilliseconds() //millisecond 
} 

if(/(y+)/.test(format)) { 
format = format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length)); 
} 

for(var k in o) { 
if(new RegExp("("+ k +")").test(format)) { 
format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length)); 
} 
} 
return format; 
} 
/*
//使用方法 
var now = new Date(); 
var nowStr = now.format("yyyy-MM-dd hh:mm:ss"); 
//使用方法2: 
var testDate = new Date(); 
var testStr = testDate.format("YYYY年MM月dd日hh小时mm分ss秒"); 
alert(testStr); 
//示例： 
alert(new Date().Format("yyyy年MM月dd日")); 
alert(new Date().Format("MM/dd/yyyy")); 
alert(new Date().Format("yyyyMMdd")); 
alert(new Date().Format("yyyy-MM-dd hh:mm:ss"));
*/