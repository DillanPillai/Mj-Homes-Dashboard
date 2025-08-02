// This file is the react component that renders a scatter chart visualizing properties clustered by location and price, color-coded by cluster group

import { ScatterChart, Scatter, XAxis, YAxis, Tooltip, Legend } from 'recharts';

interface Property {
  latitude: number;
  longitude: number;
  price: number;
  cluster: number;
}

export default function ClusterChart({ data }: { data: Property[] }) {
  const clusters = [0, 1, 2];
  const colors = ["#4f46e5", "#10b981", "#f59e0b"];

  return (
    <ScatterChart width={700} height={400}>
      <XAxis dataKey="longitude" name="Longitude" />
      <YAxis dataKey="price" name="Price" />
      <Tooltip cursor={{ strokeDasharray: '3 3' }} />
      <Legend />
      {clusters.map((c, i) => (
        <Scatter
          key={c}
          name={`Cluster ${c}`}
          data={data.filter(d => d.cluster === c)}
          fill={colors[i]}
        />
      ))}
    </ScatterChart>
  );
}
