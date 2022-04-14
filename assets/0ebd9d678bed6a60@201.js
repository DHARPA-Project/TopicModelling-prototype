// https://observablehq.com/@dharpa-project/timestamped-corpus@201
import define1 from "./a2e58f97fd5e8d7c@674.js";
import define2 from "./8d271c22db968ab0@160.js";

function _1(md){return(
md`# timestamped-corpus`
)}

function _2(md){return(
md`Visualization prototype created by:<br/>
[Dr. Lorella Viola](https://www.c2dh.uni.lu/people/lorella-viola)<br/>
[Mariella De Crouy Chanel](https://www.c2dh.uni.lu/people/mariella-de-crouy-chanel)`
)}

function _colorScheme(form,html){return(
form(html`<form>
  <div class='form-header'>Select color scheme:<div>
  <label><input name="value" type="radio" value="blue" checked>Blue</label>
  <label><input name="value" type="radio" value="green">Green</label>
  <label><input name="value" type="radio" value="grey">Grey</label>
  <label><input name="value" type="radio" value="orange">Orange</label>
  <label><input name="value" type="radio" value="purple">Purple</label>
  <label><input name="value" type="radio" value="red">Red</label>
</form>`)
)}

function _timeSpan(form,html){return(
form(html`<form>
  <div class='form-header'>Select table:<div>
  <label><input name="period" type="radio" value="day">Day</label>
  <label><input name="period" type="radio" value="month" checked>Month</label>
  <label><input name="period" type="radio" value="year">Year</label>
</form>`)
)}

function _scaleTypeTest(form,html){return(
form(html`<form>
  <div class='form-header'>Select how to scale values<div>
  <label><input name="scale" type="radio" value="color" checked>Color</label>
  <label><input name="scale" type="radio" value="height">Height</label>
</form>`)
)}

function _axisLabelTest(form,html){return(
form(html`<form>
  <div class='form-header'>Select the right axis label interval for your data<div>
  <label><input name="axis" type="radio" value="5-year" checked>5 year</label>
  <label><input name="axis" type="radio" value="year">year</label>
  <label><input name="axis" type="radio" value="month">month</label>
  <label><input name="axis" type="radio" value="day">day</label>
</form>`)
)}

