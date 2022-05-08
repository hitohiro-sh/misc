// Hooks API

import React from 'react'
import './App.css';


function Button(props) {
  return (<button onClick={props.onClick}>{props.label}</button>)
}

function App() {
  const [msg, setMsg] = React.useState('');

  return (
    <div className="App">
      <header className="App-header">
        <Button onClick={() => {setMsg('clicked!')}} label="Button" />
        <p>"{msg}"</p>
      </header>
    </div>
  );

}

export default App;
