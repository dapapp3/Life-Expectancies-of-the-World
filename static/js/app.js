const Base_url = "http://127.0.0.1:5000/api/v1.0/";

// Initializes the page with a default plot
function init() {

  // Select the dropdown menus from HTML file
  let dropdownMenu = d3.select("#selCountry");
  let dropdownMenu_Year = d3.select("#selYear");

  // Fetch the JSON data
  d3.json(Base_url + "base").then((data) => {
      // Loop through a countries Array appending each to the html file so that they appear as options in the dropdownMenu
      let countries = data;
      countries.forEach((country) => {dropdownMenu.append("option").text(country[0]).property("value", country[0]);});

      // Loop through a years Array appending each to the html file so that they appear as options in the dropdownMenu_Year
      let years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]
      years.forEach((year) => {dropdownMenu_Year.append("option").text(year).property("value", year)})

      // Assign default country value for initial page load
      let country = countries[1][0];
      dropdownMenu.property("value", country);

      // Create default/starter charts
      update_country_info();
      update_line_chart();
      update_bar_chart();
      update_gauge_chart();
      update_country_mortality();
      update_average_mortality_chart();
  });
};

// Function to create/update the country info panel
function update_country_info() {
  // Find Data For Chosen Country & Year
  let Country_Name = d3.select("#selCountry").property("value");
  let Chosen_Year = d3.select("#selYear").property("value");
  
  // Fetch the JSON data
  d3.json(Base_url + Country_Name + "/" + Chosen_Year).then((data) => {
      // Clears previously populated elements from sample-metadata div tag to prep for upcoming append
      d3.select("#sample-metadata").html("");

      // Append country info to html file's sample-metadata div section
      for (const key in data) {
          if (Object.hasOwnProperty.call(data, key)) {
              const value = data[key];
              d3.select("#sample-metadata").append("h5").text(`${key}: ${value}`);
          }
      }
  });
};

function update_line_chart() {
  // Find Data For Chosen Country
  let Country_Name = d3.select("#selCountry").property("value");

  d3.json(Base_url + Country_Name).then(function(data) {
    // Create an empty array for the x-axis (years) and for the y-axis (life expectancy)
    var years = [];
    var LifeExp = new Map();

    // Loop through each object in the data array and extract the year and life expectancy
    data.forEach(function(d) {
      years.push(d.Year);
      LifeExp.set(d.Year, d.Life_Expectancy);
    });

    // Sort the years array based on the year values
    years.sort(function(a, b) {
      return a - b;
    });
    
    // Sort the LifeExp array based on the corresponding year value
    var sortedLifeExp = years.map(function(year) {
      return LifeExp.get(year);
    });

    // Destroy the existing chart, if one exists
    var chartElement = document.getElementById('LifeExp_ChartJS');
    var existingChart = Chart.getChart(chartElement);
    if (existingChart) {
      existingChart.destroy();
    }

    // Create a Chart.js line chart
    var chart = new Chart('LifeExp_ChartJS', {
      type: 'line',
      data: {
        labels: years,
        datasets: [{
          label: 'Life Expectancy by Year',
          data: sortedLifeExp,
          borderColor: 'rgb(255, 99, 132)',
          fill: false
        }]
      },
      options: {
        title: {
          display: true,
          text: 'Life Expectancy by Year'
        },
        plugins: {
          datalabels: {
            display: true,
            align: 'end',
            color: 'rgb(255, 99, 132)'
          }
        }
      }
    });
  });
};

// Function to create/update the bar chart
function update_bar_chart() {
  // Find Data For Chosen Country
  let Country_Name = d3.select("#selCountry").property("value");

  d3.json(Base_url + Country_Name).then(function(data) {
    // Create an empty array for the x-axis (years) and for the y-axis (population)
    var years = [];
    var populationData = [];
  
    // Loop through each object in the data array and extract the year and population
    data.forEach(function(d) {
      years.push(d.Year);
      populationData.push(d.Population_Millions);
    });
  
    // Sort the populationData array based on the corresponding year value
    var sortedPopulationData = populationData.slice().sort(function(a, b) {
      return populationData[years.indexOf(a.Year)] - populationData[years.indexOf(b.Year)];
    });
  
    // Create a Plotly bar chart
    var trace = {
      x: years,
      y: sortedPopulationData,
      type: 'bar'
    };
    var layout = {
      title: 'Population (in millions) by Year'
    };
    Plotly.newPlot('bar', [trace], layout);
  });
};

