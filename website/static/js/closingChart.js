
function d3ClosingChart(dataset){
    // set the dimensions and margins of the graph
    const margin = {top: 50, right: 30, bottom: 60, left: 65},
    width = 800 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    function get_grouped_data(group, dataset){
        const _ = [];
        for (let obj of dataset){
            if (obj['group']==group){
                _.push(obj)
            }
        }
        return _;
    }
    default_stock = dataset[0]['stocks'][0]   
    dataset = get_grouped_data(default_stock, dataset)

    const svgContainer = d3.select("#closingChart")
    .append("svg")      //Injecting an SVG element
    .data([dataset])    //Binding the pie chart data
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("background", "rgb(0,34,28)")
    .style("background", "linear-gradient(135deg, rgba(0,34,28,1) 47%, rgba(18,91,69,1) 100%)")
    .style("color", "white")
    .style("font-family", "Gotham-Lgt")
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
    .attr("class","myXaxis");

    // Add Y axis
    var yScale = d3.scaleLinear()
    .domain([d3.min(dataset, function(d) { return +d.value; }), d3.max(dataset, function(d) { return +d.value; })])
    .range([ height, 0 ]);
    svg.append("g")
    .attr("class","myYaxis")
    .call(d3.axisLeft(yScale));

    svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2.5))
        // .attr("dy", "1em")
        .attr("class", "label")
        .style("text-anchor", "middle")
        .style("font-size", "16px")
        .text("Closing Prices in USD for "+ default_stock)

    const line = d3.line()
    .x(function(d) { return xScale(parseDate(d.date)); })
    .y(function(d) { return yScale(d.value); });

    // Add the line
    svg.append("path")
    .datum(dataset)
    .attr("class", "line")
    .attr("fill", "none")
    .attr("stroke", "#289c40")
    .attr("stroke-width", 1.5)
    .attr("d", line);

 }