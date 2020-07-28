import React from 'react';


function InformationDisplay(props) {
    return (
        <div style={{ width: "80%", paddingLeft: "30rem", maxHeight: "50rem" }}>
            <h1 style={{ textAlign: "center" }} >Device Name</h1>
            <div className="border">
                <div className="p_style">
                    <p>Temperature</p>
                    <p>Test</p>
                </div>
                <div className="p_style">
                    <p>Humidity</p>
                    <p>Test</p>
                </div>
                <div className="p_style">
                    <p>Smoke Density</p>
                    <p>Test</p>
                </div>
                <div className="p_style">
                    <p>Local Time</p>
                    <p>Test</p>
                </div>

            </div>
        </div>

    )
}
export default InformationDisplay