export async function fetchClusteredProperties() {
  const res = await fetch("http://localhost:8000/api/clusters");
  return await res.json();
}
