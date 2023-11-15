function d3PieChart(dataset, datasetClosingChart){
    // Set up SVG dimensions and properties
    const margin = {top:10, right:10, bottom:10, left:10};
    const width = 500,
    height = 500,
    outerRadius = Math.min(width, height) / 2,
    innerRadius = outerRadius * .5;
    const color = d3.scaleOrdinal()
        .domain(d3.range(dataset.length))
        .range(['#289c40', '#a5e06c', '#0e5b45', '#00221c']);
 
    // Selecting the div with id pieChart on the index.html template file
    const visualization = d3.select('#pieChart')
        .append("svg")      //Injecting an SVG element
        .data([dataset])    //Binding the pie chart data
        .attr("width", width)
        .attr("height", height)
        .append("g")        //Grouping the various SVG components  
        .attr("transform", "translate(" + outerRadius + "," + outerRadius + ")"); //Piechart tranformation and transition upon page loading
 
    const data = d3.pie()   //Creating the data object that will develop the various segment of the pie chart.
        .sort(null)
        .value(function(d){return d.value;})(dataset);    // Retrieve the pie chart data values from our Flask app, the pie chart where tied to a 'value' key of a JSON object.
 
    // Generate an arc generator that produces the circular chart (outer circle)
    const arc = d3.arc()   
        .outerRadius(outerRadius)
        .innerRadius(0);
 
     // Generate an arc generator that produces the circular chart (inner circle)
    const innerArc = d3.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius);
 
    // Create pie chart slices based on the data object created
    const arcs = visualization.selectAll("g.slice")
        .data(data)                    
        .enter()    // creates the initial join of data to elements                      
        .append("svg:g")              
        .attr("class", "slice")
        .on("click", click);
 
    arcs.append("svg:path")     // create path element
        .attr("fill", function(d, i) { return color(i); } )     //Add color to slice
        .attr("d", arc)     // creates actual SVG path with associated data and the arc drawing function
        .append("svg:title")        // Add title to each piechart slice
        .text(function(d) { return d.data.category + ": " + d.data.value+"%"; });          
 
    d3.selectAll("g.slice")     // select slices in the group SVG element (pirchart)
        .selectAll("path")
        .transition()           //Set piechart transition on loading
        .duration(200)
        .delay(5)
        .attr("d", innerArc);
 
    arcs.filter(function(d) { return d.endAngle - d.startAngle > .1; })     //Define slice labels at certain angles
        .append("svg:text")     //Insert text area in SVG
        .attr("dy", "0.20em")      //shift along the y-axis on the position of text content
        .attr("text-anchor", "middle")      //Position slice labels
        .attr("transform", function(d) { return "translate(" + innerArc.centroid(d) + ")"; }) //Positioning upon transition and transform
        .attr("fill", "white")
        .text(function(d) { return d.data.category; }); // Append category name on slices
 
    visualization.append("svg:text") //Append the title of chart in the middle of the pie chart
        .attr("dy", ".20em")
        .attr("text-anchor", "middle")
        .text("Your custom portfolio")
        .attr("fill", "black")
        .attr("class","title");   
 
    // Function to update barchart when a piechart slice is clicked
    function click(d, i) {
        updateClosingChart(d.data.category, color(i), datasetClosingChart);
     }
 }