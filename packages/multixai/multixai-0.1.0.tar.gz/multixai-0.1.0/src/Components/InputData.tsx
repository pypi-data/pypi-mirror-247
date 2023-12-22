import React from 'react'
import { useExp } from "src/Context/ExpContext"
import { showVarValue } from 'src/helpers/helpers';

function InputData() {
  const { exp} = useExp();
  const dataType = exp['input_data']['type']

  const content = dataType === 'tabular'?
  (exp.input_data.headers ).map((header, i) => header + ': ' + showVarValue(exp.input_data.value[i])).join(', ')
  : dataType === 'image'?
  [<img src={exp['input_data']['value'] as string} alt="input_img"/>]:
  <span>{exp['input_data']['value']}</span>

  return (
  <div className='input_data block' style={{color:"black"}}>
    <span className='label left'>Input Data Point: </span>
    <div className='right' style={dataType!='image'?{maxHeight: '100px', overflowY: 'scroll'}: {}}>
      {content}
      </div>
   </div>
  )
}

export default InputData
