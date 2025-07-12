import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/api/premium-traded")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-8">
      <h1 className="text-2xl font-bold mb-6">Premium Traded (Crores) by Symbol</h1>
      {loading ? (
        <div className="text-lg">Loading...</div>
      ) : (
        <table className="min-w-[400px] bg-white shadow rounded-lg">
          <thead>
            <tr>
              <th className="px-4 py-2 border-b">Symbol</th>
              <th className="px-4 py-2 border-b">Premium Traded (Crores)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr key={row.TckrSymb}>
                <td className="px-4 py-2 border-b">{row.TckrSymb}</td>
                <td className="px-4 py-2 border-b">{row["Premium Traded (Crores)"].toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
