import React, { Component } from 'react'
import PropTypes from 'prop-types'

class CreateItem extends Component {
  state = {
    title: '',
    desc: '',
    submitted: false
  }

  handleChange = e => {
    const target = e.target
    this.setState({ [target.name]: target.value })
  }
  handleKeyPress = e => {
    if (e.key === 'Enter') {
      this.setState({ submitted: true })
      if (this.state.title && this.state.desc) {
        this.props.addItem(this)
        this.setState({ submitted: false })
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
            className={!this.state.title && this.state.submitted ? 'empty' : ''}
            type="text"
            placeholder="title"
            value={this.state.title}
            required
            pattern=".{3,}"
            autoFocus
            tabIndex="1"
          />
        </td>
        <td>
          <input
            name="desc"
            onChange={this.handleChange}
            onKeyPress={this.handleKeyPress}
            className={!this.state.desc && this.state.submitted ? 'empty' : ''}
            value={this.state.desc}
            required
            pattern=".{3,}"
            type="text"
            placeholder="Add new task description here and press Enter."
            tabIndex="2"
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
