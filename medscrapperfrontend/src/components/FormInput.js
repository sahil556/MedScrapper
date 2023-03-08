function FormInput({handleChange, formInputData, handleSubmit}){
    return(
    
        <div className="form-row row">
          <div className="col">
            <input type="email" onChange={handleChange} value={formInputData.emailAddress} name="emailAddress" className="form-control" placeholder="Email Address" />
          </div>
          <div className="col">
            <input type="submit" value={"View Subscriptions"} onClick={handleSubmit} className="btn btn-primary" />
          </div>
        </div>
     
      
    )
    }
    
    export default FormInput;