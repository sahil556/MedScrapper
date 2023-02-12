import React, { useState } from 'react'
import MedicineState from '../context/medicinecontext'
import { ReactSearchAutocomplete } from 'react-search-autocomplete'

export default function Search() {
    const [responseStatus, setResponseStatus] = useState(false)

    const HandleInput = (e)=>{
        console.log(e.target.value)
        MedicineState(e.target.value).then((data)=>{
            console.log(data)
        })
    }
    
    return (
        <>
       
        
            {/* <div>
                <h1>pharmeasy scrapping request : </h1>
                <form action="http://127.0.0.1:8000/pharmeasy" method="post">
                    <input autoComplete='off' type="text" onChange={HandleInput} name="name" placeholder="Enter medicine name" />
                    <button type="submit">submit</button>
                </form>
                <br /><br />
                <hr />
                <br />
                <h1>netmeds scrapping request : </h1>
                <form action="http://127.0.0.1:8000/netmeds" method="post">
                    <input type="text" name="name" placeholder="Enter medicine name" />
                    <button type="submit">submit</button>
                </form>
            </div> */}
        </>
    )
}
