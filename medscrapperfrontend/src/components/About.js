import React, {useEffect, useState} from 'react'
import { AboutCompo } from './about/AboutCompo'
import { Features } from "./about/features";
import { Services } from "./about/services";
import { Contact } from "./about/contact";
import JsonData from "./data/data.json";
import './about.css'


export default function About() {
  const [landingPageData, setLandingPageData] = useState({});
  useEffect(() => {
    setLandingPageData(JsonData);
  }, []);

  return (
    <div>
      {/* <Features data={landingPageData.Features} /> */}
      <AboutCompo data={landingPageData.About} />
      <Services data={landingPageData.Services} />
      <Contact data={landingPageData.Contact} />
    </div>
  )
}
