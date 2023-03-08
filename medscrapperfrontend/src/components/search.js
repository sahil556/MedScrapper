import React, { useEffect, useState } from 'react'
import MedicineState, {MedicineInfo} from '../context/medicinecontext'
import Spinner from './Spinner'
import { ReactSearchAutocomplete } from 'react-search-autocomplete'

function Search(props) {
    const [items, setItems] = useState([])
    const [loading, setLoading] = useState(false)
    const [input, setInput] = useState("");
    let HandleInput = (name) => {
        setInput(name);
        if (name.length == 1) {
            setLoading(true)
            MedicineState(name).then((data) => {
               return JSON.parse(data) 
            }).then(data => {
                for(let i = 0; i < data.length; i++) {
                     data[i].id = i
                }
                setLoading(false)
                setItems(data);  }) 
           
        }
    }

    const handleOnSearch = () => {
        handleOnSelect({"name":input})
    }

    const handleOnHover = (result) => {
        
        // the item hovered
        console.log(result)
    }
    
    const handleOnSelect = (item) => {
        if (item.name.length > 1) {
        props.setLoadingMedicine(true)

            let str = item.name;
            // console.log(str)
            MedicineInfo(item.name, '1mg').then((str) => {
                return JSON.parse(str)
            }).then(data => {
                // console.log(data)
              props.setMedicines1mg(data)
              
            })
            
            MedicineInfo(item.name, 'netmeds').then((str) => {
              return JSON.parse(str)
            }).then(data => {
                // console.log(data)
              props.setMedicinesnm(data)
              
            })

            MedicineInfo(item.name, 'pharmeasy').then((str) => {
                return JSON.parse(str)
              }).then(data => {
                // console.log(data)
                props.setMedicinespe(data)
            props.setLoadingMedicine(false)
                
            })
          }
        //   console.log(item)
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
        
        <div className="App d-flex p-4 justify-content-center" style={{position:'relative'}} >
            {/* <header className="App-header"> */}
                <div style={{ width: 400, position:'absolute', zIndex:1}} >
                    <ReactSearchAutocomplete
                        items={items}
                        onSearch={HandleInput} 
                        autoFocus
                        formatResult={formatResult}
                    />
                </div>
                <div style={{ width: 400, position:'absolute', zIndex:1, marginTop:'5px', marginLeft:'500px'}}>
                    <button className='btn btn-dark' data-toggle="modal" data-target="#exampleModalLong" onClick={handleOnSearch}>search</button>
                </div>
            {/* </header> */}
            
        </div>
        
        {loading && <Spinner />}
        </>
    )
}

export default Search