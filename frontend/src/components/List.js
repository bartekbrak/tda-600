import React from 'react'
import Row from './Row'
import CreateItem from './CreateItem'
import PropTypes from 'prop-types'

const List = props => {
  const rows = []
  props.items.forEach(item => {
    rows.push(
      <Row
        id={item.id}
        key={item.id}
        title={item.title}
        desc={item.desc}
        status={item.status}
        deleteItem={props.deleteItem}
        patchItem={props.patchItem}
      />
    )
  })
  return (
    <table>
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
        <CreateItem addItem={props.addItem} />
      </tbody>
    </table>
  )
}

List.propTypes = {
  items: PropTypes.array,
  deleteItem: PropTypes.func,
  patchItem: PropTypes.func,
  addItem: PropTypes.func
}

export default List
