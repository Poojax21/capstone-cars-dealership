import React, { useEffect, useState } from "react";

const Dealers = ({ state }) => {
  const [dealers, setDealers] = useState([]);

  useEffect(() => {
    const url = state
      ? `/djangoapp/get_dealers/${state}`
      : "/djangoapp/get_dealers/";
    fetch(url)
      .then((res) => res.json())
      .then((data) => setDealers(data.dealers || []));
  }, [state]);

  return (
    <table className="dealers-table">
      <thead>
        <tr>
          <th>Dealer Name</th>
          <th>City</th>
          <th>State</th>
          <th>Address</th>
          <th>Reviews</th>
        </tr>
      </thead>
      <tbody>
        {dealers.map((dealer) => (
          <tr key={dealer.id}>
            <td>{dealer.full_name}</td>
            <td>{dealer.city}</td>
            <td>{dealer.state}</td>
            <td>{dealer.address}</td>
            <td>
              <a href={`/dealer/${dealer.id}`}>Review Dealer</a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default Dealers;
