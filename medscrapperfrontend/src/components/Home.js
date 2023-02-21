import React, { useState } from 'react'
import MedicineList from './MedicineList'
import Search from './Search'
import Spinner from './Spinner'
import { MedicineInfo } from '../context/medicinecontext'
import Medicine from './Medicine'

export default function Home() {
  const [medicines, setMedicines] = useState([])
  var medicines_temp ;
  if (medicines.length > 0) {
    console.log("yes greater")
    console.log(medicines)
    medicines_temp = medicines.map(x => <Medicine item={x} />)
  }
  return (
    <div>
      <Search setMedicines={setMedicines}/>
      { medicines_temp}   
         
    </div>
  )
}

