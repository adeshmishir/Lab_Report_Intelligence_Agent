import { useState, useCallback } from "react";
import { Upload, CheckCircle, AlertCircle, FileText } from "lucide-react";
import { Button } from "../common/Button";

const ACCEPTED = ["application/pdf", "image/jpeg", "image/png"];
const ACCEPTED_LABELS = ["PDF", "JPG", "PNG"];

export function UploadReport({ onUploaded }) {
  const [state, setState] = useState("idle");
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [patientName, setPatientName] = useState("");

  const handleFile = useCallback((file) => {
    if (!file) return;
    if (!ACCEPTED.includes(file.type)) {
      setState("error");
      setErrorMessage("Please use a PDF, JPG, or PNG file.");
      setSelectedFile(null);
      return;
    }
    setSelectedFile(file);
    setErrorMessage("");
    setState("selected");
  }, []);

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files?.[0];
      handleFile(file);
    },
    [handleFile]
  );

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setDragOver(false);
  }, []);

  const handleUpload = useCallback(async () => {
    setState("uploading");
    try {
      const response = await fetch("/api/reports/upload", {
        method: "POST",
        body: (() => {
          const data = new FormData();
          data.append("file", selectedFile);
          if (patientName.trim()) data.append("patient_name", patientName.trim());
          return data;
        })(),
      }).then(async (response) => {
        const payload = await response.json().catch(() => ({}));
        if (!response.ok) {
          const error = new Error(payload?.error?.message || "Upload failed.");
          error.status = response.status;
          error.code = payload?.error?.code;
          throw error;
        }
        return payload;
      });
      setState("syncing");
      await onUploaded?.(response);
      setState("success");
      window.setTimeout(() => {
        setState("idle");
        setSelectedFile(null);
        setPatientName("");
      }, 3000);
    } catch (error) {
      setErrorMessage(error.message);
      if (error.code === "DUPLICATE_REPORT" || error.status === 409) {
        setState("duplicate");
      } else if (error.message.includes("does not contain a patient name")) {
        setState("needs-name");
      } else {
        setState("error");
        setSelectedFile(null);
      }
    }
  }, [onUploaded, patientName, selectedFile]);

  const handleReset = useCallback(() => {
    setState("idle");
    setSelectedFile(null);
    setErrorMessage("");
    setPatientName("");
  }, []);

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6">
      <h3 className="text-sm font-semibold text-slate-900">Add a lab report</h3>
      <p className="mt-1 text-xs text-slate-500">Upload a sample report to extract and compare your results.</p>

      <div className="mt-4 flex items-center gap-2">
        {ACCEPTED_LABELS.map((label) => (
          <span key={label} className="text-xs text-slate-400 font-medium">{label}</span>
        ))}
      </div>

      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`mt-3 rounded-lg border-2 border-dashed transition-colors ${
          dragOver
            ? "border-slate-400 bg-slate-50"
            : state === "error"
            ? "border-red-300 bg-red-50"
            : state === "success"
            ? "border-emerald-300 bg-emerald-50"
            : "border-slate-200 hover:border-slate-300"
        }`}
      >
        <div className="flex flex-col items-center justify-center py-8 px-4">
          {state === "success" ? (
            <>
              <CheckCircle className="h-8 w-8 text-emerald-500 mb-2" />
              <p className="text-sm font-medium text-emerald-700">Report uploaded successfully</p>
            </>
          ) : state === "duplicate" ? (
            <>
              <AlertCircle className="h-8 w-8 text-amber-400 mb-2" />
              <p className="text-sm font-medium text-amber-700">Report already uploaded</p>
              <p className="mt-1 text-center text-xs text-amber-600">This exact file is already stored for this patient.</p>
              <button onClick={handleReset} className="mt-3 text-xs text-slate-600 underline hover:text-slate-800">
                Choose another report
              </button>
            </>
          ) : state === "error" ? (
            <>
              <AlertCircle className="h-8 w-8 text-red-400 mb-2" />
              <p className="text-sm font-medium text-red-700">Upload failed</p>
              <p className="text-xs text-red-500 mt-1">{errorMessage}</p>
              <button onClick={handleReset} className="mt-3 text-xs text-red-600 underline hover:text-red-700">
                Try again
              </button>
            </>
          ) : state === "needs-name" && selectedFile ? (
            <>
              <AlertCircle className="h-8 w-8 text-amber-400 mb-2" />
              <p className="text-sm font-medium text-slate-800">Patient name not found</p>
              <p className="mt-1 text-center text-xs text-slate-500">Enter the name to file this report correctly.</p>
              <input
                autoFocus
                value={patientName}
                onChange={(event) => setPatientName(event.target.value)}
                placeholder="Patient name"
                className="mt-3 w-full max-w-xs rounded-md border border-slate-200 px-3 py-2 text-sm"
              />
              <div className="mt-3 flex gap-2">
                <Button size="sm" onClick={handleUpload} disabled={!patientName.trim()}>Upload report</Button>
                <Button size="sm" variant="ghost" onClick={handleReset}>Cancel</Button>
              </div>
            </>
          ) : state === "uploading" || state === "syncing" ? (
            <>
              <div className="h-8 w-8 rounded-full border-2 border-slate-300 border-t-slate-600 animate-spin mb-2" />
              <p className="text-sm text-slate-500">
                {state === "syncing" ? "Updating patient reports..." : "Uploading..."}
              </p>
            </>
          ) : state === "selected" && selectedFile ? (
            <>
              <FileText className="h-8 w-8 text-slate-400 mb-2" />
              <p className="text-sm font-medium text-slate-700">{selectedFile.name}</p>
              <p className="text-xs text-slate-400 mt-1">
                {(selectedFile.size / 1024).toFixed(1)} KB
              </p>
              <div className="flex gap-2 mt-3">
                <Button size="sm" onClick={handleUpload}>Upload</Button>
                <Button size="sm" variant="ghost" onClick={handleReset}>Cancel</Button>
              </div>
            </>
          ) : (
            <>
              <Upload className="h-8 w-8 text-slate-400 mb-2" />
              <p className="text-sm font-medium text-slate-700">Drop your report here</p>
              <p className="text-xs text-slate-400 mt-1">
                or{" "}
                <label className="underline cursor-pointer text-slate-600 hover:text-slate-800">
                  choose a file
                  <input
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png"
                    className="sr-only"
                    onChange={(e) => handleFile(e.target.files?.[0])}
                  />
                </label>
              </p>
            </>
          )}
        </div>
      </div>

      <p className="mt-3 text-xs text-slate-400">PDF, JPG or PNG · Sample reports only</p>
    </div>
  );
}