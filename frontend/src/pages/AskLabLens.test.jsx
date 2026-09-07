import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import AskLabLens from "./AskLabLens";
import Trends from "./Trends";
import * as appContext from "../context/AppContext";

vi.mock("../context/AppContext", () => ({
  useApp: () => ({
    chatMessages: [],
    addChatMessage: vi.fn(),
    selectedPatientId: 7,
  }),
}));

describe("patient-scoped chat and trends", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("sends the active patient id with the Ask LabLens request", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: async () => ({ answer: "Latest HbA1c is 5.8.", citations: [] }),
    });

    render(<AskLabLens />);
    fireEvent.change(screen.getByPlaceholderText("Ask about your lab results..."), { target: { value: "What is my HbA1c?" } });
    fireEvent.click(screen.getByLabelText("Send message"));

    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
    expect(fetchMock.mock.calls[0][1].body).toContain('"patient_id":7');
  });

  it("requests trends for the active patient instead of the demo patient", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: async () => ({ tests: ["HbA1c"], data: { HbA1c: [{ date: "2026-01-01", value: 5.6 }] } }),
    });

    render(<Trends />);

    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
    expect(fetchMock.mock.calls[0][0]).toBe("/api/trends?patient_id=7");
  });
});
