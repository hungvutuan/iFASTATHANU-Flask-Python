import React from 'react';
import { CircularProgressbarWithChildren } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import "./style.css"

function StatusDetail(props) {
    return (
        // <div clasName="container" style={{maxWidth:"50%"}}>
        //     <h2 style={{paddingLeft:"4rem"}}>Fire Probability</h2>
        //     <div style={{border:"solid",borderRadius:"50%", maxWidth:"50%",maxHeight:"200px",height:"200px",textAlign:"center"}}>
        //         <h3 style={{paddingTop:"1.5rem",fontSize:"60px",margin:"0px"}}>43%</h3>
        //         <p style={{fontSize:"25px",margin:"0px"}}>Prominent</p>
        //     </div>
        // </div>
        <div style={{ maxHeight: "30%", maxWidth: "30%" }}>
            <h1 style={{ textAlign: "center" }}>Fire Probability</h1>
            <CircularProgressbarWithChildren value={60} >
                <strong style={{ fontSize: 40, marginTop: -5 }}>60%</strong>
                <div><p>Safe</p></div>
            </CircularProgressbarWithChildren >
        </div>

    )
}
export default StatusDetail