function _chart(d3,width,height,margin,x2,interval,publications,data,scaleType,yScale,dateFormat,colorScale,color2,dateFormatLabel,$0,addEventListener)
{
  
  const svg = d3
    .create("svg")
    .attr("viewBox", [0, 0, width, height])
    .style("font-family", "sans-serif");
  
  const xAxis = svg
    .append("g")
    .attr("class","axis")
    .attr("transform", `translate(0,${height - margin.bottom/2})`)
    .attr("class", "grid")
    .call(d3.axisBottom(x2).ticks(interval).tickSize(-(height-margin.top-15)).tickSizeOuter(0))

  const axisLabel = svg
    .append("g")
    .attr("transform", `translate(0, ${height / 2})rotate(-90)`)
    .append('text')
    .style("font-size", "12px")
    .style("text-anchor", "middle");
  
  publications.map((pub,idx) => {
    
   const filter = data.filter(d => d.publication_name == pub)
   const bars = svg.append('g')
    
    bars.selectAll('rect')
      .data(filter)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr("x", (d) => x2(new Date(d.date)))
      .attr("y", (d) => scaleType == "height" ?  margin.top + 25 * idx + yScale(d.count) + 5 : margin.top + 25 * idx +5 )
      .attr("height", (d) => scaleType == "height" ?  yScale(0) - yScale(d.count) : 20)
      .attr("width", (width-margin.left-margin.right)/(x2.ticks(dateFormat).length-1))
      .attr('fill', (d) => {
          if (scaleType == "color") {
               return d.count > 0 ? colorScale(d.count) : "rgb(255,255,255)"
            }
          else { return color2}
    })
      .attr('opacity', 1);
    
    const texts = svg.append('g')
      texts.append('text')
      .attr("x", 5)
      .attr("y", margin.top + 25*idx + 23)
      .style('font-family', 'Palanquin')
      .style('font-size', "10px")
      .text(pub)
    
    const gridlines = svg.append('g')
      gridlines.attr("class","grid")
      gridlines.append('line')
      .attr("x0", 5) 
      .attr("x1", width - margin.right)
      .attr("y1", margin.top + 25*idx + 25)
      .attr("y2", margin.top + 25*idx + 25)
  
  }) 
  
  const lines = svg.append('g')
    
   // semi opaque rect for tooltip info visibility 
   lines.append('rect')
      .attr("class", "rect")
      .attr("y",margin.top )
      .attr("width", 30)
      .attr("height", height)
      .style("fill", 'rgba(255,255,255,.6)')
    
    // tooltip line
    lines.append("line")
      .attr("class", "line")
      .attr("stroke", 'rgba(0,0,0,.5)')
      .attr("stroke-dasharray", .5)
      .attr("y1", margin.top )
      .attr("y2", height);
  
    const line = svg.selectAll(".line");
  
  const temp = []
  temp.length = publications.length
  
  const texts = svg.append('g')
    texts.selectAll('text')
      .data(temp)
      .enter()
      .append('text')
      .attr('class', 'value-labels')
      .attr('id', (d,i) => `label-${i}`)
      .attr('x', 10)
      .attr('y', (d,i) => 25*i + 21 + margin.top )
      .style('font-family', 'Palanquin')
      .style('font-size', '11px')
      .style('fill', 'black')
      .text((d)=>d)
  
   const tooltipDate = svg.append('text')
      .attr('id', 'date-label')
      .attr('y', margin.top-10)
      .style('font-family', 'Palanquin')
      .style('font-size', '12px')
      .style('fill', 'black')
    
   let clientX = - margin.left
 
  
  function mousemoved(event) {   
    
    clientX = event.clientX;
    
    if (clientX>margin.left -3) {   
      
      line.attr("x1", clientX)
      line.attr("x2", clientX)
      d3.selectAll(".rect").attr("x", clientX)
      
      const date = x2.invert(clientX)
      
      d3.select('#date-label')
        .attr('x', clientX - 20)
        .text(dateFormatLabel(date))
        .on("click", dateClicked)
      
      function dateClicked() {
        const formatYear = d3.timeFormat("%Y")
        const month = date.getMonth() + 1
        const formatDay = d3.timeFormat("%d")
        $0.value = [+formatYear(date),month,+formatDay(date)]
      }
     
      
      let result = []

      publications.map((pub,idx) => {
        
        const corpus_filt = data.filter(d => (d.publication_name == pub && dateFormatLabel(new Date(d.date)) == dateFormatLabel(date)))     
        
        corpus_filt.length > 0 ? result.push(+corpus_filt[0].count) : result.push(0)
        })
      
      d3.selectAll(`.value-labels`).attr('x',clientX + 3).text((d,i) => result[i])

      }
    

    }
  
    addEventListener("mousemove", mousemoved);    
    requestAnimationFrame(() => mousemoved({clientX, clientY: 0}));
        
  
  return svg.node()

}


function _Table(dateInfo,timeSelected,Inputs,d3,data,html)
{
  if (dateInfo !== null) {
    switch(timeSelected) {
      case 'year':
        return Inputs.table(d3.filter(data, d => new Date(d.date).getFullYear() == dateInfo[0]))
      case 'month':
        return Inputs.table(d3.filter(data, d => (new Date(d.date).getFullYear() == dateInfo[0])&&(new Date(d.date).getMonth()+1 == dateInfo[1]) ))
      case 'day':
        return Inputs.table(d3.filter(data, d => (new Date(d.date).getFullYear() == dateInfo[0])&&(new Date(d.date).getMonth()+1 == dateInfo[1]) && (new Date(d.date).getDate() == dateInfo[2])))
    
    }
  }
  else {
    return html`<i>Click on the date on top of navigation bar to display data<i>`
  }
}


