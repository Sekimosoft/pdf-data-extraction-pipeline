"use client";

import { useState } from "react";
import { UploadForm } from "@/components/UploadForm";
import { ResultPanel } from "@/components/ResultPanel";
import { LanguageToggle } from "@/components/LanguageToggle";
import { useLocale } from "@/lib/locale-context";
import { getMessages } from "@/lib/i18n";
import type { ExtractResponse } from "@/lib/api";
import { colors, layout, wrapText } from "@/lib/theme";

export function HomePage() {
  const { locale } = useLocale();
  const t = getMessages(locale);
  const [response, setResponse] = useState<ExtractResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleResult = (result: ExtractResponse) => {
    setResponse(result);
    if (result.resultMode === "extraction_error") {
      setError(result.validationIssues[0]?.message ?? t.errExtractionFailed);
      return;
    }
    if (result.resultMode === "invoice_structured" && !result.success) {
      setError(t.errValidationFailed);
      return;
    }
    setError("");
  };

  const showResult =
    response &&
    (response.resultMode === "text_preview" ||
      (response.resultMode === "invoice_structured" && response.data));

  return (
    <main style={layout.page}>
      <div style={layout.container}>
        <header style={{ marginBottom: "2rem" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-start",
              gap: "1rem",
              flexWrap: "wrap",
              marginBottom: "0.5rem",
            }}
          >
            <p style={{ color: colors.accent, fontWeight: 600, margin: 0, fontSize: "0.875rem" }}>
              {t.brand}
            </p>
            <LanguageToggle />
          </div>
          <h1 style={{ margin: "0 0 0.75rem", fontSize: "clamp(1.75rem, 4vw, 2.25rem)" }}>
            {t.title}
          </h1>
          <p style={{ color: colors.muted, margin: 0, maxWidth: 640, lineHeight: 1.6, ...wrapText }}>
            {t.description}
          </p>
        </header>

        <div
          style={{
            margin: "0 0 1.5rem",
            padding: "0.75rem 1rem",
            background: colors.surfaceAlt,
            border: `1px solid ${colors.border}`,
            borderRadius: 8,
            color: colors.muted,
            fontSize: "0.875rem",
          }}
        >
          <p style={{ margin: "0 0 0.5rem", fontWeight: 600, color: colors.text }}>{t.scopeTitle}</p>
          <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
            <li>{t.scopeTextBased}</li>
            <li>{t.scopeNoOcr}</li>
            <li>{t.scopeInvoiceTemplates}</li>
            <li>{t.scopeTextPreview}</li>
          </ul>
        </div>

        <p
          style={{
            margin: "0 0 1.5rem",
            padding: "0.75rem 1rem",
            background: colors.surfaceAlt,
            border: `1px solid ${colors.border}`,
            borderRadius: 8,
            color: colors.muted,
            fontSize: "0.875rem",
            ...wrapText,
          }}
        >
          {t.demoNotice}
        </p>

        <div style={{ display: "grid", gap: "1.5rem", minWidth: 0, maxWidth: "100%" }}>
          <section style={layout.card}>
            <h2 style={{ margin: "0 0 1rem", fontSize: "1.125rem" }}>{t.sectionUpload}</h2>
            <UploadForm onResult={handleResult} onError={setError} onLoading={setLoading} />
            {loading && (
              <p style={{ color: colors.muted, marginTop: "1rem", marginBottom: 0 }} role="status">
                {t.extracting}
              </p>
            )}
            {error && (
              <p style={{ color: colors.danger, marginTop: "1rem", marginBottom: 0, ...wrapText }} role="alert">
                {error}
              </p>
            )}
          </section>

          {showResult && (
            <section style={layout.card}>
              <ResultPanel response={response} />
            </section>
          )}
        </div>

        <footer style={{ marginTop: "2.5rem", color: colors.muted, fontSize: "0.875rem", ...wrapText }}>
          {t.footer}
        </footer>
      </div>
    </main>
  );
}
