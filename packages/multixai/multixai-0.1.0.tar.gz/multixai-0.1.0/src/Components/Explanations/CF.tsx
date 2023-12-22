import React from "react";
import { useExp } from "src/Context/ExpContext";
import { COL_WIDTH, CF_ROW_GAP, COL_GAP, CF_ROW_HEIGHT } from "src/Const";
import {scaleLinear, scaleBand, ScaleBand, ScaleLinear} from 'd3-scale'
import { CfExplanation } from "src/Types/types";

const MARKER_SIZE = 8

export default function Partial_Dependency() {
    const {exp} = useExp();
    if (! exp['explanations']['cf']) return null
    
    const {ranges, values} = exp['independent_vars']
    const cfGroups = exp['explanations']['cf']

    const XScalerArray = ranges.map((range, i) => 
        typeof(range[0])== "number"? 
            scaleLinear().domain(range as number[]).range([0, COL_WIDTH]): 
            scaleBand().domain(range as string[]).range([0, COL_WIDTH])
    )

    const HeaderHeight = CF_ROW_HEIGHT * 0.8
    let groupStartY = 0
    const vis = cfGroups.map((model:CfExplanation) => {
        const name = model['name']
        const cfExamples = model['delta']
        const groupContent = (
            <g key={name} transform={ `translate(0, ${groupStartY})`}> 
            <text textAnchor="start" y= {HeaderHeight}>{name}</text>
                {cfExamples.map((deltas, row_index) => { 
                    return <g key={`row_${row_index}`} className={`row_${row_index}`} transform={`translate(0,${(CF_ROW_HEIGHT + CF_ROW_GAP)*row_index + HeaderHeight + CF_ROW_GAP})`}>
                        <rect 
                            className="cf_row_background"
                            width={values.length * (COL_GAP+COL_WIDTH)} height={CF_ROW_HEIGHT } y={ 0 } fill="#eee" />
                        {deltas.map(
                            (delta, var_index) => (
                                <g key={`var_${var_index}`} transform={`translate(${(COL_WIDTH+COL_GAP)*var_index},0)`}> 
                                    {typeof(delta) === "number"?
                                    <OneNumberChart orginal={values[var_index] as number} delta={delta as number} scaler={XScalerArray[var_index] as ScaleLinear<number, number, never>}/>
                                    :<OneStringChart orginal={values[var_index] as string}  delta={delta } scaler={XScalerArray[var_index] as ScaleBand<string>}/>
                                }
                                </g>))}
                    </g>})
                }
            </g>
            )
        groupStartY += (CF_ROW_HEIGHT + CF_ROW_GAP)* cfExamples.length + HeaderHeight + CF_ROW_GAP

        return groupContent
    })

   
    return <div className="block">
        <div className="left">
            <span className="label">Counterfactuals</span>
        </div>
        <div className="right">
            <svg width={(COL_WIDTH + COL_GAP)* values.length} height={groupStartY }>
                <defs>
                    <marker id="arrowhead" markerWidth={MARKER_SIZE} markerHeight={MARKER_SIZE} 
                    refX={MARKER_SIZE} refY={MARKER_SIZE/2} orient="auto">
                        <polyline points={`0 0, ${MARKER_SIZE} ${MARKER_SIZE/2}, 0 ${MARKER_SIZE}`} fill="none" stroke="black"/>
                    {/* <polygon points={`0 0, ${MARKER_SIZE} ${MARKER_SIZE/2}, 0 ${MARKER_SIZE}`} /> */}
                    </marker>
                </defs>
                {vis}
            </svg>
        </div> 
    </div>
}

function OneNumberChart ({orginal, delta, scaler}: {orginal: number, delta: number, scaler: ScaleLinear<number, number, never>}) {
    if (delta === 0 ) return null

    const xStart = scaler(orginal), xEnd = scaler(orginal +  delta)

    return <>
        <rect 
            className='background' 
                x={ 0} 
                y={0}
                width={COL_WIDTH} 
                height={CF_ROW_HEIGHT} 
                 fill="white"
                opacity="1"
                stroke="lightgray"
            />
        <line x1={xStart} x2={xEnd} y1={CF_ROW_HEIGHT - MARKER_SIZE/2} y2={CF_ROW_HEIGHT-MARKER_SIZE/2} stroke="gray" marker-end="url(#arrowhead)"/>
        <text textAnchor="middle" x={scaler(orginal+delta/2)} y={CF_ROW_HEIGHT - MARKER_SIZE}>{ (delta>0?'+':'') + String(delta)}</text>
    </>
}

function OneStringChart ({orginal, delta, scaler}: {orginal: string, delta: string, scaler: ScaleBand<string>}) {
    if (delta === '' ) return null

    return <>
        <rect 
            className='background' 
                x={ 0} 
                y={0}
                width={COL_WIDTH} 
                height={CF_ROW_HEIGHT} 
                 fill="white"
                opacity="1"
                stroke="gray"
            />
        <line x1={scaler(orginal)} x2={scaler(delta)} y1={CF_ROW_HEIGHT  - MARKER_SIZE/2 } y2={CF_ROW_HEIGHT  - MARKER_SIZE/2} stroke="gray" marker-end="url(#arrowhead)"/>
        <text textAnchor="middle" x={scaler(delta)} y={CF_ROW_HEIGHT -  - MARKER_SIZE}>{ delta }</text>
    </>
}