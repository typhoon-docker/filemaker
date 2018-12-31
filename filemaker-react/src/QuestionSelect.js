import React from 'react';

const QuestionSelect = props => {
  return (
    <div className="form-group">
      <div className="form-legend">{props.desc}:</div>
      <select className="form-core" name={props.name} value={props.value} onChange={props.onChange}>
        {props.choices.map(option => (
          <option key={option}>{option}</option>
        ))}
      </select>
      <div className="form-info">{props.info}</div>
    </div>
  );
}

export default QuestionSelect;
