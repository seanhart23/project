function d3RollingBetaChart(dataset){

    function get_grouped_data(group, dataset){
        const _ = [];
        for (let obj of dataset){
            if (obj['group']==group){
                _.push(obj)
            }
        }
        return _;
    };
    // set the dimensions and margins of the graph
    const margin = {top: 50, right: 30, bottom: 60, left: 70};
    let width = 800 - margin.left - margin.right;
    let height = 500 - margin.top - margin.bottom;

    dataset = get_grouped_data('Beta', dataset);

    // append the svg object to the body of the page
    const svgContainer = d3.select("#rollingBetaChart")
    .append("svg")      //Injecting an SVG element
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    const svg = svgContainer.append("g")        //Grouping the various SVG components  
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

    const xAxis = d3.axisBottom(xScale)
    .tickFormat(d3.timeFormat("%b %Y"));

    
    svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .selectAll("text")  
    .style("text-anchor", "end")
    .attr("transform", "rotate(-65)" )

    // Add Y axis
    var yScale = d3.scaleLinear()
    .domain([2 * d3.min(dataset, function(d) { return d.value; }) - 0.5, 1.5*d3.max(dataset, function(d) { return +d.value; })])
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
    .datum(dataset)
    .attr("class", "line")
    .attr("fill", "none")
    .attr("stroke", "#289c40")
    .attr("stroke-width", 2.5)
    .attr("d", line);


     svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .text("Rolling Beta");


 }