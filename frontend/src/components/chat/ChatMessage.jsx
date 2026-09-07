import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`max-w-lg rounded-2xl px-4 py-3 text-sm ${
          isUser
            ? "bg-slate-900 text-white rounded-br-md"
            : "bg-slate-100 text-slate-700 rounded-bl-md"
        }`}
      >
        {isUser ? (
          message.content
        ) : (
          <div className="chat-markdown">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
          </div>
        )}
        {message.safetyNotice && (
          <p className="mt-2 text-xs text-slate-500">{message.safetyNotice}</p>
        )}
        {message.citations?.length > 0 && (
          <div className="mt-3 border-t border-slate-200 pt-2 text-xs text-slate-500">
            <p className="font-medium text-slate-600">Sources</p>
            {message.citations.map((citation) => (
              <p key={`${citation.report_id}-${citation.result_id}`}>
                {citation.test_name} · {citation.filename}
                {citation.report_date ? ` · ${citation.report_date}` : ""}
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}