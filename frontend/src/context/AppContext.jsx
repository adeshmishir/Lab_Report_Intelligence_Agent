import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { correctResult, getReport, listReports, normalizeReport, uploadReport } from "../api/client";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [reports, setReports] = useState([]);
  const [trendData] = useState({});
  const [chatMessages, setChatMessages] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [reportsLoading, setReportsLoading] = useState(true);
  const [error, setError] = useState(null);

  const refreshReports = useCallback(async () => {
    setReportsLoading(true);
    try {
      const payload = await listReports();
      setReports(payload.map(normalizeReport));
      setError(null);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setReportsLoading(false);
    }
  }, []);

  const fetchReport = useCallback(async (reportId) => normalizeReport(await getReport(reportId)), []);

  useEffect(() => {
    refreshReports();
  }, []);

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
    reportsLoading,
    error,
    refreshReports,
    uploadReport,
    correctResult,
    getReport: fetchReport,
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
