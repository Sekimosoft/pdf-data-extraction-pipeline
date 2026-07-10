"use client";

import { useState } from "react";
import type { ExtractResponse } from "@/lib/api";
import { documentToCsv } from "@/lib/api";
import { useLocale } from "@/lib/locale-context";
import { getMessages, validationStateLabel } from "@/lib/i18n";
import { colors, wrapText } from "@/lib/theme";

type Props = {
  response: ExtractResponse;
};

function stateColor(state: string): string {
  if (state === "valid") return colors.success;
  if (state === "warning") return colors.warning;
  return colors.danger;
}

export function ResultPanel({ response }: Props) {
  const { locale } = useLocale();
  const t = getMessages(locale);
  const [copyNote, setCopyNote] = useState("");

  if (response.resultMode === "text_preview" && response.textPreview) {
    const preview = response.textPreview;
    return (
      <div style={{ display: "grid", gap: "1rem", minWidth: 0, maxWidth: "100%" }}>
        <h2 style={{ margin: 0, fontSize: "1.125rem" }}>{t.textPreviewResult}</h2>
        {response.notice && (
          <p
            role="status"
            style={{
              margin: 0,
              padding: "0.75rem 1rem",
              borderRadius: 8,
              background: colors.surfaceAlt,
              border: `1px solid ${colors.border}`,
              color: colors.text,
              ...wrapText,
            }}
          >
            {response.notice}
          </p>
        )}
        <dl
          style={{
            display: "grid",
            gridTemplateColumns: "minmax(120px, 1fr) 2fr",
            gap: "0.5rem 1rem",
            margin: 0,
            minWidth: 0,
          }}
        >
          <Stat label={t.pageCount} value={String(preview.pageCount)} />
          <Stat label={t.characterCount} value={String(preview.characterCount)} />
          <Stat label={t.documentStatus} value={preview.documentStatus} />
        </dl>
        <div style={{ minWidth: 0 }}>
          <h3 style={{ margin: "0 0 0.5rem", fontSize: "1rem" }}>{t.textPreviewLabel}</h3>
          <pre style={previewStyle}>{preview.textPreview}</pre>
        </div>
      </div>
    );
  }

  const data = response.data;
  if (!data) return null;

  const fields: { key: keyof typeof data; label: string }[] = [
    { key: "documentType", label: t.documentType },
    { key: "invoiceNumber", label: t.invoiceNumber },
    { key: "issueDate", label: t.issueDate },
    { key: "dueDate", label: t.dueDate },
    { key: "vendorName", label: t.vendorName },
    { key: "customerName", label: t.customerName },
    { key: "subtotal", label: t.subtotal },
    { key: "tax", label: t.tax },
    { key: "total", label: t.total },
    { key: "currency", label: t.currency },
    { key: "confidence", label: t.confidence },
    { key: "validationState", label: t.validationState },
  ];

  const onCopyJson = async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(data, null, 2));
      setCopyNote(t.copied);
    } catch {
      setCopyNote(t.copyFailed);
    }
  };

  const onDownloadCsv = () => {
    const csv = documentToCsv(data);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "extracted-invoice.csv";
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ display: "grid", gap: "1rem", minWidth: 0, maxWidth: "100%" }}>
      <h2 style={{ margin: 0, fontSize: "1.125rem" }}>{t.structuredResult}</h2>

      {response.validationIssues.length > 0 && (
        <div
          role="alert"
          style={{
            border: `1px solid ${colors.warning}`,
            borderRadius: 8,
            padding: "0.75rem 1rem",
            background: colors.surfaceAlt,
          }}
        >
          <p style={{ margin: "0 0 0.5rem", fontWeight: 600 }}>{t.validationIssues}</p>
          <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
            {response.validationIssues.map((issue, index) => (
              <li key={`${issue.field}-${index}`} style={{ color: colors.muted, ...wrapText }}>
                {issue.message}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 140px), 1fr))",
          gap: "0.75rem",
          minWidth: 0,
        }}
      >
        {fields.map(({ key, label }) => {
          let value = data[key];
          if (key === "validationState") {
            value = validationStateLabel(locale, String(value));
          }
          return (
            <div
              key={key}
              style={{
                padding: "0.75rem",
                borderRadius: 8,
                background: colors.surfaceAlt,
                border: `1px solid ${colors.border}`,
                minWidth: 0,
              }}
            >
              <div style={{ fontSize: "0.75rem", color: colors.muted, marginBottom: 4 }}>{label}</div>
              <div
                style={{
                  fontWeight: key === "validationState" ? 600 : 400,
                  color: key === "validationState" ? stateColor(data.validationState) : colors.text,
                  ...wrapText,
                }}
              >
                {value ?? "—"}
              </div>
            </div>
          );
        })}
      </div>

      {response.success && (
        <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
          <button type="button" onClick={onCopyJson} style={buttonStyle}>
            {t.copyJson}
          </button>
          <button type="button" onClick={onDownloadCsv} style={buttonStyle}>
            {t.downloadCsv}
          </button>
        </div>
      )}
      {copyNote && <p style={{ margin: 0, color: colors.muted, fontSize: "0.875rem" }}>{copyNote}</p>}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <>
      <dt style={{ color: colors.muted, margin: 0 }}>{label}</dt>
      <dd style={{ margin: 0, ...wrapText }}>{value}</dd>
    </>
  );
}

const previewStyle: React.CSSProperties = {
  margin: 0,
  padding: "1rem",
  borderRadius: 8,
  background: "#0d1117",
  border: `1px solid ${colors.border}`,
  overflowX: "auto",
  maxWidth: "100%",
  whiteSpace: "pre-wrap",
  fontSize: "0.85rem",
  lineHeight: 1.5,
  ...wrapText,
};

const buttonStyle: React.CSSProperties = {
  background: colors.surfaceAlt,
  border: `1px solid ${colors.border}`,
  color: colors.text,
  borderRadius: 8,
  padding: "0.55rem 1rem",
  cursor: "pointer",
};
