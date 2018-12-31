import React from 'react';

const QuestionTextInput = props => {
  return (
    <div className="form-group">
      <div className="form-legend">{props.desc}:</div>
      <input className="form-core" type="text" value={props.value} name={props.name} onChange={props.onChange} />
      <div className="form-info">{props.info}</div>
    </div>
  );
}

export default QuestionTextInput;
