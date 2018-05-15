import React, { Component } from 'react'
import PropTypes from 'prop-types'

class CreateItem extends Component {
  state = {
    title: '',
    desc: '',
    tried: false
  }

  handleChange = e => {
    const target = e.target
    this.setState({ [target.name]: target.value })
  }
  handleKeyPress = e => {
    if (e.key === 'Enter') {
      this.setState({ tried: true })
      if (this.state.title && this.state.desc) {
        this.props.addItem(this)
        this.setState({ tried: false })
      }
    }
  }

  render() {
    return (
      <tr>
        <td>new</td>
        <td>
          <input
            name="title"
            onChange={this.handleChange}
            onKeyPress={this.handleKeyPress}
            className={!this.state.title && this.state.tried ? 'empty' : ''}
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
            name="desc"
            onChange={this.handleChange}
            onKeyPress={this.handleKeyPress}
            className={!this.state.desc && this.state.tried ? 'empty' : ''}
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

CreateItem.propTypes = {
  addItem: PropTypes.func
}
export default CreateItem
