// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

const d = new Date();
const day = d.getDate();

var dateArray = new Array(8);
for (var i =0 ; i<dateArray.length - 1; i++){
  dateArray[i] = new Date(new Date().setDate(day- 7 + i)).toLocaleDateString();
}
dateArray[7] = new Date(new Date().setDate(day)).toLocaleDateString();

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [dateArray[0],dateArray[1],dateArray[2],dateArray[3],dateArray[4],dateArray[5],dateArray[6],dateArray[7]],
    datasets: [
      {
        label: "company1",
        lineTension: 0.3,
        backgroundColor: "transparent",
        borderColor: "#FFCC00",
        pointRadius: 5,
        pointBackgroundColor: "#FFCC00",
        //pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        //pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849]
      },
      {
        label: "company2",
        lineTension: 0.3,
        backgroundColor: "transparent",
        borderColor: "#33CC00",
        pointRadius: 5,
        pointBackgroundColor: "#33CC00",
        //pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        //pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: [10010, 30000, 25000, 17000, 20000, 25000, 30004, 30010, 29000]
      },
      {
        label: "company3",
        lineTension: 0.3,
        backgroundColor: "transparent",
        borderColor: "#FF6699",
        pointRadius: 5,
        pointBackgroundColor: "#FF6699",
        //pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        //pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: [8000, 32000, 25000, 18000, 19000, 27000, 32000, 33000, 26000]
      },
      {
        label: "company4",
        lineTension: 0.3,
        backgroundColor: "transparent",
        borderColor: "#CC00FF",
        pointRadius: 5,
        pointBackgroundColor: "#CC00FF",
        //pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        //pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: [10500, 31000, 26000, 17000, 17500, 29600, 33333, 35664, 25346]
      },
      {
        label: "company5",
        lineTension: 0.3,
        backgroundColor: "transparent",
        borderColor: "#0033FF",
        pointRadius: 5,
        pointBackgroundColor: "#0033FF",
        //pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        //pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: [10266, 31165, 22354, 17539, 19112, 29234, 29535, 35684, 30264]
      },
    ],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 8
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 40000,
          maxTicksLimit: 5
        },
        gridLines: {
          display: true,
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
