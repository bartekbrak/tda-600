import React from 'react'
import PropTypes from 'prop-types'

const Row = props => {
  const editDesc = () => {}
  const deleteItem = () => {
    props.deleteItem(props.id)
  }
  const completeItem = () => {
    props.patchItem(props.id, 'done')
  }
  const undoItem = () => {
    props.patchItem(props.id, 'pending')
  }

  return (
    <tr id={props.id}>
      <td className="delete" onClick={deleteItem}>
        {props.id}
      </td>
      <td>{props.title}</td>
      <td onClick={editDesc}>{props.desc}</td>
      <td
        className={props.status === 'pending' ? 'complete' : 'undo'}
        onClick={props.status === 'pending' ? completeItem : undoItem}
      >
        {props.status}
      </td>
    </tr>
  )
}

Row.propTypes = {
  deleteItem: PropTypes.func,
  patchItem: PropTypes.func,
  title: PropTypes.string,
  desc: PropTypes.string,
  status: PropTypes.string,
  id: PropTypes.number
}
export default Row
