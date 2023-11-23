function d3CumulativeReturnsChart(dataset){

    function get_grouped_data(group, dataset){
        const _ = [];
        for (let obj of dataset){
            if (obj['group']==group){
                _.push(obj)
            }
        }
        return _;
    };
    
    var containerWidth = $(".chart").width();
    var containerHeight = $(".chart").height();

    // set the dimensions and margins of the graph
    // const margin = {top: 50, right: 30, bottom: 60, left: 80};
    const margin = {top: parseInt($(".padding").css("marginTop")), right: parseInt($(".padding").css("marginRight")), bottom: parseInt($(".padding").css("marginBottom")), left: parseInt($(".padding").css("marginLeft"))};
    const width = containerWidth - margin.right - margin.left;
    const height = containerHeight - margin.top - margin.bottom;

    custom_dataset = get_grouped_data('Your Portfolio', dataset);
    spy_dataset = get_grouped_data('SPY', dataset);

    // append the svg object to the body of the page
    const svgContainer = d3.select("#cumulativeReturnsChart")
    .append("svg")      //Injecting an SVG element
    .attr("width", containerWidth)
    .attr("height", containerHeight)
    const svg = svgContainer.append("g")   
    .attr("width", containerWidth)
    .attr("height", containerHeight)     //Grouping the various SVG components  
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var parseDate = d3.timeParse("%Y-%m-%d");
    var dates = [];
    for (let obj of dataset) {
        dates.push(parseDate(obj.date));
    }

    // Add X axis --> it is a date format
    var xScale = d3.scaleTime()
    .domain(d3.extent(dates))
    .range([ 0, width ]);
    
    svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale))
    .selectAll("text")  
    .style("text-anchor", "end")
    .attr("transform", "rotate(-65)" )
    .attr("class","myXaxis");

    // Add Y axis
    var yScale = d3.scaleLinear()
    .domain([-d3.min(dataset, function(d) { return +d.value; }), 1.1*d3.max(dataset, function(d) { return +d.value; })])
    .range([ height, 0 ]);
    svg.append("g")
    .attr("class","myYaxis")
    .call(d3.axisLeft(yScale));

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 10 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .attr("class", "label")
        .style("text-anchor", "middle")
        .text("USD");

    const line = d3.line()
    .x(function(d) { return xScale(parseDate(d.date)); })
    .y(function(d) { return yScale(d.value); });

    // Add the line
    svg.append("path")
    .datum(custom_dataset)
    .attr("class", "line")
    .attr("fill", "none")
    .attr("stroke", "#289c40")
    .attr("stroke-width", 2.5)
    .attr("d", line);

     // Add the line
     svg.append("path")
     .datum(spy_dataset)
     .attr("class", "line")
     .attr("fill", "none")
     .attr("stroke", "#0e5b45")
     .attr("stroke-width", 2.5)
     .attr("d", line);

     svg.append("text")
        .attr("x", ((width - margin.left) / 2))             
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .text("5 Yr Cumulative Portfolio Returns vs SPY");


    // Handmade legend
    svg.append("circle").attr("cx",50).attr("cy",30).attr("r", 6).style("fill", "#289c40")
    svg.append("circle").attr("cx",50).attr("cy",60).attr("r", 6).style("fill", "#0e5b45")
    svg.append("text").attr("x", 70).attr("y", 30).text("Your Portfolio").style("font-size", "15px").attr("alignment-baseline","middle")
    svg.append("text").attr("x", 70).attr("y", 60).text("SPY").style("font-size", "15px").attr("alignment-baseline","middle")
}




