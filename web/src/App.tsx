import { useEffect, useRef, useState } from "react";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    return () => {
      eventSourceRef.current?.close();
    };
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const stopStreaming = () => {
    eventSourceRef.current?.close();
    eventSourceRef.current = null;
    setLoading(false);
  };

  const handleSubmit = () => {
    if (!input.trim() || loading) {
      return;
    }

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: input.trim(),
    };
    const assistantId = crypto.randomUUID();

    setMessages((prev) => [
      ...prev,
      userMessage,
      { id: assistantId, role: "assistant", content: "" },
    ]);
    setInput("");
    setLoading(true);

    const url = new URL("http://localhost:8000/weather");
    url.searchParams.set("query", userMessage.content);

    const es = new EventSource(url.toString());
    eventSourceRef.current = es;

    es.onmessage = (event) => {
      const chunk = event.data ?? "";
      if (!chunk) {
        return;
      }
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantId
            ? { ...msg, content: msg.content + chunk }
            : msg,
        ),
      );
    };

    es.onerror = () => {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantId
            ? {
                ...msg,
                content:
                  msg.content ||
                  "Unable to stream right now. Please try again.",
              }
            : msg,
        ),
      );
      es.close();
      eventSourceRef.current = null;
      setLoading(false);
    };

    es.onopen = () => {
      setLoading(true);
    };
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen w-full max-w-5xl flex-col px-6 py-10">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
              Assignment
            </p>
            <h1 className="text-2xl font-semibold text-white sm:text-2xl">
              Agentic AI Mini-Project
            </h1>
          </div>
          <div className="rounded-full bg-slate-900 px-4 py-2 text-xs text-slate-400">
            SSE · localhost:8000/weather
          </div>
        </header>

        <div className="flex-1 space-y-6 overflow-y-auto rounded-3xl border border-slate-800 bg-slate-900/60 p-6 shadow-2xl shadow-slate-900/40">
          {messages.length === 0 && (
            <div className="grid place-items-center text-center text-slate-400">
              <div className="space-y-2">
                <p className="text-lg">Ask for a city to get live weather.</p>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[78%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-lg sm:text-base ${
                  message.role === "user"
                    ? "bg-indigo-500 text-white shadow-indigo-500/30"
                    : "bg-slate-800 text-slate-100 shadow-slate-950/30"
                }`}
              >
                {message.content ||
                  (message.role === "assistant" && loading ? "…" : "")}
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/70 p-4 shadow-xl shadow-slate-900/40">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <textarea
              className="flex-1 resize-none rounded-2xl border border-slate-800 bg-slate-950/80 px-4 content-center-safe text-sm text-slate-100 outline-none placeholder:text-slate-500 focus:border-indigo-500 sm:text-base"
              placeholder="What is the weather in Bangalore?"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
            />
            <div className="flex w-full gap-3 sm:w-auto">
              <button
                onClick={handleSubmit}
                className="flex-1 rounded-2xl bg-indigo-500 px-5 py-3 text-sm font-semibold text-white  transition hover:bg-indigo-400 hover:cursor-pointer disabled:cursor-not-allowed disabled:opacity-60 sm:text-base"
                disabled={loading}
              >
                {loading ? "Streaming…" : "Send"}
              </button>
              <button
                onClick={stopStreaming}
                className="flex-1 rounded-2xl border border-slate-700 px-5 py-3 text-sm font-semibold text-slate-200 transition hover:border-slate-500 disabled:cursor-not-allowed disabled:opacity-60 sm:text-base"
                disabled={!loading}
              >
                Stop
              </button>
            </div>
          </div>
          <p className="mt-3 text-xs text-slate-500">
            Streaming uses Server-Sent Events. Keep this tab open while
            responses arrive.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
