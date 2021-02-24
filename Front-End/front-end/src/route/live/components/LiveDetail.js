import React from 'react';

import { makeStyles } from '@material-ui/core/styles';

import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import { useState, useEffect } from 'react'

function LiveDetail(props) {
  const useStyles = makeStyles({
    root: {
      width: '100%',

    },
    container: {
      maxHeight: 440,
    },
  });


  const classes = useStyles();
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };
  const handleChangeRowsPerPage = event => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <Paper className={classes.root}>
      <TableContainer className={classes.container}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              <TableCell>Id</TableCell>
              <TableCell align="right">Location</TableCell>
              <TableCell align="right">Temperature</TableCell>
              <TableCell align="right">Humidity</TableCell>
              <TableCell align="right">Smoke</TableCell>
              <TableCell align="right">Status</TableCell>
              <TableCell align="right">Time</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>

            <TableRow >
              <TableCell component="th" scope="row">
                {"HCM"}
              </TableCell>
              <TableCell align="right">{"60"}</TableCell>
              <TableCell align="right">{"80"}</TableCell>
              <TableCell align="right">{"No"}</TableCell>
              <TableCell align="right">{"Normal"}</TableCell>
              <TableCell align="right">{"Test"}</TableCell>
            </TableRow>

          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 15]}
        component="div"
        count={5}
        rowsPerPage={rowsPerPage}
        page={page}
        onChangePage={handleChangePage}
        onChangeRowsPerPage={handleChangeRowsPerPage}
      />
    </Paper>);
}
export default LiveDetail;