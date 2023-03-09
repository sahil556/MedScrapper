import React, { useEffect, useState } from 'react'
import MedicineState, { MedicineInfo } from '../context/medicinecontext'
import Spinner from './Spinner'
import { ReactSearchAutocomplete } from 'react-search-autocomplete'

function Search(props) {
    const [items, setItems] = useState([])
    const [loading, setLoading] = useState(false)
    const [input, setInput] = useState("");
    const [searchby, setSearchBy] = useState("name")
    const [selected, setSelected] = useState(false);
    const [company, setCompany]  = useState("");


    const toggleSwitch = () => {
        setItems([])
        if(searchby == "name" )
            setSearchBy("content")
        else
            setSearchBy("name")
    }

    let HandleInput = (name) => {
        setInput(name);
        if (name.length == 1 || (name.length > 1 && searchby == "content")) {
            
            setLoading(true)
            // api call to fetch seacrh suggestion
            MedicineState(name, searchby).then((data) => {
                return JSON.parse(data)
            }).then(data => {
                if(searchby == "content")
                {
                    let listitem = []
                    for (let i = 0; i < data.length; i++) {
                        listitem.push({"name": data[i], "id":i})
                    }
                    setItems(listitem)
                }
                else
                {
                for (let i = 0; i < data.length; i++) {
                    data[i].id = i
                }
                setItems(data);
                }
            })
            setLoading(false)


        }
    }

    const handleOnSearch = () => {
        console.log(input)
        handleOnSelect({ "name": input, "searchby" : searchby, "comapny": company})
    }

    const selectedfromsuggestion = (e) =>{
        setCompany(e.company)
        setSelected(true);
        console.log("selected from suggestion")
    }

    const handleOnHover = (result) => {

        // the item hovered
        console.log(result)
    }

    const handleOnSelect = (item) => {
        console.log(item)
        console.log(selected)
        if (item.name.length > 1) {
            props.setLoadingMedicine(true)
            let str = item.name;
            console.log(str)
            if(selected)
            {
                let comapnylist
                if(item.comapny == "pharmeasy")
                    comapnylist = ["netmeds", "1mg"]
                else if(item.comapny == "netmeds")
                    comapnylist = ["pharmeasy, 1mg"]
                else
                    comapnylist = ["netmeds", "pharmeasy"]
                
                console.log(comapnylist)

                MedicineInfo(item.name, item.comapny, selected).then((str) => {
                    return JSON.parse(str)
                }).then(data => {
                    props.setMedicines1mg(data)
                })

                // salt synonym request
                let saltsynonymlist = []
                MedicineState(item.name, searchby, company).then((data) => {
                    return JSON.parse(data)
                }).then(data => {
                    if(searchby == "content")
                    {
                        saltsynonymlist = data
                    }
                    else
                    {
                        for (let i = 0; i < data.length; i++) {
                        saltsynonymlist.push(data[i].name)
                    } 
                    }
                })
                console.log("salt synonym list")
                console.log(saltsynonymlist)

            }
            else
            {

            MedicineInfo(item.name, '1mg').then((str) => {
                return JSON.parse(str)
            }).then(data => {
                props.setMedicines1mg(data)
            })

            MedicineInfo(item.name, 'netmeds').then((str) => {
                return JSON.parse(str)
            }).then(data => {
                // props.setMedicinesnm(data)

            })

            MedicineInfo(item.name, 'pharmeasy').then((str) => {
                return JSON.parse(str)
            }).then(data => {
                props.setMedicinespe(data)
                props.setLoadingMedicine(false)

            })
            }
        }
        console.log(item)
    }

    const handleOnFocus = () => {
        console.log('Focused')
    }

    const formatResult = (item) => {
        return (
            <>
                <span key={item.id} style={{ textAlign: 'left' }}>{item.name}</span>
            </>
        )
    }

    return (
        <>

            <div className="App d-flex p-4 justify-content-center" style={{ position: 'relative' }} >
                <div style={{ width: 400, position: 'absolute', zIndex: 1, marginTop: '7px', marginLeft:'-100px' }}>
                    <div className="form-check form-switch" style={{"height": "2rem", "width":"calc(3rem + 0.75rem)"}}>
                        <input className="form-check-input" type="checkbox" role="switch" onClick={toggleSwitch} id="flexSwitchCheckDefault" />
                    </div>
                </div>
                <div style={{ width: 400, position: 'absolute', zIndex: 1 }} >
                    <ReactSearchAutocomplete
                        items={items}
                        onSearch={HandleInput}
                        autoFocus
                        onSelect={selectedfromsuggestion}
                        formatResult={formatResult}
                        placeholder={"search by medicine " +searchby}
                    />
                </div>
                <div style={{ width: 400, position: 'absolute', zIndex: 1, marginTop: '5px', marginLeft: '500px' }}>
                    <button className='btn btn-dark' data-toggle="modal" data-target="#exampleModalLong" onClick={handleOnSearch}>search</button>
                </div>
                {/* </header> */}

            </div>

            {loading && <Spinner />}
        </>
    )
}

export default Search