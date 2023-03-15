import React from 'react'
import image1 from './data/img1.jpg'
import image2 from './data/img2.jpg'
import image3 from './data/img3.jpg'
import data from '../components/data/data.json'
import './test.css'


function Test() {
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
          <div className="carousel-item active">
            <img src={image1} className="d-block w-100" alt="..." />
            <div className="carousel-caption d-none d-md-block">
              <h5>First slide label</h5>
              <ul>
                {items}
              </ul>
              <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Modi possimus rerum sed quaerat molestias voluptate vitae ipsam consectetur similique reprehenderit? Sed repellendus natus iste cum autem est assumenda tenetur esse corporis nobis rerum, praesentium itaque necessitatibus voluptatem ullam dolore fuga! Tempore animi saepe natus libero praesentium voluptas recusandae vero accusamus!</p>
              <hr/>
              <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Tenetur laudantium quisquam incidunt nemo dolorem ducimus, fuga est, corrupti placeat sed doloribus beatae maxime dolor impedit error in dignissimos ex id, veritatis magnam alias. Repellat, optio. Aspernatur voluptatum aliquam quae, quibusdam facere necessitatibus, cumque sed quam nulla, dolorum possimus officia minima!</p>
              <hr/>
              <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Aspernatur sit illo consequuntur nam inventore ab, mollitia, ut fuga dolore totam ducimus neque natus est excepturi suscipit quibusdam, vitae aliquid vero aut sequi? Neque fugiat sint recusandae est, mollitia totam esse.</p>
            </div>
          </div>
          <div className="carousel-item">
            <img src={image2} className="d-block w-100" alt="..." />
            <div className="carousel-caption d-none d-md-block">
              <h5>Second slide label</h5>
              <p>Some representative placeholder content for the second slide.</p>
            </div>
          </div>
          <div className="carousel-item">
            <img src={image3} className="d-block w-100" alt="..." />
            <div className="carousel-caption d-none d-md-block">
              <h5>Third slide label</h5>
              <p>Some representative placeholder content for the third slide.</p>
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

export default Test