function _9(md){return(
md`### Inputs`
)}

function _10(md){return(
md`Inputs are collected here with Observable UI widgets, but would be passed to the viz via external UI elements in non-prototype context`
)}

function _11(width){return(
width
)}

function _dateInfo(){return(
null
)}

function _timeSelected(timeSpan){return(
timeSpan.period
)}

function _axisLabel(axisLabelTest){return(
axisLabelTest.axis
)}

function _margin(){return(
{top: 30, bottom: 40, left: 130, right: 20}
)}

function _scaleType(scaleTypeTest){return(
scaleTypeTest.scale
)}

function _color(getColor,colorScheme){return(
getColor(colorScheme.value)[0]
)}

function _color2(getColor,colorScheme){return(
getColor(colorScheme.value)[1]
)}

function _getColor(d3){return(
(color) => {
  const userScheme = {
    'blue': [d3.interpolateBlues,d3.schemeTableau10[0]],
    'green': [d3.interpolateGreens,d3.schemeTableau10[4]],
    'grey': [d3.interpolateGreys,d3.schemeTableau10[9]],
    'orange': [d3.interpolateOranges,d3.schemeTableau10[1]],
    'purple': [d3.interpolatePurples,d3.schemeTableau10[6]],
    'red': [d3.interpolateReds,d3.schemeTableau10[2]],
    'default': null
  }
  return userScheme[color] || userScheme['default']
}
)}

function _getData(d3,source){return(
(period) => {
  const userTable = {
    'year': d3.filter(source, d => d.agg == 'year'),
    'month': d3.filter(source, d => d.agg == 'month'),
    'day': d3.filter(source, d => d.agg == 'day'),
    'default': null
  }
  return userTable[period] || userTable['default']
}
)}

function _21(md){return(
md`### Functions for vizualisation `
)}

function _height(publications,margin){return(
25 * publications.length + margin.top + margin.bottom
)}

function _interval(axisLabel,d3){return(
axisLabel == 'day' ? d3.timeDay : axisLabel == 'month' ? d3.timeMonth : axisLabel == 'year' ? d3.timeYear : axisLabel == '5-year' ? d3.timeYear.every(5) : null
)}

function _x2(d3,ticks,margin,width){return(
d3
  .scaleTime()
  .domain([d3.min(ticks[1]), d3.max(ticks[1])])
  .range([margin.left, width - margin.right])
)}

function _x3(d3,dates_list,margin,width){return(
d3
  .scaleLinear()
  .domain([0,dates_list])
  .range([margin.left, width - margin.right])
)}

function _colorScale(d3,color,data){return(
d3.scaleSequential(color)
  .domain([0,d3.max(data,(d) => +d.count)])
)}

function _yScale(d3,data){return(
d3.scaleLinear()
  .domain([0,d3.max(data,(d) => +d.count)])
  .range([20,0])
)}

function _dateFormatLabel(timeSelected,d3){return(
timeSelected == 'day' ? d3.timeFormat("%B %d, %Y"): timeSelected == 'month' ? d3.timeFormat("%B, %Y") : timeSelected == 'year' ? d3.timeFormat("%Y") : d3.timeFormat("%Y")
)}

function _dateFormat(timeSelected,d3){return(
timeSelected == 'day' ? d3.timeDay : timeSelected == 'month' ? d3.timeMonth : timeSelected == 'year' ? d3.timeYear : null
)}

function _ticks(timeSelected,ticksYear,ticksMonth,ticksDay){return(
timeSelected == 'year' ? ticksYear() : timeSelected == 'month' ? ticksMonth() : timeSelected == 'day' ? ticksDay() : null
)}

