import { Pie } from 'react-chartjs-2'
import React from 'react';

function PieChart(props) {
    const statusData = {
        labels: [
            "Promiment",
            "Safe",
            "Alert"
        ],
        datasets: [
            {
                label: "Status",
                backgroundColor: ["#009900", "#ff3300", "#ffff00"],
                borderColor: "#fff",
                borderWidth: 4,
                data: [30, 40, 30]
            }
        ]
    }
    return (
        <Pie
            data={statusData}
            options={{
                title: {
                    display: true,
                    text: "Status",
                    fontSize: 20
                },
                legend: {
                    display: true,
                    position: "bottom"
                },
                pieLabel: {
                    render: "percentage",
                    fontSize: 20
                }
            }}
        />

    )
}

export default PieChart