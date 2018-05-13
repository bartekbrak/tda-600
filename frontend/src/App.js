/* eslint-disable react/prop-types */
import React, { Component } from 'react'
import logo from './cog.svg'
import './App.css'
import axios from 'axios'

const ITEMS = '/items/'

let baseURL = 'http://localhost:8000'
// in future, this might be the address of the API, not just yet
//if (process.env.NODE_ENV === 'production') {
//  baseURL = `https://api.${window &&
//    window.location &&
//    window.location.hostname}`
//}

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json'
  }
})

class CreateTask extends Component {
  constructor(props) {
    super(props)
    this.state = { title: '', desc: '' }
  }

  handleChange = e => {
    const target = e.target
    this.setState({ [target.id]: target.value })
  }
  handleKeyPress = e => {
    if (e.key === 'Enter') {
      let title = document.getElementById('title')
      let desc = document.getElementById('desc')
      if (this.state.title && this.state.desc) {
        this.props.addItem(this)
        title.classList.remove('invalid')
        desc.classList.remove('invalid')
      } else {
        if (!this.state.title) {
          title.classList.add('invalid')
        }
        if (!this.state.desc) {
          desc.classList.add('invalid')
        }
      }
    }
  }

  render() {
    return (
      <tr>
        <td>new</td>
        <td>
          <input
            id="title"
            onChange={this.handleChange}
            onKeyPress={this.handleKeyPress}
            type="text"
            placeholder="title"
            value={this.state.title}
            required
            pattern=".{3,}"
            autoFocus
          />
        </td>
        <td>
          <input
            id="desc"
            onChange={this.handleChange}
            onKeyPress={this.handleKeyPress}
            value={this.state.desc}
            required
            pattern=".{3,}"
            type="text"
            placeholder="Add new task description here and press Enter."
          />
        </td>
        <td>-</td>
      </tr>
    )
  }
}

class Row extends React.Component {
  render() {
    return (
      <tr id={this.props.id}>
        <td className="delete" onClick={this.deleteItem}>
          {this.props.id}
        </td>
        <td>{this.props.title}</td>
        <td onClick={this.editDesc}>{this.props.desc}</td>
        <td
          className={this.props.status === 'pending' ? 'complete' : 'undo'}
          onClick={
            this.props.status === 'pending' ? this.completeItem : this.undoItem
          }
        >
          {this.props.status}
        </td>
      </tr>
    )
  }
  editDesc = () => {}
  deleteItem = () => {
    this.props.deleteItem(this.props.id)
  }
  completeItem = () => {
    this.props.patchItem(this.props.id, 'done')
  }
  undoItem = () => {
    this.props.patchItem(this.props.id, 'pending')
  }
}

class List extends React.Component {
  render() {
    if (this.props.items && this.props.items.length) {
      const rows = []
      this.props.items.forEach(item => {
        rows.push(
          <Row
            id={item.id}
            title={item.title}
            desc={item.desc}
            status={item.status}
            deleteItem={this.props.deleteItem}
            patchItem={this.props.patchItem}
          />
        )
      })
      return (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>id</th>
              <th>title</th>
              <th>desc</th>
              <th>status</th>
            </tr>
          </thead>
          <tbody>
            {rows}
            <CreateTask addItem={this.props.addItem} new={this.props.new} />
          </tbody>
        </table>
      )
    } else {
      return <p>loading...</p>
    }
  }
}

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      items: [],
      new: {}
    }
  }

  componentDidMount() {
    api.get(ITEMS).then(result => {
      this.setState({
        items: result.data.items
      })
    })
  }

  componentWillUnmount() {
    this.serverRequest.abort()
  }

  addItem = child => {
    api
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
    api.delete(ITEMS + id).then(result => {
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
    api.patch(ITEMS + id, { status: status }).then(result => {
      this.changeStatus(id, status)
    })
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to tda-600.</h1>
          <div>A simple to-do app.</div>
        </header>
        click on ID to deleteItem, click on status to complete
        <List
          deleteItem={this.deleteItem}
          patchItem={this.patchItem}
          addItem={this.addItem}
          new={this.state.new}
          items={this.state.items}
        />
      </div>
    )
  }
}

export default App
