import React from 'react'

export default function Search() {
    return (
        <>
            <div>
                <h1>pharmeasy scrapping request : </h1>
                <form action="http://127.0.0.1:8000/pharmeasy" method="post">
                    <input type="text" name="name" placeholder="Enter medicine name" />
                    <button type="submit">submit</button>
                </form>
                <br /><br />
                <hr />
                <br />
                <h1>netmeds scrapping request : </h1>
                <form action="http://127.0.0.1:8000/netmeds" method="post">
                    <input type="text" name="name" placeholder="Enter medicine name" />
                    <button type="submit">submit</button>
                </form>
            </div>
        </>
    )
}
