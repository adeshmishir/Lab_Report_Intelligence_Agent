import { createContext, useContext, useState } from "react";
import { demoReports, demoTrendData } from "../data/demoData";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [reports] = useState(demoReports);
  const [trendData] = useState(demoTrendData);
  const [chatMessages, setChatMessages] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const addChatMessage = (message) => {
    setChatMessages((prev) => [...prev, message]);
  };

  const value = {
    reports,
    trendData,
    chatMessages,
    selectedReport,
    loading,
    setSelectedReport,
    setLoading,
    addChatMessage,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
}
