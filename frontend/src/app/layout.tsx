import type { Metadata } from "next";
import { LocaleProvider } from "@/lib/locale-context";
import "./globals.css";

export const metadata: Metadata = {
  title: "PDF Invoice Extraction Pipeline | Sekimosoft",
  description:
    "Extract text from text-based PDFs and structured invoice fields from supported demo templates.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <LocaleProvider>{children}</LocaleProvider>
      </body>
    </html>
  );
}
