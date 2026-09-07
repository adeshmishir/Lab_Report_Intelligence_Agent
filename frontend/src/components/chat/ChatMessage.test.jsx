import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ChatMessage } from "./ChatMessage";

describe("ChatMessage", () => {
  it("renders assistant markdown as formatted content", () => {
    render(
      <ChatMessage
        message={{
          role: "assistant",
          content: "**HbA1c**\n\n| Date | Value |\n| --- | --- |\n| 2026-08-12 | 5.9% |",
        }}
      />,
    );

    expect(screen.getByText("HbA1c")).toBeInTheDocument();
    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByText("5.9%")).toBeInTheDocument();
  });
});