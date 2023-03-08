import React from 'react'
import './Card.css'

export default function MedicineDisplay(props) {
    const {name, price, imglink, manufacturer, medlink, content, description} = props.item
  return (
    // <div className="col-xs-12 col-md-4 bootstrap snippets bootdeys">
    <div className="product-content product-wrap clearfix">
        <div className="row">
            <div className="col-md-4 col-sm-12 col-xs-12">
                <div className="product-image"> <img src={imglink}
                        alt="Medicine Image" className="img-responsive"/> <span className="tag2 hot"> RX </span></div>
            </div>
            <div className="col-md-12 col-sm-12 col-xs-12">
                <div className="product-deatil">
                    <h5 className="name" > <a href={medlink} style={{"fontSize":"22px"}}> {name} <span>{manufacturer}</span> </a></h5>
                    <p className="price-container"> <span>{price}</span></p> <span className="tag1"></span>
                </div>
                <div className="product-detail">
                    
                    <p className='container'>{content}</p>
                </div>
                <div className="description">
                    <p>{description.substr(0, 80)}...</p>
                </div>
                <div className="mx-5">
                    <div className="row">
                        <div className="col center btn"> <a href={medlink}
                                className="btn btn-outline-primary">View Details</a>&nbsp;&nbsp;
                                <a onClick={()=>{props.Notifyme(props.item)}} href="#"
                                className="btn btn-outline-danger">Notifyme</a>
                        </div>
                        
                        
                    </div>
                </div>
            </div>
        </div>
    </div>
// </div>
  )
}
