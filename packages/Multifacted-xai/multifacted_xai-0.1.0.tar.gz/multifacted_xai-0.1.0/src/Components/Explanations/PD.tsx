import React, {useRef, useEffect, ReactSVGElement, ReactHTMLElement, ReactNode} from "react";
import { useExp } from "src/Context/ExpContext";
import { COL_WIDTH, PD_ROW_HEIGHT, COL_GAP, PD_ROW_GAP, VAL_ROW_HEIGHT } from "src/Const";
import {scaleLinear, scaleBand, scaleSequential, ScaleSequential} from 'd3-scale'
import { showVarValue } from "src/helpers/helpers";

export default function Partial_Dependency() {
    // const canvasRef = useRef < HTMLCanvasElement >(null);
    const {exp} = useExp();
    const {ranges, values} = exp['independent_vars']
    const PDGroups = exp.explanations.pd
    const axes = values.map((val, i) => (<g transform={`translate(${(COL_WIDTH+COL_GAP)*i}, 0)`}> 
        <OneAxis val={val} range={ ranges[i]}/>
    </g>))

    const colorScaler = scaleLinear().domain([0, .5, 1]).range(["orange", "white", "steelblue"])

    // const legendWidth = 70, legendHeight = 20, legendMargin = 14
   
    const PDCharts = PDGroups?.map((group, group_index) => {
        return <g key={'PD:'+group.name} className={'PD:'+group.name} transform={`translate(0, ${group_index * (PD_ROW_HEIGHT + PD_ROW_GAP)})`}>
            
            {group.score.map((scoresForOneVar, var_index) => {
                return <g key={var_index} className={`var_${var_index}`} transform={`translate(${(COL_WIDTH+COL_GAP)*var_index}, 0)`}>
                    <OnePDChart scores={scoresForOneVar} scaler={colorScaler}/>
                </g>
            })}
            <text y={PD_ROW_HEIGHT}>{group.name}</text>
        </g>
    })
   
    return <div className="block PD">
        <div className="left" style={{gridRow: "1"}}>
            <span className="label">Partial Dependence</span>
        </div>
        {/* <canvas className="left" ref={canvasRef} 
            width={`${legendWidth + legendMargin * 2}px`} height={`${legendHeight + legendMargin }px`} 
            style={{gridRow: "2"}}
        /> */}
        <Legend scaler={colorScaler} />
        <div className="right" style={{gridRow: "1/3"}}>
            <svg width={(COL_WIDTH + COL_GAP)* values.length} height={(PD_ROW_HEIGHT + PD_ROW_GAP)*(PDGroups?.length||0) + VAL_ROW_HEIGHT + PD_ROW_GAP}>
                {axes}
                <g className="pd_charts" transform={`translate(0, ${VAL_ROW_HEIGHT + PD_ROW_GAP})`}>
                    {PDCharts}
                </g>
            </svg>
        </div>
    </div>
}


function OneAxis ({val, range}: {val: number | string, range: (number| string)[]}) {
    const labelW = 10,
    labelPath = `0,0, ${-0.5*labelW}, ${-0.5*labelW} ${-0.5*labelW}, ${-1.5*labelW} ${0.5*labelW}, ${-1.5*labelW} ${0.5*labelW}, ${-0.5*labelW}`
    
    const x = typeof(val)== "number"? 
        scaleLinear().domain(range as [number, number]).range([0, COL_WIDTH])(val as number):
        scaleBand().domain(range as string[]).range([0, COL_WIDTH])(val as string)
    
    return <>
        <line x1={0} x2={COL_WIDTH} y1={VAL_ROW_HEIGHT} y2={VAL_ROW_HEIGHT} stroke="gray" />
        <polygon transform={`translate(${x}, ${VAL_ROW_HEIGHT})`} points={labelPath} stroke="black"/>
        <text textAnchor="start" x={x!+labelW} y={VAL_ROW_HEIGHT - labelW/2}>{showVarValue(val)}</text>
    </>
}

function OnePDChart ({scores, scaler}: {scores: number[], scaler: ScaleSequential<string>}) {
    const STEP_WIDTH = COL_WIDTH/scores.length
    return <g className="PDChart">
        
        {scores.map((score, i) => (
            <rect key={`var_${i}`} fill={scaler(score)} 
                width={STEP_WIDTH}  height={PD_ROW_HEIGHT}
                x={STEP_WIDTH*i} y={0}
            />
            ))}
        <rect fill="none" stroke="gray" width={COL_WIDTH} height={PD_ROW_HEIGHT} />
    </g>
}

function Legend ({scaler, width=100, height=30, step=20}: {scaler: ScaleSequential<string>, width?: number, height?: number, step?: number}) {
    const step_width = width/step
   
    return <svg width={width} height={height}>
        {  [...Array(step).keys()]
            .map(i => <rect key={i} 
                 fill={scaler(i / (step - 1))} 
                 width={step_width} height={height/3} 
                 transform={`translate(${step_width*i}, 0)`}
                />)}
        <text x={0} y={height-5} textAnchor="start">rej</text>
        <text x={width} y={height-5} textAnchor="end">sup</text>
    </svg>
}