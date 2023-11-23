function d3HeatmapChart(dataset){
    var containerWidth = $(".chart").width();
    var containerHeight = $(".chart").height();
    
    // set the dimensions and margins of the graph
    // var margin = {top: 80, right: 15, bottom: 30, left: 100}
    const margin = {top: parseInt($(".paddingHeat").css("marginTop")), right: parseInt($(".paddingHeat").css("marginRight")), bottom: parseInt($(".paddingHeat").css("marginBottom")), left: parseInt($(".paddingHeat").css("marginLeft"))};

    var width = containerWidth - margin.left - margin.right;
    var height = containerHeight - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svgContainer = d3.select("#heatmapChart")
    .append("svg")
    .attr("width", containerWidth)
    .attr("height", containerHeight)
    .style("background-color", "#a5e06c")
    var svg = svgContainer.append("g")
    .attr("transform","translate(" + margin.left + "," + margin.top + ")");

    // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
    var myGroups = d3.map(dataset, function(d){return d.group;}).keys()
    var myVars = d3.map(dataset, function(d){return d.variable;}).keys()

    // Build X scales and axis:
    var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(myGroups)
        .padding(0.05);
    svg.append("g")
        .style("font-size", 12)
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSize(0))
        .select(".domain").remove()

    // Build Y scales and axis:
    var y = d3.scaleBand()
        .range([ height, 0 ])
        .domain(myVars)
        .padding(0.05);
    svg.append("g")
        .style("font-size", 12)
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove()

    // Build color scale
    var myColor = d3.scaleLinear()
        .range(["#289c40", "#0e5b45", "#00221c"])
        .domain([0.7, 0.85, 1])

    // create a tooltip
    var tooltip = d3.select("#heatmapChart")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px")
        .style("z-index", "10")
        .style("position", "absolute")

    // Three function that change the tooltip when user hover / move / leave a cell
    var mouseover = function(d) {
        tooltip
        .style("opacity", 1)
        d3.select(this)
        .style("stroke", "black")
        .style("opacity", 1)
    }
    var mousemove = function(d) {
        tooltip
        .html("The exact value of this cell is: " + d.value)
        .style("left", (d3.mouse(this)[0]+70) + "px")
        .style("top", (d3.mouse(this)[1]) + "px")
    }
    var mouseleave = function(d) {
        tooltip
        .style("opacity", 0)
        d3.select(this)
        .style("stroke", "none")
        .style("opacity", 0.8)
    }

    // add the squares
    svg.selectAll()
        .data(dataset, function(d) {return d.group+':'+d.variable;})
        .enter()
        .append("rect")
        .attr("x", function(d) { return x(d.group) })
        .attr("y", function(d) { return y(d.variable) })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .style("fill", function(d) { return myColor(d.value)} )
        .style("stroke-width", 4)
        .style("stroke", "none")
        .style("opacity", 0.8)
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)

    // Add title to graph
    svg.append("text")
            .attr("x", 0)
            .attr("y", -40)
            .attr("text-anchor", "left")
            .style("font-size", "22px")
            .text("Correlation Heatmap");

    // Add subtitle to graph
    svg.append("text")
            .attr("x", 0)
            .attr("y", -20)
            .attr("text-anchor", "left")
            .style("font-size", "14px")
            .style("fill", "grey")
            .style("max-width", 400)
            .text("Correlation values for every pair of tickers.");



}


 
    
 