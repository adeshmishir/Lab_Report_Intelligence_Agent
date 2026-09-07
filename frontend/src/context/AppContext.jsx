import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { correctResult, createPatient, getReport, listPatients, listReports, normalizeReport, uploadReport } from "../api/client";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [reports, setReports] = useState([]);
  const [trendData] = useState({});
  const [chatMessages, setChatMessages] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [reportsLoading, setReportsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [patients, setPatients] = useState([]);
  const [selectedPatientId, setSelectedPatientId] = useState(() => Number(localStorage.getItem("lablens_patient_id")) || 1);

  const refreshPatients = useCallback(async () => {
    const loadedPatients = await listPatients();
    setPatients(loadedPatients);
    return loadedPatients;
  }, []);

  const refreshReports = useCallback(async () => {
    setReportsLoading(true);
    try {
      const payload = await listReports(selectedPatientId);
      setReports(payload.map(normalizeReport));
      setError(null);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setReportsLoading(false);
    }
  }, [selectedPatientId]);

  const fetchReport = useCallback(async (reportId) => normalizeReport(await getReport(reportId, selectedPatientId)), [selectedPatientId]);

  useEffect(() => {
    refreshPatients().then((loadedPatients) => {
      if (!loadedPatients.some((patient) => patient.id === selectedPatientId) && loadedPatients[0]) {
        setSelectedPatientId(loadedPatients[0].id);
      }
    }).catch((requestError) => setError(requestError.message));
  }, [refreshPatients, selectedPatientId]);

  useEffect(() => {
    localStorage.setItem("lablens_patient_id", String(selectedPatientId));
    refreshReports();
  }, [selectedPatientId, refreshReports]);

  const addChatMessage = (message) => {
    setChatMessages((prev) => [...prev, message]);
  };

  const clearChatMessages = () => setChatMessages([]);

  const value = {
    reports,
    trendData,
    chatMessages,
    selectedReport,
    loading,
    setSelectedReport,
    setLoading,
    addChatMessage,
    clearChatMessages,
    reportsLoading,
    error,
    refreshReports,
    uploadReport,
    correctResult,
    getReport: fetchReport,
    patients,
    refreshPatients,
    selectedPatientId,
    setSelectedPatientId,
    createPatient,
    uploadForPatient: (file) => uploadReport(file),
    correctPatientResult: (reportId, resultId, value, reason) => correctResult(reportId, resultId, value, reason, selectedPatientId),
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
