import { useState, useRef, useEffect, useCallback } from "react";
import { Send, Bot } from "lucide-react";
import ChatMessage from "./ChatMessage";

interface Message {
  role: "user" | "assistant";
  content: string;
  category?: string;
  sources?: { title: string; snippet: string }[];
}

const SUGGESTED_PROMPTS = [
  "How is certification calculated?",
  "What is the grading policy?",
  "What are the deadlines?",
  "What topics are covered?",
];

const API_BASE_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");
const API_URL = `${API_BASE_URL}/answer`;

const AIAssistantPanel = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Welcome to the Course Assistant. I can help you with questions about grading, certification, deadlines, and course structure. How can I assist you today?",
      category: "General",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || isLoading) return;

      const userMessage: Message = { role: "user", content: text.trim() };
      setMessages((prev) => [...prev, userMessage]);
      setInput("");
      setIsLoading(true);

      try {
        const response = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: text.trim(), top_k: 3 }),
        });

        if (!response.ok) throw new Error("Request failed");

        const data = await response.json();
        const aiMessage: Message = {
          role: "assistant",
          content: data.answer || "I'm sorry, I couldn't find an answer to that question.",
          category: data.category,
          sources: data.retrieval_results?.map((r: any) => ({
            title: r.title || "Source Document",
            snippet: r.text || r.content || "",
          })),
        };
        setMessages((prev) => [...prev, aiMessage]);
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content:
              "I'm unable to connect to the course knowledge base right now. Please try again later or contact your instructor.",
            category: "System",
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading]
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  return (
    <div className="flex h-full flex-col rounded-lg border bg-card shadow-card">
      {/* Header */}
      <div className="border-b px-5 py-4">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <Bot className="h-4 w-4 text-primary-foreground" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-foreground">Course Assistant</h2>
            <p className="text-xs text-muted-foreground">
              Ask about grading, certification, deadlines, or course structure.
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {messages.map((msg, i) => (
          <ChatMessage key={i} {...msg} />
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="rounded-lg rounded-bl-sm bg-chat-ai px-4 py-3">
              <div className="dot-animation flex gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground inline-block" />
                <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground inline-block" />
                <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground inline-block" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested prompts */}
      {messages.length <= 1 && (
        <div className="border-t px-4 py-3">
          <p className="text-[11px] uppercase tracking-wider text-muted-foreground mb-2 font-medium">
            Suggested questions
          </p>
          <div className="flex flex-wrap gap-1.5">
            {SUGGESTED_PROMPTS.map((prompt) => (
              <button
                key={prompt}
                onClick={() => sendMessage(prompt)}
                className="rounded-md border bg-card px-3 py-1.5 text-xs text-foreground hover:bg-muted transition-colors"
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t px-4 py-3">
        <div className="flex items-center gap-2 rounded-lg border bg-background px-3 py-1.5 focus-within:ring-2 focus-within:ring-ring/20 transition-shadow">
          <input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            disabled={isLoading}
            className="flex-1 bg-transparent text-sm text-foreground placeholder:text-muted-foreground outline-none disabled:opacity-50 py-1.5"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="flex h-7 w-7 items-center justify-center rounded-md bg-primary text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-30"
          >
            <Send className="h-3.5 w-3.5" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default AIAssistantPanel;
