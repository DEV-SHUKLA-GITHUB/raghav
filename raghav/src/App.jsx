import React, { useEffect, useState } from "react";
import { Bar, Line } from 'react-chartjs-2';
import 'chart.js/auto';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [date, setDate] = useState('2025-07-07');

  const fetchData = (selectedDate) => {
    setLoading(true);
    // fetch(`http://127.0.0.1:4000/api/premium-traded?date=${selectedDate}`)
    fetch(`http://raghav-1-68tm.onrender.com/api/premium-traded?date=${selectedDate}`)
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchData(date);
  }, []);

  const handleDateChange = (e) => {
    setDate(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchData(date);
  };

  const chartData = {
    labels: data.map(row => row.TckrSymb),
    datasets: [
      {
        label: 'Premium Traded (Crores)',
        data: data.map(row => row['Premium Traded (Crores)']),
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-8">
      <h1 className="text-2xl font-bold mb-6">Premium Traded (Crores) by Symbol</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <label htmlFor="date" className="mr-2 font-semibold">Select Date:</label>
        <input
          type="date"
          id="date"
          value={date}
          onChange={handleDateChange}
          className="border rounded px-2 py-1"
          max="2025-07-13"
          min="2025-01-01"
          required
        />
        <button type="submit" className="ml-2 bg-blue-500 text-white px-4 py-1 rounded">Fetch</button>
      </form>
      {loading ? (
        <div className="text-lg">Loading...</div>
      ) : (
        <>
          <table className="min-w-[400px] bg-white shadow rounded-lg mb-6">
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
          <div className="w-full max-w-4xl">
            <Bar data={chartData} />
          </div>
        </>
      )}
    </div>
  );
}

export default App;
