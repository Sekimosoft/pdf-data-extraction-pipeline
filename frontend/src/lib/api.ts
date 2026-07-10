const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type ValidationIssue = {
  field: string;
  message: string;
  severity: "error" | "warning";
};

export type ExtractedDocument = {
  documentType: string | null;
  invoiceNumber: string | null;
  issueDate: string | null;
  dueDate: string | null;
  vendorName: string | null;
  customerName: string | null;
  subtotal: number | null;
  tax: number | null;
  total: number | null;
  currency: string | null;
  confidence: number;
  validationState: "valid" | "warning" | "error";
};

export type TextPreview = {
  pageCount: number;
  characterCount: number;
  textPreview: string;
  documentStatus: string;
};

export type ExtractResponse = {
  success: boolean;
  resultMode: "invoice_structured" | "text_preview" | "extraction_error";
  data: ExtractedDocument | null;
  textPreview: TextPreview | null;
  notice: string | null;
  validationIssues: ValidationIssue[];
  provider: string;
  locale: "en" | "ja";
};

export async function extractPdf(file: File, locale: "en" | "ja"): Promise<ExtractResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("locale", locale);

  const response = await fetch(`${API_BASE}/api/v1/extract`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(typeof body.detail === "string" ? body.detail : "Request failed");
  }

  return response.json();
}

export function samplePdfUrl(locale: "en" | "ja"): string {
  return `${API_BASE}/api/v1/sample-pdf?locale=${locale}`;
}

export function documentToCsv(doc: ExtractedDocument): string {
  const headers = [
    "documentType",
    "invoiceNumber",
    "issueDate",
    "dueDate",
    "vendorName",
    "customerName",
    "subtotal",
    "tax",
    "total",
    "currency",
    "confidence",
    "validationState",
  ];
  const row = headers.map((key) => {
    const value = doc[key as keyof ExtractedDocument];
    const text = value === null || value === undefined ? "" : String(value);
    return `"${text.replace(/"/g, '""')}"`;
  });
  return `${headers.join(",")}\n${row.join(",")}\n`;
}
