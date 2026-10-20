import React, { useEffect, useState } from "react";

const Dealer = ({ dealerId }) => {
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch(`/djangoapp/dealer/${dealerId}`)
      .then((res) => res.json())
      .then((data) => setDealer(data.dealer));
    fetch(`/djangoapp/reviews/dealer/${dealerId}`)
      .then((res) => res.json())
      .then((data) => setReviews(data.reviews || []));
  }, [dealerId]);

  if (!dealer) return <p>Loading dealer...</p>;

  return (
    <div className="dealer-detail">
      <h2>{dealer.full_name}</h2>
      <p>
        {dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}
      </p>
      <h3>Reviews</h3>
      <ul>
        {reviews.map((review) => (
          <li key={review.id}>
            <strong>{review.name}</strong>: {review.review} ({review.sentiment})
          </li>
        ))}
      </ul>
      <a href={`/dealer/${dealerId}/review`}>Post a Review</a>
    </div>
  );
};

export default Dealer;
