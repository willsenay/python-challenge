// from data.js
var tableData = data;

// set reference to table body
var tbody = d3.select("tbody");

// set reference to filter button
var submit = d3.select("#filter-btn");

// do the following on a filter button click
submit.on("click", function() {

  // prevent page from refreshing
  d3.event.preventDefault();  

  // delete existing table rows
  $("#ufo-table tbody tr").remove();

  // select input id in html
  var inputElement = d3.select("#datetime");  
  
  // get the value of the element
  var inputValue = inputElement.property("value");   
  
  // filter the table and set to new var
  var filteredData = tableData.filter(date => date.datetime === inputValue);  
  
  // take the filtered data and add its values to table
  filteredData.forEach((sighting) => {
    var row = tbody.append("tr");
    Object.entries(sighting).forEach(([key, value]) => {
      var cell = row.append("td");
      cell.text(value);
    });
  });
});
