import React from "react";
import { useState } from "react";
import FormInput from "./FormInput";
import Table from "./Table";

function ViewSubscription() {

  const [tableData, setTableData] = useState([])
  const [formInputData, setformInputData] = useState(
    {
      emailAddress: '',
    }
  );

  const handleChange = (evnt) => {
    const newInput = (data) => ({ ...data, [evnt.target.name]: evnt.target.value })
    setformInputData(newInput)
  }

  const removeSubscription = async(id) => {
    if(window.confirm("Are You Sure You Want to UnSubScribe ?"))
    {
      let headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Content-Type": "application/json"
       }
       
       let bodyContent = JSON.stringify({
         "id" : id
       });
       
       let response = await fetch("http://127.0.0.1:8000/removeSubscription", { 
         method: "POST",
         body: bodyContent,
         headers: headersList
       });
       
       let data = await response.text();
       const newData = tableData.filter((data) => { return data.id !== id })
       setTableData(newData)
    }
   
  }

  const handleSubmit = async (evnt) => {
    evnt.preventDefault();
    const checkEmptyInput = !Object.values(formInputData).every(res => res === "")
    if (checkEmptyInput) {
      let headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Content-Type": "application/json"
      }

      let bodyContent = JSON.stringify({
        "email": formInputData.emailAddress
      });

      let response = await fetch("http://127.0.0.1:8000/showsubscription", {
        method: "POST",
        body: bodyContent,
        headers: headersList
      });

      let data = await response.json();
      setTableData(data);
      console.log(data)
      const emptyInput = { emailAddress: '' }
      setformInputData(emptyInput)
    }
  }

  return (
    <React.Fragment>
      <div className="container mt-5">
        <div className="row">
          <div className="col-sm-8">
            <FormInput handleChange={handleChange} formInputData={formInputData} handleSubmit={handleSubmit} />
            <br/>
            <Table tableData={tableData} removeSubscription = {removeSubscription} />
          </div>
          <div className="col-sm-4">

          </div>
        </div>
      </div>
    </React.Fragment>
  );
}
export default ViewSubscription;