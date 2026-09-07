import { useRef, useEffect } from "react";
import { ChatMessage } from "./ChatMessage";

export function ChatWindow({ messages }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full">
          <p className="text-sm text-slate-400">Ask something about your reports</p>
        </div>
      ) : (
        <div className="max-w-2xl mx-auto">
          {messages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg} />
          ))}
          <div ref={endRef} />
        </div>
      )}
    </div>
  );
}