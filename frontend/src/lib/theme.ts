import type { CSSProperties } from "react";

export const colors = {
  bg: "#0c1210",
  surface: "#152019",
  surfaceAlt: "#1c2a22",
  border: "#2a4034",
  text: "#e6f0ea",
  muted: "#8fa89a",
  accent: "#14b8a6",
  accentHover: "#0d9488",
  success: "#22c55e",
  warning: "#eab308",
  danger: "#f87171",
};

export const layout: Record<string, CSSProperties> = {
  page: {
    minHeight: "100vh",
    width: "100%",
    background: `linear-gradient(145deg, ${colors.bg} 0%, #111916 45%, ${colors.bg} 100%)`,
    color: colors.text,
    fontFamily: "'Segoe UI', system-ui, -apple-system, sans-serif",
  },
  container: {
    width: "100%",
    maxWidth: 920,
    minWidth: 0,
    margin: "0 auto",
    padding: "2rem clamp(1rem, 3vw, 1.25rem) 4rem",
    boxSizing: "border-box",
  },
  card: {
    width: "100%",
    minWidth: 0,
    maxWidth: "100%",
    background: colors.surface,
    border: `1px solid ${colors.border}`,
    borderRadius: 10,
    padding: "1.5rem",
    boxSizing: "border-box",
  },
};

export const wrapText: CSSProperties = {
  overflowWrap: "anywhere",
  wordBreak: "break-word",
};

export const MAX_FILE_SIZE_MB = 5;
