import { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });
      const data = await res.json();
      setResponse(data.answer); // Assumes FastAPI returns { "answer": "..." }
    } catch (err) {
      setResponse("Error connecting to Agent backend.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-6">Multi-Agent Assistant</h1>

      <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-md">
        <textarea
          className="w-full p-2 border rounded mb-4"
          placeholder="e.g., Get weather in NYC and summarize it"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? "Agents are thinking..." : "Ask Agents"}
        </button>
      </div>

      {response && (
        <div className="mt-8 p-6 max-w-2xl bg-white rounded-lg shadow-inner border-l-4 border-blue-500">
          <p className="text-gray-800">{response}</p>
        </div>
      )}
    </div>
  );
}

export default App;
