// Stats Pie Chart

var ctx2 = document.getElementById('statsPieChart').getContext('2d');

var walletPieChart = new Chart(ctx2, {

  type: 'doughnut',

  data: {
    datasets: [{
      data: [15, 15, 20, 25, 25],
      backgroundColor: ['#dc3545','#fd7e14','#ffc107','#28a745','#007bff'],
      label: 'Dataset 1'
    }],
    labels: ['red','orange','yellow','green','blue']
  },
  
  options: {

    legend: {
      align: 'start',
      position: 'right',
    },

  }
});