function _ticksYear(dates_list){return(
() => {
  const date1 = new Date(dates_list[0])
  const year1 = date1.getFullYear() 
  const datemin = new Date(date1.setFullYear(year1-1))
  const date2 = new Date(dates_list[dates_list.length - 1])
  const year2 = date2.getFullYear() 
  const datemax = new Date(date2.setFullYear(year2+2))
  const newDatesStr = dates_list
  newDatesStr.unshift(`${datemin}`)
  newDatesStr.push(`${datemax}`)
  const newDates = newDatesStr.map(date => new Date(date))
  return [newDatesStr,newDates]
}
)}

function _ticksMonth(dates_list){return(
() => {
  const date1 = new Date(dates_list[0])
  const month1 = date1.getMonth() 
  const datemin = new Date(date1.setMonth(month1-1))
  const date2 = new Date(dates_list[dates_list.length - 1])
  const month2 = date2.getMonth() 
  const datemax = new Date(date2.setMonth(month2+2))
  const newDatesStr = dates_list
  newDatesStr.unshift(`${datemin}`)
  newDatesStr.push(`${datemax}`)
  const newDates = newDatesStr.map(date => new Date(date))
  return [newDatesStr,newDates]
}
)}

function _ticksDay(dates_list){return(
() => {
  const date1 = new Date(dates_list[0])
  const day1 = date1.getDate() 
  const datemin = new Date(date1.setDate(day1-1))
  const date2 = new Date(dates_list[dates_list.length - 1])
  const day2 = date2.getDate() 
  const datemax = new Date(date2.setDate(day2+2))
  const newDatesStr = dates_list
  newDatesStr.unshift(`${datemin}`)
  newDatesStr.push(`${datemax}`)
  const newDates = newDatesStr.map(date => new Date(date))
  return [newDatesStr,newDates]
}
)}

function _34(md){return(
md`### Data`
)}

function _dates_list(data){return(
[...new Set(data.map(d => d.date))]
)}

function _publications(data){return(
[...new Set(data.map(d => d.publication_name))]
)}

function _data(getData,timeSelected){return(
getData(timeSelected)
)}

function _source(FileAttachment){return(
FileAttachment("df_distrib@1.csv").csv()
)}

function _39(md){return(
md`### Imports`
)}

function _42(md){return(
md`### Styling`
)}

