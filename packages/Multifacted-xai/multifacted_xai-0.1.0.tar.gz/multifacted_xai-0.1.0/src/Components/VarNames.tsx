import React from "react";
import { useExp } from "src/Context/ExpContext";
import { COL_WIDTH, COL_GAP } from "src/Const";

const headerStyle = {
    display: "flex"
  }
  
  const cellStyle: React.CSSProperties  = {
    color: "black",
    flex: `1 0 ${COL_WIDTH -6}px`,
    padding: "0 2px",
    marginRight:`${COL_GAP}px`,
    border: "1px solid black",
    borderRadius: "3px",
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis",
    height:"fit-content"
}

export default function VarNames() {
    const {exp} = useExp();
    const { names } = exp['independent_vars']
   
    return <>
    <div className='target block' style={{color:"black"}}>
        <span className='label left'>Depedent Variable: </span> 
        <span className="right">{exp['dependent_var']} </span>
    </div>
    <div className="block">
        <span className='label left'>Independent Variables: </span>
    
        <div className="header right" style={headerStyle}>
            {names.map((name, i) => (<span key={i} className="var" style={cellStyle}>{name}</span>))} 
        </div>
    </div>
    </>
}
