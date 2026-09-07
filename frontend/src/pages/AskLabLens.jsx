import { useState } from "react";
import { useApp } from "../context/AppContext";
import { ChatWindow } from "../components/chat/ChatWindow";
import { ChatInput } from "../components/chat/ChatInput";
import { SuggestedQuestion } from "../components/chat/SuggestedQuestion";

export default function AskLabLens() {
  const { chatMessages, addChatMessage } = useApp();

  const handleSend = (question) => {
    addChatMessage({ role: "user", content: question });
    setTimeout(() => {
      addChatMessage({
        role: "assistant",
        content: "LabLens will answer this using your uploaded report data.",
      });
    }, 500);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">Ask LabLens</h1>
        <p className="mt-1 text-sm text-slate-500">
          Ask questions about your uploaded reports. Answers will be grounded in your report data.
        </p>
      </div>

      {chatMessages.length === 0 && (
        <div className="flex-1 flex flex-col items-center justify-center">
          <p className="text-lg font-medium text-slate-900 mb-6">Ask something about your reports</p>
          <SuggestedQuestion onClick={handleSend} />
        </div>
      )}

      <div className={`flex flex-col ${chatMessages.length === 0 ? "" : "flex-1 min-h-0"}`}>
        {chatMessages.length > 0 && <ChatWindow messages={chatMessages} />}
        <div className="mt-auto pt-4">
          <ChatInput onSend={handleSend} />
        </div>
      </div>
    </div>
  );
}