function _style(html){return(
html`
<style>
@import url('https://fonts.googleapis.com/css2?family=Palanquin:wght@400;700&display=swap');
form {font-family: 'Palanquin', sans-serif;}
form.label {display: 'block';}
.grid line {
  stroke-width: .2;
  stroke: rgba(0,0,0,.5);
  stroke-dasharray: .5;
}
#date-label {
  cursor: pointer;
}
form table {font-family: 'Palanquin', sans-serif;}
</style>
`
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["df_distrib@1.csv",new URL("./files/af788bf38e949778a945d97592d0ef07e0f0e084dbd0e8b95c3593a3e6b79e3cf7b3fd12bbecc9dd8cb87d5ec70e7ef941176a936079d45a96f6fa5c8205ef9c",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer()).define(["md"], _2);
  main.variable(observer("viewof colorScheme")).define("viewof colorScheme", ["form","html"], _colorScheme);
  main.variable(observer("colorScheme")).define("colorScheme", ["Generators", "viewof colorScheme"], (G, _) => G.input(_));
  main.variable(observer("viewof timeSpan")).define("viewof timeSpan", ["form","html"], _timeSpan);
  main.variable(observer("timeSpan")).define("timeSpan", ["Generators", "viewof timeSpan"], (G, _) => G.input(_));
  main.variable(observer("viewof scaleTypeTest")).define("viewof scaleTypeTest", ["form","html"], _scaleTypeTest);
  main.variable(observer("scaleTypeTest")).define("scaleTypeTest", ["Generators", "viewof scaleTypeTest"], (G, _) => G.input(_));
  main.variable(observer("viewof axisLabelTest")).define("viewof axisLabelTest", ["form","html"], _axisLabelTest);
  main.variable(observer("axisLabelTest")).define("axisLabelTest", ["Generators", "viewof axisLabelTest"], (G, _) => G.input(_));
  main.variable(observer("viewof chart")).define("viewof chart", ["d3","width","height","margin","x2","interval","publications","data","scaleType","yScale","dateFormat","colorScale","color2","dateFormatLabel","mutable dateInfo","addEventListener"], _chart);
  main.variable(observer("chart")).define("chart", ["Generators", "viewof chart"], (G, _) => G.input(_));
  main.variable(observer("viewof Table")).define("viewof Table", ["dateInfo","timeSelected","Inputs","d3","data","html"], _Table);
  main.variable(observer("Table")).define("Table", ["Generators", "viewof Table"], (G, _) => G.input(_));
  main.variable(observer()).define(["md"], _9);
  main.variable(observer()).define(["md"], _10);
  main.variable(observer()).define(["width"], _11);
  main.define("initial dateInfo", _dateInfo);
  main.variable(observer("mutable dateInfo")).define("mutable dateInfo", ["Mutable", "initial dateInfo"], (M, _) => new M(_));
  main.variable(observer("dateInfo")).define("dateInfo", ["mutable dateInfo"], _ => _.generator);
  main.variable(observer("timeSelected")).define("timeSelected", ["timeSpan"], _timeSelected);
  main.variable(observer("axisLabel")).define("axisLabel", ["axisLabelTest"], _axisLabel);
  main.variable(observer("margin")).define("margin", _margin);
  main.variable(observer("scaleType")).define("scaleType", ["scaleTypeTest"], _scaleType);
  main.variable(observer("color")).define("color", ["getColor","colorScheme"], _color);
  main.variable(observer("color2")).define("color2", ["getColor","colorScheme"], _color2);
  main.variable(observer("getColor")).define("getColor", ["d3"], _getColor);
  main.variable(observer("getData")).define("getData", ["d3","source"], _getData);
  main.variable(observer()).define(["md"], _21);
  main.variable(observer("height")).define("height", ["publications","margin"], _height);
  main.variable(observer("interval")).define("interval", ["axisLabel","d3"], _interval);
  main.variable(observer("x2")).define("x2", ["d3","ticks","margin","width"], _x2);
  main.variable(observer("x3")).define("x3", ["d3","dates_list","margin","width"], _x3);
  main.variable(observer("colorScale")).define("colorScale", ["d3","color","data"], _colorScale);
  main.variable(observer("yScale")).define("yScale", ["d3","data"], _yScale);
  main.variable(observer("dateFormatLabel")).define("dateFormatLabel", ["timeSelected","d3"], _dateFormatLabel);
  main.variable(observer("dateFormat")).define("dateFormat", ["timeSelected","d3"], _dateFormat);
  main.variable(observer("ticks")).define("ticks", ["timeSelected","ticksYear","ticksMonth","ticksDay"], _ticks);
  main.variable(observer("ticksYear")).define("ticksYear", ["dates_list"], _ticksYear);
  main.variable(observer("ticksMonth")).define("ticksMonth", ["dates_list"], _ticksMonth);
  main.variable(observer("ticksDay")).define("ticksDay", ["dates_list"], _ticksDay);
  main.variable(observer()).define(["md"], _34);
  main.variable(observer("dates_list")).define("dates_list", ["data"], _dates_list);
  main.variable(observer("publications")).define("publications", ["data"], _publications);
  main.variable(observer("data")).define("data", ["getData","timeSelected"], _data);
  main.variable(observer("source")).define("source", ["FileAttachment"], _source);
  main.variable(observer()).define(["md"], _39);
  const child1 = runtime.module(define1);
  main.import("Inputs", child1);
  const child2 = runtime.module(define2);
  main.import("form", child2);
  main.variable(observer()).define(["md"], _42);
  main.variable(observer("style")).define("style", ["html"], _style);
  return main;
}
