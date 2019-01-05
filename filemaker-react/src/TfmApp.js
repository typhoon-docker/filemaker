import React, { Component } from 'react';
import './TfmApp.css';

import io from 'socket.io-client';
import QuestionTextInput from './QuestionTextInput';
import QuestionSelect from './QuestionSelect';
import QuestionCheckBox from './QuestionCheckBox';

class TfmApp extends Component {
  constructor(props) {
    super(props);

    this.state = {
      dockerfile: [],                      // Displayed Dockerfile
      dockerCompose: null,                 // Displayed docker-compose file
      questions: [],                       // List of all question ids
      questionsData: {},                   // Details for each question, by id
    }

    this.socket = io(process.env.REACT_APP_BACKEND_URL + '/typhoon');

    // When receiving the questions, get their label and data, and fill the state with them
    this.socket.on('questions', msg => {
      const newQuestions = [];
      const newQuestionsData = {};

      JSON.parse(msg.data).forEach(element => {
        newQuestions.push(element.label);
        newQuestionsData[element.label] = element;
      });

      this.setState({questions: newQuestions, questionsData: newQuestionsData});
    });

    // When receiving Dockerfile data, display it
    this.socket.on('dockerfile', msg => this.setState({dockerfile: msg.data}));

    // When receiving docker-compose data, display it
    this.socket.on('docker_compose', msg => this.setState({dockerCompose: msg.data}));
  }

  sendFormToBackend = (validation) => {
    const sendData = this.state.questions.map(label => ({label, answer: this.state.questionsData[label].answer }));
    this.socket.emit('form_changed', {validation, data: sendData});
  }

  changeHandler = event => {
    const name = event.target.name;
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;

    const newQuestionsData = {...this.state.questionsData};
    newQuestionsData[name].answer = value;
    this.setState({questionsData: newQuestionsData});

    this.sendFormToBackend(false);
  }

  sendHandler = event => {
    this.sendFormToBackend(true);
  }

  makeQuestionComponent = qData => {
    if (qData.boolean) {
      return <QuestionCheckBox
        key={qData.label}
        name={qData.label}
        desc={qData.desc}
        info={qData.info}
        value={qData.answer}
        onChange={this.changeHandler}
        />
    }
    else if (qData.choices.length > 0) {
      return <QuestionSelect
        key={qData.label}
        name={qData.label}
        desc={qData.desc}
        info={qData.info}
        value={qData.answer}
        choices={qData.choices}
        onChange={this.changeHandler}
        />
    } else {
      return <QuestionTextInput
        key={qData.label}
        name={qData.label}
        desc={qData.desc}
        info={qData.info}
        value={qData.answer}
        onChange={this.changeHandler}
        />
    }
  }

  makeDockerfileComponents = () => {
    let table = []
    this.state.dockerfile.forEach(df =>
      table.push(
        <div className="TfmApp-file" key={df.image}>
          <h2 className="TfmApp-file-title">Dockerfile {df.image}:</h2>
          <div className="TfmApp-file-content" id="dockerfile">
            <pre>{df.dockerfile}</pre>
          </div>
        </div>
      ));
    return table
  }

  render() {
    return (
      <div className="TfmApp">
        <h1 className="TfmApp-title">Making files for Docker deployment</h1>
        <div className="TfmApp-content">
          {this.state.questions.map(q => {
            const qData = this.state.questionsData[q];

            // If there is parents, the question should be shown only if one of the question+answer parents are chosen
            if (qData.parents.length > 0) {
              let res = null;
              qData.parents.some(qr => {
                let qParent = this.state.questionsData[qr[0]];
                if (qParent !== undefined && qParent.answer === qr[1]) {
                  res = this.makeQuestionComponent(qData);
                  return true;
                }
                return false;
              });
              return res;
            }

            // Else, display the question
            return this.makeQuestionComponent(qData);
          })}
          <input className="TfmApp-send-button" type="submit" value="Send" name="send_button" onClick={this.sendHandler} />

          {this.makeDockerfileComponents()}

          {/* <div className="TfmApp-file">
            <h2 className="TfmApp-file-title">Dockerfile:</h2>
            <div className="TfmApp-file-content" id="dockerfile">
              <pre>{this.state.dockerfile}</pre>
            </div>
          </div> */}

          <div className="TfmApp-file">
            <h2 className="TfmApp-file-title">docker-compose.yml:</h2>
            <div className="TfmApp-file-content" id="docker_compose">
              <pre>{this.state.dockerCompose}</pre>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default TfmApp;
