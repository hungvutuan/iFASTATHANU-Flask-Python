import React from 'react';
import InformationDisplay from './InformationDisplay';
import StatusDetail from './StatusDetail';




function MainDetail(props) {
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>MainBoard</h1>
      <div style={{ display: "flex", flexDirection: "row", paddingLeft: "28rem" }} className="row">
        <p>Current Status:</p>
        <select value="test" style={{ color: "green" }}>
          <option value="A" style={{ color: "green" }}>Active</option>
          <option value="B" style={{ color: "red" }}>Inactive</option>
        </select>

      </div>
      <div className="row" style={{ display: "flex", justifyContent: "space-between" }} >
        <StatusDetail />
        <InformationDisplay />
      </div>
    </div>

  )
}
export default MainDetail;