import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    // Fetch historical prices
    fetch("http://127.0.0.1:5000/api/historical_prices")
      .then((res) => res.json())
      .then((data) => {
        const parsed = data.map((d) => ({
          ...d,
          Date: new Date(d.Date),
        }));
        setPrices(parsed);
      });

    // Fetch events
    fetch("http://127.0.0.1:5000/api/events")
      .then((res) => res.json())
      .then((data) => {
        const parsed = data.map((d) => ({
          ...d,
          Start_Date: new Date(d.Start_Date),
        }));
        setEvents(parsed);
      });
  }, []);

  // Filter prices by selected dates and mark events
  const filteredPrices = prices
    .filter(
      (p) =>
        (!startDate || p.Date >= new Date(startDate)) &&
        (!endDate || p.Date <= new Date(endDate))
    )
    .map((p) => ({
      ...p,
      isEvent: events.some(
        (e) =>
          e.Start_Date.toISOString().split("T")[0] ===
          p.Date.toISOString().split("T")[0]
      ),
    }));

  // Compute average price for event points
  const averagePrice =
    filteredPrices
      .filter((p) => p.isEvent)
      .reduce((sum, p) => sum + p.Price, 0) /
    (filteredPrices.filter((p) => p.isEvent).length || 1);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2>📊 Brent Oil Price Dashboard</h2>

      <div style={{ marginBottom: "20px" }}>
        <label>
          Start Date:{" "}
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
        <label style={{ marginLeft: "20px" }}>
          End Date:{" "}
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
      </div>

      <h3>Historical Prices</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={filteredPrices}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="Date"
            tickFormatter={(tick) =>
              new Date(tick).toLocaleDateString()
            }
          />
          <YAxis />
          <Tooltip
            labelFormatter={(label) =>
              new Date(label).toLocaleDateString()
            }
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="Price"
            stroke="#8884d8"
            strokeWidth={2}
            dot={(props) => {
              const { cx, cy, payload } = props;
              return (
                <circle
                  cx={cx}
                  cy={cy}
                  r={payload.isEvent ? 6 : 3}
                  fill={payload.isEvent ? "red" : "#8884d8"}
                />
              );
            }}
          />
        </LineChart>
      </ResponsiveContainer>

      <h3 style={{ marginTop: "30px" }}>Key Events</h3>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "10px",
        }}
      >
        <thead>
          <tr style={{ backgroundColor: "#f0f0f0" }}>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>
              Date
            </th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>
              Event
            </th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>
              Category
            </th>
          </tr>
        </thead>
        <tbody>
          {events
            .filter(
              (e) =>
                (!startDate || e.Start_Date >= new Date(startDate)) &&
                (!endDate || e.Start_Date <= new Date(endDate))
            )
            .map((e, idx) => (
              <tr
                key={idx}
                style={{
                  backgroundColor: "#ffeeba",
                }}
              >
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                  {e.Start_Date.toLocaleDateString()}
                </td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                  {e.Event_Name}
                </td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                  {e.Category}
                </td>
              </tr>
            ))}
        </tbody>
      </table>

      <div style={{ marginTop: "20px", fontWeight: "bold" }}>
        Average Price at Event Points: {averagePrice.toFixed(2)}
      </div>
    </div>
  );
}

export default App;
