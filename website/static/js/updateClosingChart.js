function updateClosingChart(group, color, datasetClosingChart){
    function get_grouped_data(group, dataset){
        const _ = [];
        for (let obj of dataset){
            if (obj['group']==group){
                _.push(obj)
            }
        }
        return _;
    }
    const currentClosingChart = get_grouped_data(group, datasetClosingChart);

    const svg = d3.select("#closingChart svg")
    const margin = {top: 50, right: 30, bottom: 60, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;
    let graph_misc = {ylabel: 4, xlabelH : 5, title:9};


    var parseDate = d3.timeParse("%Y-%m-%d");
    var dates = [];
    for (let obj of currentClosingChart) {
        dates.push(parseDate(obj.date));
    }

    // Add X axis --> it is a date format
    var xScale = d3.scaleTime()
    .domain(d3.extent(dates))
    .range([ 0, width ]);

    // Add Y axis
    var yScale = d3.scaleLinear()
    .domain([d3.min(currentClosingChart, function(d) { return d.value; }), d3.max(currentClosingChart, function(d) { return d.value; })])
    .range([ height, 0 ]);

    svg.selectAll('text.label')
    .text("Closing Prices in USD for "+ group);

    svg.selectAll('g.myYaxis')
    .transition()
    .duration(3000)
    .call(d3.axisLeft(yScale));

    const line = d3.line()
    .x(function(d) { return xScale(parseDate(d.date)); })
    .y(function(d) { return yScale(d.value); });


    // Add title to Barchart
    const closingChart = d3.select("#closingChart")

    closingChart.selectAll("text.title")
    .attr("x", (width + margin.left + margin.right)/2)
    .attr("y", graph_misc.title)
    .attr("text-anchor", "middle")
    .text("30 Day Closing Prices For " + group);

    // Create a update selection: bind to the new data
    var u = svg.selectAll(".line")
    .data([currentClosingChart], function(d){ return d.date });

    // Update the line
    u
    .enter()
    .append("path")
    .attr("class","line")
    .merge(u)
    .transition()
    .duration(3000)
    .attr("d", line)
        .attr("fill", "none")
        .attr("stroke", "#289c40")
        .attr("stroke-width", 2.5)
    };