// Make the gauge chart 
function update_gauge_chart() {
  // Fetch the JSON data
  d3.json(Base_url + "life-expectancy").then((data) => {
      // Find Life Expectancy Percentile For Chosen Country
      let Country_Name = d3.select("#selCountry").property("value");
      let percentileValue = null;
      let resultDict = data.find(result => result.Country === Country_Name);
      if (resultDict) {percentileValue = resultDict.Percentile};

      // Set trace info for gauge chart
      let trace = [{
          value: percentileValue,
          title: { text: "<b>Life Expectancy (Percentile)", font: {size: 24}},
          type: "indicator", 
          mode: "gauge+number",
          gauge: {
              axis: {range: [null, 100]}, 
              bar: {color: "rgb(70,70,200)"},
              steps: [
                  { range: [0, 10], color: "rgb(235,255,250)" },
                  { range: [10, 20], color: "rgb(220,245,245)" },
                  { range: [20, 30], color: "rgb(205,235,240)" },
                  { range: [30, 40], color: "rgb(190,225,235)" },
                  { range: [40, 50], color: "rgb(175,215,230)" },
                  { range: [50, 60], color: "rgb(160,205,225)" },
                  { range: [60, 70], color: "rgb(145,195,220)" },
                  { range: [70, 80], color: "rgb(130,185,215)" },
                  { range: [80, 90], color: "rgb(115,175,210)" },
                  { range: [90, 100], color: "rgb(100,165,205)" }
              ]
          }
      }];

       // Plot the gauge chart
       Plotly.newPlot("gauge", trace);
  });
};

// Make the Single-Country Mortality Chart
function update_country_mortality() {
  // Find Data For Chosen Country
  let Country_Name = d3.select("#selCountry").property("value");

  d3.json(Base_url + Country_Name).then(function(data) {
  var years = [];
  var infantDeaths = [];
  var fiveYearDeaths = [];
  var adultMortality = [];

  // Sort Data
  sorted_data = data.sort((a, b) => a.Year - b.Year);

  // Loop through each object in the data array and extract the year and population
  sorted_data.forEach(function(d) {
    years.push(d.Year);
    infantDeaths.push(d.Infant_Deaths);
    fiveYearDeaths.push(d.Under_Five_Deaths);
    adultMortality.push(d.Adult_Deaths);
  });

  var trace3 = {
    x: years,
    y: infantDeaths,
    mode: 'lines+markers',
    name: 'Infant Deaths'
  };
  
  var trace2 = {
    x: years,
    y: fiveYearDeaths,
    mode: 'lines+markers',
    name: 'Five Year Deaths'
  };
  
  var trace1 = {
    x: years,
    y: adultMortality,
    mode: 'lines+markers',
    name: 'Adult Mortality'
  };
  
  var trace_data = [ trace1, trace2, trace3 ];
  
  var linelayout = {
    title:'Selected Country Mortality',
    xaxis: {
      title: 'Year',
      showgrid: false,
      zeroline: false
    },
    yaxis: {
      title: 'Deaths per 1000',
      showline: false
    }
  };
  
  Plotly.newPlot('line', trace_data, linelayout);
  });
};

// Make the AVG Mortality Chart
function update_average_mortality_chart() {
  // Find Data For Chosen Country
  let Country_Name = d3.select("#selCountry").property("value");

  d3.json(Base_url + "avg_mortality").then(function(data) {
    // Create an empty array for the x-axis (years) and for the y-axis (population)
    var years = [];
    var infantDeaths = [];
    var fiveYearDeaths = [];
    var adultMortality = [];
    sorted_data = data.sort((a, b) => a.Year - b.Year)
    // Loop through each object in the data array and extract the year and population
    sorted_data.forEach(function(d) {
      years.push(d.Year);
      infantDeaths.push(d.Infant_Deaths);
      fiveYearDeaths.push(d.Under_Five_Deaths);
      adultMortality.push(d.Adult_Deaths);
    });

    var trace3 = {
      x: years,
      y: infantDeaths,
      mode: 'lines+markers',
      name: 'Infant Deaths'
    };
    
    var trace2 = {
      x: years,
      y: fiveYearDeaths,
      mode: 'lines+markers',
      name: 'Five Year Deaths'
    };
    
    var trace1 = {
      x: years,
      y: adultMortality,
      mode: 'lines+markers',
      name: 'Adult Mortality'
    };
    
    var trace_data = [ trace1, trace2, trace3 ];
    
    var linelayout = {
      title:'Average Mortality',
      xaxis: {
        title: 'Year',
        showgrid: false,
        zeroline: false
      },
      yaxis: {
        title: 'Deaths per 1000',
        showline: false
      }
    };
    
    Plotly.newPlot('line2', trace_data, linelayout);
  });
};

// Update plots when an option is changed
function option_changed() {
    update_country_info();
    update_line_chart();
    update_bar_chart();
    update_gauge_chart();
    update_country_mortality();
    update_average_mortality_chart();
};

// Call init function on page load
init();