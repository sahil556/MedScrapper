
const MedicineState = async (medicineName) => {
    let headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
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
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
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
   return data;
   
}
export default MedicineState
