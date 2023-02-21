import React from 'react'

export default function Medicine(props) {
  // console.log(props.item);
  return (
    <>
    
      <div className='my-2'>
        {/* <div className="mx-2  g-2 py-1 row-cols-1 row-cols-lg-3 " style={{display:'flex', position:'relative'}}> */}
          <span className="badge badge-pill bg-warning " style={{position:'absolute', top:'-1', left:'-1', width:'auto'}}>{props.item.manufacturer}</span>
          <div  className="bg-dark py-4 col d-flex align-items-start border border-secondary-subtle border-1 rounded">
            <div
              className="mt-5 mx-3 icon-square text-bg-light d-inline-flex align-items-center justify-content-center fs-4 flex-shrink-0 me-3">
              <img className="icon" src={props.item.imglink} alt="medicine image" srcSet="" />
            </div>
            <div>
            {/* <span className=" badge rounded-pill bg-danger" style={{left:'85%', zIndex:1}}>
                            {source}
                        </span> */}
            
              <h4 className="fs-4 fw-bolder text-white">{props.item.name}</h4>
              <p className="fw-light text-white fs-6 lh-1">{props.item.content}</p>
              {/* <p className="fw-light text-secondary fw-semibold lh-1">10 CAPSULE(S) IN STRIP</p> */}
              <div className="d-flex justify-content-between lh-lg">
                <div className="d-flex flex-row">
                  <h5 className="fw-light fw-semibold me-2 text-white">{props.item.price}</h5>
                </div>
              </div>
              <a className="btn btn-lg text-dark pe-auto p-0 fw-semibold fs-6 text-white" href="www.google.com">{props.item.description.substr(0,50)}..</a>
              <div className='mt-2'>
              <a href={props.item.medlink} className="btn btn-success btn-md fw-semibold align-top">Visit</a>
                &nbsp;
                <button onClick={()=>{props.Notifyme(props.item)}} className="mx-2 btn btn-outline-primary btn-md fw-semibold align-top">Notify</button>
              </div>
            </div>
          </div>
        </div>
        {/* </div> */}
      </>
    )
}
