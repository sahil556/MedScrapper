import React, { useState } from 'react'
import MedicineList from './MedicineList'
import Search from './Search'
import Spinner from './Spinner'
import { MedicineInfo } from '../context/medicinecontext'
import Medicine from './Medicine'

export default function Home() {
  const [medicines, setMedicines] = useState([])
  if (medicines.length > 0) {
    console.log("yes greater")
    console.log(medicines)
  }
  return (
    <div>
      <Search/>
      {medicines.length > 0 &&
        medicines.map((item)=>{
          <Medicine item={item}/>
        })}      
    </div>
  )
}

