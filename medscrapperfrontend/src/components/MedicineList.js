import React from 'react'
import Medicine from './Medicine'

export default function MedicineList(props) {
  console.log(props.medicines)
  return (
    <div>
      {/* <Medicine item={{ "name": "shil" }} /> */}
      {/* {props.medicines.map((item) => {
        <Medicine item={item} />
      })} */}
    </div>
  )
}
