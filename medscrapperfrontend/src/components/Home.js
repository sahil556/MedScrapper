import React, { useState, useRef } from 'react'
import Search from './Search'
import { addSubscription } from '../context/medicinecontext'
import MedicineDisplay from './MedicineDisplay'
import Disclaimer from './Disclaimer'


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
      if (medicines1mg.length > 0) {
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

<div className='container'>
      <Search setMedicinespe={setMedicinespe} setMedicines1mg={setMedicines1mg} setMedicinesnm={setMedicinesnm} setLoadingMedicine={setLoadingMedicine} style={{ zIndex: 10 }} />
</div>
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


      <div className='container my-3 mt-5'>

        <div className='row'>

          {loadingMedicine && <Disclaimer />}
          {!loadingMedicine && medicine_list_pe == undefined&&
            <div>
              <div className="jumbotron mt-4" style={{ backgroundColor: "#ccffe5" }}>
                <h1 style={{ fontFamily: "serif" }}>Welcome to our Medicine WebScapping Store</h1>
                <p style={{ fontFamily: "sans-serif" }}>Find the medications you need at affordable prices.</p>
                <a className="btn btn-outline-dark btn-lg" to="#" style={{textDecoration:"none"}} role="button">Browse Medicine</a>
              </div>
              <div className="container">
                <h3>Featured Results</h3>
                <div className="row">
                  <div className="col-sm-4">
                    <div className="card">
                      <img src="https://onemg.gumlet.io/l_watermark_346,w_480,h_480/a_ignore,w_480,h_480,c_fit,q_auto,f_auto/cropped/mu5bahqxfrp28cut6que.jpg" className="card-img-top" alt="..." />
                      <div className="card-body">
                        <h5 className="card-title"><b>Dolo 650 Tablet</b></h5>
                        <p className="card-text"><b>₹25</b><br/>Dolo 650 Tablet helps relieve pain and fever by blocking the release of certain chemical messengers responsible for fever and pain....</p>
                        <a href="https://www.1mg.com/drugs/dolo-650-tablet-74467" target={"_blank"} style={{textDecoration:"none"}} className="btn btn-outline-dark">Know More</a>
                      </div>
                    </div>
                  </div>
                  <div className="col-sm-4">
                    <div className="card">
                      <img style={{height: "250px"}} src="https://cdn01.pharmeasy.in/dam/products/I43006/crocin-650mg-advance-tab-15s-2-1641538269.jpg?dim=350x200&dpr=1&q=100" className="card-img-top" alt="crosin img" />
                      <div className="card-body">
                        <h5 className="card-title"><b>Crocin 650mg Advance Tablets 15'S</b></h5>
                        <p className="card-text"><b>₹29.13</b><br/>Crocin 650 Advance tablet is a pain-relieving medicine. It contains paracetamol as an active ingredient...</p>
                        <a href="https://pharmeasy.in/online-medicine-order/crocin-650mg-advance-tab-15-s-217263" target={"_blank"} style={{textDecoration:"none"}} className="btn btn-outline-dark">Know More</a>
                      </div>
                    </div>
                  </div>
                  <div className="col-sm-4">
                    <div className="card">
                      <img style={{height: "250px"}}  src="https://www.netmeds.com/images/product-v1/600x600/369491/azifast_250mg_tablet_6_s_0.jpg" className="card-img-top" alt="..." />
                      <div className="card-body">
                        <h5 className="card-title"><b>Azifast 250mg Tablet 6'S</b></h5>
                        <p className="card-text"><b>₹ 55.86</b> <br/>Azifast is used to treat mild to moderate susceptible infections caused by bacteria and micro-organisms which includes chest, ...</p>
                        <a href="https://www.netmeds.com/prescriptions/azifast-250mg-tablet-6-s" target={'_blank'} style={{textDecoration:"none"}} className="btn btn-outline-dark">Know More</a>
                      </div>
                    </div>
                  </div>
                </div>
                <div />
              </div>
              </div>
              }
              {medicine_list_pe}
              {medicine_list_1mg}
              {medicine_list_nm}
            </div>
        </div>


      </div >
      )
}

