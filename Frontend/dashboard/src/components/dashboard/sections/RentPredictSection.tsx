import React, { useState } from 'react';

export const RentPredictSection = () => {
  const [form, setForm] = useState({ suburb: '', floor_size: '', bedrooms: '', bathrooms: '' });
  const [result, setResult] = useState<number | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handlePredict = async () => {
    const res = await fetch('/predict_rent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    setResult(data.predicted_rent);
  };

  return (
    <div>
      <h2>Rent Cost Prediction</h2>
      <input name="suburb" placeholder="Suburb" onChange={handleChange} />
      <input name="floor_size" placeholder="Floor Size" onChange={handleChange} />
      <input name="bedrooms" placeholder="Bedrooms" onChange={handleChange} />
      <input name="bathrooms" placeholder="Bathrooms" onChange={handleChange} />
      <button onClick={handlePredict}>Confirm</button>
      {result !== null && <div>Expected Rent Cost: ${result}</div>}
    </div>
  );
};