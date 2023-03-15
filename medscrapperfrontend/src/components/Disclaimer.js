import React from 'react'
import image1 from './data/img1.jpg'
import image2 from './data/img2.jpg'
import image3 from './data/img3.jpg'
import data from '../components/data/data.json'
import './disclaimer.css'


function Disclaimer() {
  console.log(data.About.Why)
  const about = data.About.Why
  const items = about.map((item) => {
    return (<li>{item}</li>)
  })
  return (
    <div className='container mt-3'>
      <div id="carouselExampleCaptions" className="carousel slide" data-bs-ride="true">
        <div className="carousel-indicators">
          <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" className="active" aria-current="true" aria-label="Slide 1"></button>
          <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
          <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2" aria-label="Slide 3"></button>
        </div>
        <div className="carousel-inner">
            <h3 className='text-center'>please wait ! processing your request...</h3>
          <div className="carousel-item active">
            <img src={image1} className="d-block w-100" alt="..." />
            <div className="carousel-caption d-none d-md-block" >
              <h5 style={{ color: "red", fontSize: "30px" }}>Disclaimer</h5>
              <p style={{ fontSize: "16px" }}>Disclaimer: Our company provides information of medications strictly for medicinal purposes only. We do not make any claims or representations about the efficacy or safety of the medications we recommand. Our information is not intended to diagnose, treat, cure, or prevent any disease.
              </p>
              <hr />
              <p style={{ fontSize: "16px" }}>
                The information provided on our website is for informational purposes only and is not intended as a substitute for professional medical advice or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition or treatment.
              
                We make no warranties or representations regarding the accuracy, completeness, reliability, or suitability of any information provided on our website.
              </p>
              <hr />
              <p style={{ fontSize: "16px" }}>
                It is your responsibility to ensure that you use medicine in accordance with the instructions provided and under the guidance of a qualified healthcare provider. If you experience any adverse reactions or side effects from medicine, discontinue use immediately and consult with a healthcare provider.</p>
            </div>
          </div>
          <div className="carousel-item">
            <img src={image2} className="d-block w-100" alt="..." />
            <div className="carousel-caption d-none d-md-block">
              <h5 style={{ color: "orange", fontSize: "30px" }}>General Advice For Taking Any Medication</h5>
              <hr />
              <p>
                Read the label: Always read the label and instructions provided with the medication carefully. Follow the dosage instructions and any special instructions such as taking the medication with food or avoiding certain foods.
              </p>
              <hr />
              <p>
                Check the expiration date: Do not take any medication that is past its expiration date as it may not be effective or safe to use.
              </p>
              <hr />
              <p>
                Avoid alcohol and other substances: Some medications can interact with alcohol or other substances, so it's important to avoid these while taking medication.
              </p>
              <hr />
              <p>
                Follow the full course of treatment: Make sure to complete the full course of treatment as prescribed by your healthcare provider, even if you start feeling better before the medication is finished.
              </p>
              <hr />
              <p>
                Monitor for side effects: Be aware of any potential side effects of the medication and monitor for them. If you experience any adverse effects, inform your healthcare provider immediately.
              </p>
            </div>
          </div>
          <div className="carousel-item">
            <img src={image3} className="d-block w-100" alt="..." />
            <div className="carousel-caption d-none d-md-block">
              <h5 style={{ color: "yellow", fontSize: "30px" }}>General Advice for food</h5>
              <hr />
              <li>
                Take medication with a light meal: If the medication can be taken with food, take it with a light meal such as a piece of toast or a small bowl of cereal.
              </li>

              <li>
                Avoid certain foods: Certain foods can interact with certain medications and either decrease their effectiveness or cause adverse effects. For example, some antibiotics should not be taken with dairy products, while blood thinners should be avoided with foods high in vitamin K such as spinach and kale.
              </li><hr /><li>
                Take medication with water: Always take medication with water and avoid taking it with other beverages such as alcohol or fruit juice.
              </li><li>

                Don't take medication with a heavy meal: Avoid taking medication with a heavy meal, as this can slow down the absorption of the medication and decrease its effectiveness.
              </li>
              <hr />
              <li>
                Check with your healthcare provider: If you have any questions about whether or not to take a medication with food, check with your healthcare provider or pharmacist. They can advise you on the best way to take the medication for your specific condition.
              </li>
            </div>
          </div>
        </div>
        <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
          <span className="carousel-control-prev-icon" aria-hidden="true"></span>
          <span className="visually-hidden">Previous</span>
        </button>
        <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
          <span className="carousel-control-next-icon" aria-hidden="true"></span>
          <span className="visually-hidden">Next</span>
        </button>
      </div>
    </div>
  )
}

export default Disclaimer
