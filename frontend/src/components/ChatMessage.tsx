import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

interface Source {
  title: string;
  snippet: string;
}

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  category?: string;
  sources?: Source[];
}

const ChatMessage = ({ role, content, category, sources }: ChatMessageProps) => {
  const [sourcesOpen, setSourcesOpen] = useState(false);

  if (role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-lg rounded-br-sm bg-chat-user px-4 py-2.5 text-sm text-chat-user-foreground">
          {content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="max-w-[90%] space-y-2">
        {category && (
          <span className="inline-block rounded-md bg-badge px-2 py-0.5 text-[11px] font-medium text-badge-foreground uppercase tracking-wider">
            {category}
          </span>
        )}
        <div className="rounded-lg rounded-bl-sm bg-chat-ai px-4 py-2.5 text-sm leading-relaxed text-chat-ai-foreground">
          {content}
        </div>
        {sources && sources.length > 0 && (
          <button
            onClick={() => setSourcesOpen(!sourcesOpen)}
            className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            {sourcesOpen ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
            {sources.length} source{sources.length > 1 ? "s" : ""}
          </button>
        )}
        {sourcesOpen && sources && (
          <div className="space-y-2 pl-1">
            {sources.map((source, i) => (
              <div key={i} className="rounded-md border bg-card p-3">
                <p className="text-xs font-medium text-foreground">{source.title}</p>
                <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{source.snippet}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
