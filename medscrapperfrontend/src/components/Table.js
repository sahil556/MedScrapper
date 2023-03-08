function Table(props){
    const tableData = props.tableData
    return(
        <table className="table">
            {tableData.length > 0 &&
            <thead>
                <tr>
                    <th>S.N</th>
                    <th>Medicine Name</th>
                    <th>Available on</th>
                    <th>Action</th>
                </tr>
            </thead>
            }
            <tbody>
            {
                tableData.map((data, index)=>{
                    return(
                        <tr key={index}>
                            <td>{index+1}</td>
                            <td>{data.medicine_name}</td>
                            <td>{data.website_name}</td>
                            <td><button className="btn btn-outline-dark" onClick={() => {props.removeSubscription(data.id)}}>Unsubscribe</button></td>
                        </tr>
                    )
                })
            }
            </tbody>
        </table>
    )
}

export default Table;