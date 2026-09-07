import { useState } from "react";
import { useApp } from "../context/AppContext";
import { ChatWindow } from "../components/chat/ChatWindow";
import { ChatInput } from "../components/chat/ChatInput";
import { SuggestedQuestion } from "../components/chat/SuggestedQuestion";

export default function AskLabLens() {
  const {
    chatMessages,
    addChatMessage,
    clearChatMessages = () => {},
    selectedPatientId,
    setSelectedPatientId = () => {},
    patients = [],
  } = useApp();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const selectedPatient = patients.find((patient) => patient.id === selectedPatientId);

  const handleSend = async (question) => {
    if (!selectedPatientId) {
      setError("Choose a patient before asking about their reports.");
      return;
    }
    setError(null);
    addChatMessage({ role: "user", content: question });
    setLoading(true);
    try {
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, patient_id: selectedPatientId }),
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload?.error?.message || "LabLens could not answer that question.");
      }
      addChatMessage({
        role: "assistant",
        content: payload.answer,
        citations: payload.citations,
        safetyNotice: payload.safety_notice,
      });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">Ask LabLens</h1>
        <p className="mt-1 text-sm text-slate-500">
          Ask questions about your uploaded reports. Answers will be grounded in your report data.
        </p>
        <div className="mt-4 flex flex-wrap items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2">
          <label htmlFor="ask-patient" className="text-xs font-medium text-slate-500">Ask about</label>
          <select
            id="ask-patient"
            value={selectedPatientId || ""}
            onChange={(event) => {
              setSelectedPatientId(Number(event.target.value));
              clearChatMessages();
              setError(null);
            }}
            className="rounded-md border border-slate-200 bg-white px-2 py-1 text-sm text-slate-700"
          >
            {patients.map((patient) => <option key={patient.id} value={patient.id}>{patient.name}</option>)}
          </select>
          <span className="text-xs text-slate-400">Only {selectedPatient?.name || "this patient"}&apos;s reports will be used.</span>
        </div>
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
          {error && <p className="mb-3 text-sm text-red-600">{error}</p>}
          <ChatInput onSend={handleSend} disabled={loading} />
        </div>
      </div>
    </div>
  );
}