import React from 'react';

const QuestionCheckBox = props => {
  return (
    <div className="form-group">
      <div className="form-legend">{props.desc}:</div>
      <input className="form-core" type="checkbox" name={props.name} checked={props.value} onChange={props.onChange} />
      <div className="form-info">{props.info}</div>
    </div>
  );
}

export default QuestionCheckBox;
