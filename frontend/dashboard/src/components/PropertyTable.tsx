import { useEffect, useState } from "react";
import { fetchProperties, Property } from "../api/properties";

export default function PropertyTable() {
  const [rows, setRows] = useState<Property[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    fetchProperties().then(setRows).catch(e => setErr(String(e)));
  }, []);

  if (err) return <div>Error: {err}</div>;

  return (
    <table>
      <thead>
        <tr>
          <th>Address</th><th>Suburb</th><th>Bed</th><th>Bath</th><th>Rent/wk</th>
        </tr>
      </thead>
      <tbody>
        {rows.map(r => (
          <tr key={r.id}>
            <td>{r.address}</td>
            <td>{r.suburb}</td>
            <td>{r.bedrooms}</td>
            <td>{r.bathrooms}</td>
            <td>{r.rent_weekly ?? "-"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
