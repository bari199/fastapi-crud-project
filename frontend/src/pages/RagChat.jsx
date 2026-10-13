import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export default function RagChat() {
  const navigate = useNavigate();

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    const value = question.trim();
    if (!value || loading) return;

    setError("");
    setQuestion("");
    setMessages((current) => [
      ...current,
      { role: "user", content: value },
    ]);
    setLoading(true);

    try {
      // Verify the request schema in FastAPI /docs.
      const response = await api.post("/rag/chat", {
        question: value,
      });

      const data = response.data;

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (err) {
      if (err.response?.status === 401) {
        sessionStorage.removeItem("access_token");
        navigate("/login", { replace: true });
        return;
      }

      setError(
        err.response?.data?.detail ||
          "Could not get an answer. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-8">
      <div className="mx-auto flex max-w-4xl flex-col gap-6">
        <header className="flex items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900">
              AI Knowledge Assistant
            </h1>
            <p className="mt-2 text-sm text-slate-600">
              Ask questions about your ingested documents.
            </p>
          </div>

          <Button
            variant="outline"
            onClick={() => navigate("/dashboard")}
          >
            Dashboard
          </Button>
        </header>

        <section
          className="min-h-[420px] space-y-5 rounded-xl border bg-white p-4 shadow-sm sm:p-6"
          aria-live="polite"
        >
          {messages.length === 0 && (
            <div className="flex min-h-[350px] flex-col items-center justify-center text-center">
              <div className="mb-4 rounded-2xl bg-slate-100 p-4 text-3xl">
                ✨
              </div>
              <h2 className="text-xl font-semibold text-slate-900">
                Ask your first question
              </h2>
              <p className="mt-2 max-w-md text-sm text-slate-500">
                Your question will be answered using relevant document
                chunks retrieved by the RAG pipeline.
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <article
              key={`${message.role}-${index}`}
              className={`rounded-xl p-4 ${
                message.role === "user"
                  ? "ml-4 bg-slate-100 sm:ml-16"
                  : "mr-4 border border-slate-200 bg-white sm:mr-16"
              }`}
            >
              <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
                {message.role === "user" ? "You" : "AI Assistant"}
              </p>

              <p className="whitespace-pre-wrap break-words text-sm leading-7 text-slate-800">
                {message.content}
              </p>

              {message.sources?.length > 0 && (
                <div className="mt-4 border-t pt-3">
                  <h3 className="mb-2 text-sm font-semibold text-slate-700">
                    Sources
                  </h3>

                  <ul className="space-y-2">
                    {message.sources.map((source, sourceIndex) => (
                      <li
                        key={`${source.source}-${source.chunk_index}-${sourceIndex}`}
                        className="rounded-md bg-slate-50 px-3 py-2 text-sm text-slate-600"
                      >
                        <span className="font-medium">
                          {source.source}
                        </span>
                        <span className="ml-2 text-xs text-slate-500">
                          Chunk {source.chunk_index}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </article>
          ))}

          {loading && (
            <div className="mr-4 rounded-xl border bg-white p-4 sm:mr-16">
              <p className="animate-pulse text-sm text-slate-500">
                Searching documents and generating an answer...
              </p>
            </div>
          )}

          {error && (
            <p
              role="alert"
              className="rounded-lg bg-red-50 p-3 text-sm text-red-700"
            >
              {error}
            </p>
          )}
        </section>

        <form
          onSubmit={handleSubmit}
          className="space-y-3 rounded-xl border bg-white p-4 shadow-sm"
        >
          <label
            htmlFor="rag-question"
            className="text-sm font-medium text-slate-700"
          >
            Your question
          </label>

          <Textarea
            id="rag-question"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask something about your project documentation..."
            rows={3}
            maxLength={5000}
            disabled={loading}
            required
          />

          <div className="flex items-center justify-between gap-3">
            <p className="text-xs text-slate-500">
              Answers may take time while the local AI model runs.
            </p>

            <Button
              type="submit"
              disabled={loading || !question.trim()}
            >
              {loading ? "Thinking..." : "Send question"}
            </Button>
          </div>
        </form>
      </div>
    </main>
  );
}
