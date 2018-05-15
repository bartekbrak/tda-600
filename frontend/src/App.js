/* eslint-disable react/prop-types */
import React, { Component } from 'react'
import logo from './static/cog.svg'
import './static/App.css'
import List from './components/List'
import axios from 'axios'

const ITEMS = '/items/'

class App extends Component {
  state = {
    items: []
  }

  addItem = child => {
    axios
      .post(ITEMS, {
        desc: child.state.desc,
        title: child.state.title,
        status: 'pending'
      })
      .then(result => {
        child.setState({ title: '', desc: '' })
        this.setState(prevState => ({
          items: [...prevState.items, result.data.item]
        }))
      })
  }
  deleteItem = id => {
    axios.delete(ITEMS + id).then(result => {
      this.setState(prevState => ({
        items: prevState.items.filter(el => el.id !== id)
      }))
    })
  }
  changeStatus = (id, status) => {
    let items = this.state.items
    let objIndex = this.state.items.findIndex(obj => obj.id === id)
    items[objIndex].status = status
    this.setState({ items: items })
  }
  patchItem = (id, status) => {
    axios.patch(ITEMS + id, { status: status }).then(result => {
      this.changeStatus(id, status)
    })
  }

  componentDidMount() {
    axios.get(ITEMS).then(result => {
      this.setState({
        items: result.data.items
      })
    })
  }

  componentWillUnmount() {
    this.serverRequest.abort()
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="" />
          <h1 className="App-title">Welcome to tda-600.</h1>
          <div>click on ID to deleteItem, click on status to complete</div>
        </header>

        <List
          deleteItem={this.deleteItem}
          patchItem={this.patchItem}
          addItem={this.addItem}
          items={this.state.items}
        />
      </div>
    )
  }
}

export default App
