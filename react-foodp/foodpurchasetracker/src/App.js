import logo from './logo.svg';
import './App.css';
import React from 'react'
import ReactDOM from 'react-dom'
 
class MainComponent extends React.Component{
  constructor(props){
    super(props)
    this.state={stores:["Aldi","Rewe"]}
  }
  render(){
    return (<h1>{this.state.stores.map(store=>{return <h1>{store}</h1>})}</h1>)    
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React 
    <MainComponent/> 
        </a>
      </header>
    </div>
  );
}

export default App;
