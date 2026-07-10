"use client";

import { useRef, useState, type DragEvent } from "react";
import { extractPdf, samplePdfUrl } from "@/lib/api";
import type { ExtractResponse } from "@/lib/api";
import { useLocale } from "@/lib/locale-context";
import { getMessages } from "@/lib/i18n";
import { colors, MAX_FILE_SIZE_MB } from "@/lib/theme";

type Props = {
  onResult: (response: ExtractResponse) => void;
  onError: (message: string) => void;
  onLoading: (loading: boolean) => void;
};

export function UploadForm({ onResult, onError, onLoading }: Props) {
  const { locale } = useLocale();
  const t = getMessages(locale);
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);

  const validateFile = (candidate: File): string | null => {
    if (!candidate.name.toLowerCase().endsWith(".pdf")) {
      return t.errInvalidType;
    }
    if (candidate.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
      return t.errTooLarge;
    }
    return null;
  };

  const handleFile = (candidate: File | null) => {
    onError("");
    if (!candidate) {
      setFile(null);
      return;
    }
    const err = validateFile(candidate);
    if (err) {
      onError(err);
      setFile(null);
      return;
    }
    setFile(candidate);
  };

  const onDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragOver(false);
    const dropped = event.dataTransfer.files?.[0];
    if (dropped) handleFile(dropped);
  };

  const onSubmit = async () => {
    if (!file) {
      onError(t.errNoFile);
      return;
    }
    onLoading(true);
    onError("");
    try {
      const result = await extractPdf(file, locale);
      onResult(result);
    } catch (err) {
      onError(err instanceof Error ? err.message : t.errExtractionFailed);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div style={{ display: "grid", gap: "1rem", minWidth: 0, maxWidth: "100%" }}>
      <div
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") inputRef.current?.click();
        }}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        style={{
          border: `2px dashed ${dragOver ? colors.accent : colors.border}`,
          borderRadius: 8,
          padding: "2rem 1rem",
          textAlign: "center",
          cursor: "pointer",
          background: dragOver ? colors.surfaceAlt : "transparent",
        }}
      >
        <p style={{ margin: "0 0 0.5rem", fontWeight: 600 }}>{t.dropHint}</p>
        <p style={{ margin: 0, color: colors.muted, fontSize: "0.875rem" }}>{t.browseFiles}</p>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf,.pdf"
          style={{ display: "none" }}
          onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
        />
      </div>

      <p style={{ margin: 0, color: colors.muted, fontSize: "0.875rem" }}>
        {t.supportedFormat} · {t.fileSizeLimit}
      </p>

      {file && (
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: "0.75rem",
            flexWrap: "wrap",
          }}
        >
          <span style={{ overflowWrap: "anywhere" }}>
            {t.selectedFile}: <strong>{file.name}</strong>
          </span>
          <button type="button" onClick={() => handleFile(null)} style={secondaryButtonStyle}>
            {t.removeFile}
          </button>
        </div>
      )}

      <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
        <button type="button" onClick={onSubmit} style={primaryButtonStyle}>
          {t.extractButton}
        </button>
        <a href={samplePdfUrl(locale)} download style={linkStyle}>
          {t.downloadSample}
        </a>
      </div>
    </div>
  );
}

const primaryButtonStyle: React.CSSProperties = {
  background: colors.accent,
  color: "#042f2e",
  border: "none",
  borderRadius: 8,
  padding: "0.65rem 1.25rem",
  fontWeight: 600,
  cursor: "pointer",
};

const secondaryButtonStyle: React.CSSProperties = {
  background: "transparent",
  border: `1px solid ${colors.border}`,
  color: colors.muted,
  borderRadius: 6,
  padding: "0.35rem 0.75rem",
  cursor: "pointer",
};

const linkStyle: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  color: colors.accent,
  textDecoration: "none",
  fontSize: "0.875rem",
};
