
const MedicineState = async (medicineName) => {
    let headersList = {
        "Accept": "*/*",
        "Content-Type": "application/json"
       }
       
       let bodyContent = JSON.stringify({
         "name" : medicineName
       });
       
       let response = await fetch("http://127.0.0.1:8000/search", { 
         method: "POST",
         body: bodyContent,
         headers: headersList
       });
       
       let data = await response.text();
       
       
    return data
}

export const MedicineInfo = async (seachquery, site) =>{
 
  
  let headersList = {
    "Accept": "*/*",
    "Content-Type": "application/json"
   }
   
   let bodyContent = JSON.stringify({
     "name" : seachquery
   });
   
   let response = await fetch("http://127.0.0.1:8000/" + site, { 
     method: "POST",
     body: bodyContent,
     headers: headersList
   });
   
   let data = await response.text();
   console.log(data)
   return data;
   
}

export const addSubscription = async (subsciption) => {
  let headersList = {
    "Accept": "*/*",
    "Content-Type": "application/json"
   }
   
   let bodyContent = JSON.stringify({
     "medicine_name" : subsciption.medicine_name,
     "email": subsciption.email,
     "website_name": subsciption.website_name,
   });
   
   let response = await fetch("http://127.0.0.1:8000/addSubscription", { 
     method: "POST",
     body: bodyContent,
     headers: headersList
   });
   
   let data = await response.text();
   console.log(data);
   
}
export default MedicineState
