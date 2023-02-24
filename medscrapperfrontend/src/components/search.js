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
                setItems(data);  }) 
           
        }
    }

    const handleOnSearch = (string, results) => {
        console.log("seaced")
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
            let str = "";
            for(let i=0; i<item.name.length; i++)
            {
                if(item.name[i] == ' ')
                break;
                str += item.name[i];
            }
            console.log(str)
            MedicineInfo(item.name, '1mg').then((str) => {
                return JSON.parse(str)
              }).then(data => {
                props.setMedicines1mg(data)
                
              })
            
            MedicineInfo(item.name, 'netmeds').then((str) => {
              return JSON.parse(str)
            }).then(data => {
              props.setMedicinesnm(data)
              
            })

            MedicineInfo(item.name, 'pharmeasy').then((str) => {
                return JSON.parse(str)
              }).then(data => {
                props.setMedicinespe(data)
                
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
        <div className="App d-flex p-4 justify-content-center" style={{position:'relative'}} >
            {/* <header className="App-header"> */}
                <div style={{ width: 400, position:'absolute', zIndex:1}} >
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