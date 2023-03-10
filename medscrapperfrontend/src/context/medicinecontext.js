
const MedicineState = async (medicineName, searchby, company) => {
  let endpoint = ""
    console.log(searchby)
    if(searchby == "name")
      endpoint = "search"
    else
      endpoint = "searchbycontent"
    
    let headersList = {
        "Accept": "*/*",
        "Content-Type": "application/json"
       }
       
       let bodyContent = JSON.stringify({
         "name" : medicineName,
         "searchby" : searchby,
         "website": company
       });
       
       let response = await fetch("http://127.0.0.1:8000/" + endpoint, { 
         method: "POST",
         body: bodyContent,
         headers: headersList
       });
       
       let data = await response.text();
       
       
    return data
}

export const MedicineInfo = async (seachquery, site, selected, searchby) =>{
 
  
  let headersList = {
    "Accept": "*/*",
    "Content-Type": "application/json"
   }
   
   let bodyContent = JSON.stringify({
     "name" : seachquery,
     "website" : site,
     "selected": selected,
     "searchby" : searchby
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

export const getcontentbymedicinename = async(name, site) => {
  let headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/json"
   }
   
   let bodyContent = JSON.stringify({
     "name" : name,
     "website": site
   });
   
   let response = await fetch("http://127.0.0.1:8000/getcontentbymedicinename", { 
     method: "POST",
     body: bodyContent,
     headers: headersList
   });
   
   let data = await response.text();
   console.log(data)
    return data;
   
}

export default MedicineState
