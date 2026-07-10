import { describe, expect, it } from "vitest";
import { DEFAULT_LOCALE, getMessages, validationStateLabel } from "@/lib/i18n";
import { documentToCsv, type ExtractedDocument } from "@/lib/api";

describe("i18n", () => {
  it("defaults to English", () => {
    expect(DEFAULT_LOCALE).toBe("en");
    expect(getMessages("en").extractButton).toBe("Extract data");
  });

  it("switches to Japanese", () => {
    expect(getMessages("ja").extractButton).toBe("データを抽出");
  });

  it("maps validation state labels", () => {
    expect(validationStateLabel("en", "valid")).toBe("Valid");
    expect(validationStateLabel("ja", "warning")).toBe("警告");
  });
});

describe("documentToCsv", () => {
  it("exports CSV with headers", () => {
    const doc: ExtractedDocument = {
      documentType: "invoice",
      invoiceNumber: "INV-1",
      issueDate: "2026-01-01",
      dueDate: "2026-02-01",
      vendorName: "V",
      customerName: "C",
      subtotal: 100,
      tax: 10,
      total: 110,
      currency: "JPY",
      confidence: 0.9,
      validationState: "valid",
    };
    const csv = documentToCsv(doc);
    expect(csv).toContain("invoiceNumber");
    expect(csv).toContain("INV-1");
  });
});
