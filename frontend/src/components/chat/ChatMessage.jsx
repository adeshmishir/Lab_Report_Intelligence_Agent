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
        {message.content}
      </div>
    </div>
  );
}