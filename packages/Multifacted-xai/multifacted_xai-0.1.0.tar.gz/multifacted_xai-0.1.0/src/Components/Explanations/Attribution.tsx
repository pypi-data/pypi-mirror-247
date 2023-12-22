import React from "react";
import { useExp } from "src/Context/ExpContext";
import { COL_WIDTH, ATTR_ROW_HEIGHT, COL_GAP } from "src/Const";
import {scaleLinear} from 'd3-scale'

export default function Attribution() {
    const {exp} = useExp();
    const { attribution } = exp['explanations']
    // const content = attribution?.map((attr, i) => {
    //     return <g key={attr.name} className={attr.name}>
    //         {attr['score'].map((val, j) => {
    //         const radius = Math.abs(val) * 100
    //         return <circle 
    //             r={radius} 
    //             fill={val>0?"orange":"blue"} 
    //             cx={ i*radius/2  + COL_WIDTH*j } 
    //             cy={100}
    //         />})}
    //     </g>
    // })
    if (!attribution) return null
   
    const maxScore = Math.max(...attribution!.map(attr => Math.max(...attr['score'].map(v=>Math.abs(v)))))
    const hightScaler = scaleLinear().domain([0, maxScore]).range([0, ATTR_ROW_HEIGHT/2])
    const width = COL_WIDTH/(attribution.length)

    const content = attribution?.map((attr, expIdx) => {
        return <g key={attr.name} className={attr.name}>
            {attr['score'].map((val, varIdx) => {
            const height = hightScaler(Math.abs(val))
            return <g transform={`translate(${(COL_WIDTH+COL_GAP)*varIdx + width * expIdx }, 0)`}>
            <rect 
                fill={val>0?"steelblue":"orange"} 
                height={height}
                width={width}
                x={ 0 } 
                y={ val>0?ATTR_ROW_HEIGHT/2-height:ATTR_ROW_HEIGHT/2 }
                stroke="white"
            />
            <text textAnchor="middle" x={width/2} y={ATTR_ROW_HEIGHT/2 + (val>0? 12: -2)}>{attr['name']}</text>
            </g>})}
        </g>
    })
    return<div className="Attribution block"> 
    <div className="left">
        <span className='label'>Attribution Explanations:</span>
    </div>
    <div className="right">
    <svg width={(COL_WIDTH + COL_GAP)*attribution[0]['score'].length} height={ATTR_ROW_HEIGHT}>
        {content}
        <line x1={0} y1={ATTR_ROW_HEIGHT/2} x2={COL_WIDTH*attribution[0]['score'].length} y2={ATTR_ROW_HEIGHT/2} stroke="lightgray" />
    </svg>
    </div>
    </div>
}

