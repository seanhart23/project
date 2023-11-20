const urls = [
   pieChartDataUrl
   ];

const urlRests = [
   pieChartDataUrl,
   closingChartDataUrl,
   cumulativeReturnsChartUrl,
   rollingBetaChartUrl,
   roiChartUrl, 
   heatmapChartUrl
   ];

Promise.all(urls.map(url => d3.json(url))).then(runPie);


function runPie(dataset) {
   d3PieChart(dataset[0], dataset[1]);
};

Promise.all(urlRests.map(urlRest => d3.json(urlRest))).then(runRest);

function runRest(dataset) {
   d3ClosingChart(dataset[1]);
   d3CumulativeReturnsChart(dataset[2]);
   d3RollingBetaChart(dataset[3]);
   d3RoiChart(dataset[4]);
   d3HeatmapChart(dataset[5]);
};

