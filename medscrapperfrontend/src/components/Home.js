import React, { useState, useRef } from 'react'
import Search from './Search'
import { addSubscription } from '../context/medicinecontext'
import MedicineDisplay from './MedicineDisplay'
import TobeDisplayed from './TobeDisplayed'


export default function Home() {
  const [medicines1mg, setMedicines1mg] = useState([])
  const [medicinespe, setMedicinespe] = useState([])
  const [medicinesnm, setMedicinesnm] = useState([])
  const [loadingMedicine, setLoadingMedicine] = useState(false)

  const ref = useRef(null)
  const regexExp = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/gi;
  const refClose = useRef(null)
  const [subscription, setSubsciption] = useState({ medicine_name: "", email: "", website_name: "" })
  const Notifyme = (currentMedicine) => {
    console.log(currentMedicine)
    ref.current.click();
    setSubsciption({ medicine_name: currentMedicine.name, email: "", website_name: currentMedicine.website_name })
  }


  const handleClick = (e) => {
    console.log(subscription.email, subscription.medicine_name, subscription.website_name)
    console.log(subscription)
    addSubscription(subscription)
    setSubsciption({ medicine_name: e.name, email: e.email, website_name: e.website_name });
    refClose.current.click();
    alert("Subscription successful !")
  }

  const onChange = (e) => {
    setSubsciption({ ...subscription, [e.target.name]: e.target.value })

  }

  // console.log("object")
  let medicine_list_1mg, medicine_list_nm, medicine_list_pe
  try {
    if (medicines1mg != null) {
      if (medicines1mg.length > 0 ) {
        medicine_list_1mg = medicines1mg.map((item) => {
          item.website_name = '1mg'
          return <MedicineDisplay key={item.id} item={item} Notifyme={Notifyme} />
        })
      }
    }
  }
  catch (e) {
    console.log(e)
  }
  if (medicinespe.length > 0) {
    // console.log(medicinespe)
    medicine_list_pe = medicinespe.map((item) => {
      item.website_name = 'pharmeasy'
      return <MedicineDisplay item={item} Notifyme={Notifyme} />
    })
  }


  if (medicinesnm.length > 0) {
    medicine_list_nm = medicinesnm.map((item) => {
      item.website_name = 'netmeds'
      return <MedicineDisplay item={item} Notifyme={Notifyme} />
    })
  }


  return (
    <div>

      <Search  setMedicinespe={setMedicinespe} setMedicines1mg={setMedicines1mg} setMedicinesnm={setMedicinesnm} setLoadingMedicine={setLoadingMedicine} style={{ zIndex: 10 }} />

      <button ref={ref} type="button" className="btn btn-primary d-none" data-bs-toggle="modal" data-bs-target="#exampleModalCenter">
        Launch demo modal
      </button>

      <div className="modal fade" id="exampleModalCenter" tabIndex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
        <div className="modal-dialog modal-dialog-centered" role="document">
          <div className="modal-content bg-dark">
            <div className="modal-header text-white">
              <h5 className="modal-title text-white" id="exampleModalLabel">Notify Me</h5>
              {/* <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button> */}
            </div>
            <div className="modal-body">
              <form className="my-2">
                <div className="mb-2">
                  <label htmlFor="medicine" className="form-label text-white ">Medicine Name: </label>
                  <input disabled={true} type="text" className="form-control" id="emedicine" name="emedicine" value={subscription.medicine_name} aria-describedby="emailHelp" onChange={onChange} minLength={5} required />
                </div>

                <div className="mb-2">
                  <label htmlFor="email" className="form-label text-white">Your Email: </label>
                  <input type="email" className="form-control" id="email" name="email" value={subscription.email} onChange={onChange} />
                </div>
                <div className='mb-1'>
                  <p style={{ color: 'yellow', display: subscription.email != undefined && subscription.email.length > 1 && subscription.email.includes('@') && subscription.email.includes('.') ? 'none' : 'block' }}>Please Enter a Valid Email !</p>
                </div>

              </form>
            </div>
            <div className="modal-footer">
              <button ref={refClose} type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button disabled={!(subscription.email != undefined && subscription.email.length > 5 && regexExp.test(subscription.email))} onClick={handleClick} type="button" className="btn btn-primary">Subscribe</button>
            </div>
          </div>
        </div>
      </div>
      {!loadingMedicine &&
        <div className='container mt-5'>
          {/* <div className='row'>
          <div className='col-4'> */}
          <div className='row'>
            
              {!medicine_list_pe && <TobeDisplayed />}
              {medicine_list_pe}
              {medicine_list_1mg}
              {medicine_list_nm}           
          </div>
        </div>
      }
      {/*<div className='col-4'>
          <div className='row'>

          </div>
        </div>
        <div className='col-4'>
          <div className='row'>

          </div>
        </div>
       
        </div>
      </div> */}

    </div >
  )
}

