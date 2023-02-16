import React, { useEffect, useState } from 'react'
import MedicineState, {MedicineInfo} from '../context/medicinecontext'
import Spinner from './Spinner'
import { ReactSearchAutocomplete } from 'react-search-autocomplete'

function Search(props) {
    const [items, setItems] = useState([])
    const [loading, setLoading] = useState(false)
    
    let HandleInput = (name) => {
        
        if (name.length == 1) {
            setLoading(true)
            MedicineState(name).then((data) => {
               return JSON.parse(data) 
            }).then(data => {
                for(let i = 0; i < data.length; i++) {
                     data[i].id = i
                }
                setLoading(false)
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
        console.log(item.name.length)
        if (item.name.length > 1) {
            MedicineInfo(item.name, 'pharmeasy').then((data) => {
              return JSON.parse(data)
            }).then(data => {
              props.setMedicines(data)
            })
          }
        console.log(item)
    }

    const handleOnFocus = () => {
        console.log('Focused')
    }

    const formatResult = (item) => {
        return (
            <>
                <span key={item.id} style={{ textAlign: 'left'}}>{item.name}</span>
            </>
        )
    }
    
    return (
        <>
        <div className="App d-flex p-4 justify-content-center" >
            {/* <header className="App-header"> */}
                <div style={{ width: 400 }} >
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
            {/* </header> */}
            
        </div>
        {loading && <Spinner />}
        </>
    )
}

export default Search