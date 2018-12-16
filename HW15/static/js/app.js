function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
  d3.json(`/metadata/${sample}`).then(

    // Use d3 to select the panel with id of `#sample-metadata`
    function(d){
      var sample_metadata = d3.select('#sample-metadata');

      // Use `.html("") to clear any existing metadata
      sample_metadata.html("")

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
      Object.entries(d).forEach(
        function([key, value]){
          sample_metadata.append("p").text(`${key}: ${value}`);
        }
      )

    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
    }
  )
}
  
function buildCharts(sample) {
    
  // @TODO: Use `d3.json` to fetch the sample data for the plots
  d3.json(`/samples/${sample}`).then(
    function(d){
      var otu_ids = d.otu_ids;
      var otu_labels = d.otu_labels;
      var sample_values = d.sample_values;
        
    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
    var pie_trace = {
      values: sample_values.sort(function(first, second){second - first}).slice(0,10),
      labels: otu_ids.sort(function(first, second){second - first}).slice(0, 10),
      type: 'pie'
    };
    var pie_data = [pie_trace];
      
    Plotly.newPlot("pie", pie_data);
      
    // @TODO: Build a Bubble Chart using the sample data
    var bubble_trace = {
      x: otu_ids,
      y: sample_values,
      mode: "markers",
      marker: {
        size: sample_values,
        color: otu_ids,
      },
      text: otu_labels
    };
    var bubble_data = [bubble_trace];
  
    Plotly.newPlot("bubble", bubble_data);

    }
  )
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
