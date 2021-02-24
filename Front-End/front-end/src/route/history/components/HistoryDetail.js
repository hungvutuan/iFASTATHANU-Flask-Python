import React from 'react';
// import { DataTable } from 'react-native-paper';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import { useState, useEffect } from 'react'
//import Constants from 'expo-constants';
import PieChart from "./PieChart"
import { Bar } from 'react-chartjs-2'
import Paper from '@material-ui/core/Paper';




const useStyles = makeStyles({
  root: {
    width: '100%',
  },
  container: {
    maxHeight: 440,
  },
});

function HistoryDetail() {
  const classes = useStyles();
  const [page, setPage] = React.useState(0);
  const [data, setData] = useState([{ status: "Safe", location: "Home", name: "HM-0103", date: "06/03/2020", type: "Manual" }]);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = event => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  var datas = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [{
      label: "Test",
      backgroundColor: 'rgb(255, 99, 132)',
      borderColor: 'rgb(255, 99, 132)',
      data: [0, 10, 5, 2, 20, 30, 45],
    }]
  }

  return (

    <div>
      <div align="center">
        <h1>History</h1>
      </div>
      <div className="row" style={{ display: "flex", flexDirection: "row" }}>
        <div style={{ width: "50%" }}>
          <Bar
            data={datas}
            options={{
              title: {
                display: true,
                text: "test",
                fontSize: 20
              },
              legend: {
                display: true,
                position: "top",
              },
              scales: {
                xAxes: [
                  {
                    scaleLabel: {
                      display: true,
                      labelString: "Time"
                    }
                  }
                ],
                yAxes: [
                  {
                    scaleLabel: {
                      display: true,
                      labelString: "%"
                    }
                  }
                ]
              }
            }}
          />
        </div>

        <div style={{ width: "50%", margin: "0%" }}>
          <PieChart />
        </div>
      </div>


      <div style={{ paddingTop: "2rem" }}>
        <Paper className={classes.root}>
          <TableContainer className={classes.container}>
            <Table stickyHeader aria-label="sticky table">
              <TableHead>
                <TableRow>
                  <TableCell>Id</TableCell>
                  <TableCell align="right">Alarm Status</TableCell>
                  <TableCell align="right">Location</TableCell>
                  <TableCell align="right">Device Name</TableCell>
                  <TableCell align="right">Date</TableCell>
                  <TableCell align="right">Type</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map(row => {
                  return (
                    <TableRow >
                      <TableCell component="th" scope="row">
                        {row.Id}
                      </TableCell>
                      <TableCell align="right">{row.status}</TableCell>
                      <TableCell align="right">{row.location}</TableCell>
                      <TableCell align="right">{row.name}</TableCell>
                      <TableCell align="right">{row.date}</TableCell>
                      <TableCell align="right">{row.type}</TableCell>
                    </TableRow>

                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 15]}
            component="div"
            count={data.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onChangePage={handleChangePage}
            onChangeRowsPerPage={handleChangeRowsPerPage}
          />
        </Paper>
      </div>
    </div>
  )
}


export default HistoryDetail;
