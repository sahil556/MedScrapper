import React, { useState } from 'react'
import MedicineState from '../context/medicinecontext'

import { ReactSearchAutocomplete } from 'react-search-autocomplete'

function Test() {
    // note: the id field is mandatory
    const [items, setItems] = useState([])
    
  
    let HandleInput = (name) => {
        
        if (name.length == 1) {
            MedicineState(name).then((data) => {
               return JSON.parse(data) 
            }).then(data => {
                for(let i = 0; i < data.length; i++) {
                     data[i].id = i
                }
                setItems(data); console.log(data) }) 
           
        }
    }

    const handleOnSearch = (string, results) => {
        // onSearch will have as the first callback parameter
        // the string searched and for the second the results.
        // console.log(string)
        // if (string.length == 1) {
        //     MedicineState(string).then((data) => {
        //         items = data
        //         console.log(items)
        //     })
        // }
        // console.log(string, results)
    }

    const handleOnHover = (result) => {
        // the item hovered
        console.log(result)
    }

    const handleOnSelect = (item) => {
        
        console.log(item)
    }

    const handleOnFocus = () => {
        console.log('Focused')
    }

    const formatResult = (item) => {
        return (
            <>
                <span key={item.id} style={{ display: 'block', textAlign: 'left' }}>{item.name}</span>
            </>
        )
    }

    return (
        <div className="App">
            <header className="App-header">
                <div style={{ width: 400 }}>
                    <ReactSearchAutocomplete
                        items={items}
                        onSearch={HandleInput}
                        // onHover={handleOnHover}
                        onSelect={handleOnSelect}
                        // onFocus={handleOnFocus}
                        autoFocus
                        formatResult={formatResult}
                    />
                </div>
            </header>
        </div>
    )
}

export default Test