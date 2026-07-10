"use client";

import { useLocale } from "@/lib/locale-context";
import { getMessages } from "@/lib/i18n";
import { colors } from "@/lib/theme";

export function LanguageToggle() {
  const { locale, setLocale } = useLocale();
  const t = getMessages(locale);

  const buttonStyle = (active: boolean) => ({
    padding: "0.35rem 0.75rem",
    border: `1px solid ${active ? colors.accent : colors.border}`,
    background: active ? colors.surfaceAlt : "transparent",
    color: active ? colors.text : colors.muted,
    borderRadius: 6,
    cursor: "pointer" as const,
    fontWeight: active ? 600 : 400,
  });

  return (
    <div role="group" aria-label={t.langSwitchLabel} style={{ display: "flex", gap: "0.35rem" }}>
      <button type="button" style={buttonStyle(locale === "en")} onClick={() => setLocale("en")}>
        {t.langEn}
      </button>
      <button type="button" style={buttonStyle(locale === "ja")} onClick={() => setLocale("ja")}>
        {t.langJa}
      </button>
    </div>
  );
}
