
barPadding = 10,
graph_misc = {ylabel: 4, xlabelH : 5, title:9};

// Setting the default group
const group = "All";

// Function to get the percentage values  for a specific selected group from the whole dataset.
function get_percentage(group, datasetBarChart){
   const _ = [];
   for (instance in datasetBarChart){
       if (datasetBarChart[instance].group==group){
           _.push(datasetBarChart[instance])
       }
   } return _;
};

function d3RoiChart(datasetBarChart){
   defaultBarChart = get_percentage(group, datasetBarChart);

    var containerWidth = $(".chart").width();
    var containerHeight = $(".chart").height();

    // set the dimensions and margins of the graph
    const margin = {top: 50, right: 10, bottom: 40, left: 30};
    var width = containerWidth - margin.left - margin.right;
    var height = containerHeight - margin.top - margin.bottom;

   const xScale = d3.scaleLinear()     // Barchart X axis scale
       .domain([0, defaultBarChart.length]) // Scale range from 0 to the length of data object
       .range([0, width]);

   const yScale = d3.scaleLinear() // Barchart y axis scale
       .domain([-d3.min(defaultBarChart, function(d) { return d.value; }), 1.5*d3.max(defaultBarChart, function(d) { return d.value; })])    //Scale range from 0 to the maximum value of the default bar chart data
       .range([height, 0]);

   // // Selecting the div with id barChart on the index.html template file
   const bar = d3.select('#barChart')
       .append('svg')
       .attr("width", containerWidth)
       .attr("height", containerHeight)
       .attr('id', 'barChartPlot');

    bar.append("text")
        .attr('x', (width + margin.left + margin.right)/2)
        .attr('y', graph_misc.title + 20)
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .text("Portfolio ROI (%)");

   const visualization = bar.append('g')
       .attr("transform", "translate(" + margin.left + "," + (margin.top + graph_misc.ylabel) + ")");

   visualization.selectAll("rect")
       .data(defaultBarChart)
       .enter()
       .append("rect")
       .attr("x", function(d, i) {
           return xScale(i);
       })
       .attr("width", width / defaultBarChart.length - barPadding)  
       .attr("y", function(d) {
           return yScale(d.value);
       }) 
       .attr("height", function(d) {
           return height-yScale(d.value);
       })
       .attr("fill", "#289c40");

   //Adding  barchart labels
   visualization.selectAll('text')
       .data(defaultBarChart)
       .enter()
       .append("text")
       .text(function(d) {
               return d.value+"%";
       })
       .attr("text-anchor", "middle")
       .style("fill", "white")

       .attr("x", function(d, i) {
               return (i * (width / defaultBarChart.length)) + ((width / defaultBarChart.length - barPadding) / 2);
       })
       .attr("y", function(d) {
               return (yScale(d.value) - graph_misc.ylabel); //Setting the Y axis to represent the value in the served JSON data
       })
       .attr("class", "yAxis");

   const xLabels = bar
       .append("g")
       .attr("transform", "translate(" + margin.left + "," + (margin.top + height + graph_misc.xlabelH)  + ")");

   xLabels.selectAll("text.xAxis")
       .data(defaultBarChart)
       .enter()
       .append("text")
       .text(function(d) { return d.category;})
       .attr("text-anchor", "middle")
       .attr("x", function(d, i) {
           return (i * (width / defaultBarChart.length)) + ((width / defaultBarChart.length - barPadding) / 2);
       })
       .attr("y", 15)
       .attr("class", "xAxis");           
}


