import React, { useState } from 'react';

export const RentPredictSection = () => {
  const [form, setForm] = useState({
    suburb: '',
    floor_size_min: '',
    floor_size_max: '',
    bedrooms_min: '',
    bedrooms_max: '',
    bathrooms_min: '',
    bathrooms_max: '',
  });
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
    <div className="max-w-md mx-auto bg-white rounded-xl shadow-md p-8 space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Rent Cost Prediction</h2>
      <input
        name="suburb"
        placeholder="Suburb"
        value={form.suburb}
        onChange={handleChange}
        className="w-full px-3 py-2 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <div className="mb-4">
        <label className="block text-gray-700 mb-1">Floor Size (㎡):</label>
        <div className="flex gap-2">
          <input
            name="floor_size_min"
            placeholder="Min"
            type="number"
            value={form.floor_size_min}
            onChange={handleChange}
            className="w-1/2 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="floor_size_max"
            placeholder="Max"
            type="number"
            value={form.floor_size_max}
            onChange={handleChange}
            className="w-1/2 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 mb-1">Number of Bedrooms:</label>
        <div className="flex gap-2">
          <input
            name="bedrooms_min"
            placeholder="Min"
            type="number"
            value={form.bedrooms_min}
            onChange={handleChange}
            className="w-1/2 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="bedrooms_max"
            placeholder="Max"
            type="number"
            value={form.bedrooms_max}
            onChange={handleChange}
            className="w-1/2 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 mb-1">Number of Bathrooms:</label>
        <div className="flex gap-2">
          <input
            name="bathrooms_min"
            placeholder="Min"
            type="number"
            value={form.bathrooms_min}
            onChange={handleChange}
            className="w-1/2 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="bathrooms_max"
            placeholder="Max"
            type="number"
            value={form.bathrooms_max}
            onChange={handleChange}
            className="w-1/2 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
      </div>
      <button
        onClick={handlePredict}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
      >
        Confirm
      </button>
      {result !== null && (
        <div className="mt-4 text-lg text-green-700 font-semibold">
          Expected Rent Cost: ${result}
        </div>
      )}
    </div>
  );
};