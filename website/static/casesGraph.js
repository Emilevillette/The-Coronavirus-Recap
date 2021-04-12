var ctx = document.getElementById("cases_graph");
var json = JSON.parse('data/graph_data/graph_data_cases.json'); //(with path)
var cases_graph = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Object.keys(json.casescountry),
        datasets: [{
            data: Object.values(json.casescountry)
        }]
    }
})