/* eslint-disable react/prop-types */
import React, { Component } from 'react'
import logo from './static/cog.svg'
import './static/App.css'
import List from './components/List'
import { ITEMS, api } from './services/api'

class App extends Component {
  state = {
    items: [],
    last_api_msg: '-'
  }

  addItem = child => {
    api
      .post(ITEMS, {
        desc: child.state.desc,
        title: child.state.title
      })
      .then(result => {
        child.setState({ title: '', desc: '' })
        this.setState(prevState => ({
          items: [...prevState.items, result.data.item]
        }))
        window.scrollBy(0, 100)
        this.setState({ last_api_msg: `Added item no ${result.data.item.id}.` })
      })
  }
  deleteItem = id => {
    api.delete(ITEMS + id).then(result => {
      this.setState(prevState => ({
        items: prevState.items.filter(el => el.id !== id)
      }))
      this.setState({ last_api_msg: `Deleted item no f{id}.` })
    })
  }
  changeStatus = (id, key, value) => {
    let items = this.state.items
    let objIndex = this.state.items.findIndex(obj => obj.id === id)
    items[objIndex][key] = value
    this.setState({
      items: items,
      last_api_msg: `Changed ${key} of item no ${id}.`
    })
  }
  patchItem = (id, key, value) => {
    api.patch(ITEMS + id, { [key]: value }).then(result => {
      this.changeStatus(id, key, value)
    })
  }

  componentDidMount() {
    api.get(ITEMS).then(result => {
      this.setState({
        items: result.data.items
      })
      this.setState({
        last_api_msg: `Loaded ${result.data.items.length} items.`
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
          <div>
            click on <b>id</b> to deleteItem, click on <b>status</b> to
            complete,<br />
            click on either <b>title</b> or <b>description</b> to edit<br />
            or on the last row to add new entry<br />
            <br />
            last api action: {this.state.last_api_msg}
          </div>
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
