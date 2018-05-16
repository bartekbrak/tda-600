import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { debounce } from 'throttle-debounce'

export default class Row extends Component {
  state = {
    lastHTML: undefined
  }
  deleteItem = () => {
    this.props.deleteItem(this.props.id)
  }
  completeItem = () => {
    this.props.patchItem(this.props.id, 'status', 'done')
  }
  undoItem = () => {
    this.props.patchItem(this.props.id, 'status', 'pending')
  }
  // https://stackoverflow.com/a/22678516/1472229
  debounceOnChange = debounce(1000, (target, id, key, value) => {
    // TODO: when empty, field can't be sent but this is not indicated
    if (target && target.innerHTML) {
      let newHTML = target.innerHTML
      if (newHTML !== this.state.lastHTML) {
        this.props.patchItem(id, key, value)
        this.setState({ lastHTML: newHTML })
      }
    }
  })
  onChange = e => {
    this.debounceOnChange(
      e.target,
      this.props.id,
      e.target.attributes.getNamedItem('data-name').value,
      e.target.innerHTML
    )
  }
  render() {
    return (
      <tr>
        <td className="delete" onClick={this.deleteItem}>
          {this.props.id}
        </td>
        <td contentEditable onInput={this.onChange} data-name="title">
          {this.props.title}
        </td>
        <td contentEditable onInput={this.onChange} data-name="desc">
          {this.props.desc}
        </td>
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
}

Row.propTypes = {
  deleteItem: PropTypes.func,
  patchItem: PropTypes.func,
  title: PropTypes.string,
  desc: PropTypes.string,
  status: PropTypes.string,
  id: PropTypes.number
}
