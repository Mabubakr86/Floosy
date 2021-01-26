// Wallet Pie Chart

var ctx1 = document.getElementById('walletPieChart').getContext('2d');

var walletPieChart = new Chart(ctx1, {

  type: 'doughnut',

  data: {
    datasets: [{
      data: [30, 15, 20, 25, 10],
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
