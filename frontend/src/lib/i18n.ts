export type Locale = "en" | "ja";

export const DEFAULT_LOCALE: Locale = "en";

export type Messages = {
  brand: string;
  title: string;
  description: string;
  demoNotice: string;
  sectionUpload: string;
  dropHint: string;
  browseFiles: string;
  supportedFormat: string;
  fileSizeLimit: string;
  selectedFile: string;
  removeFile: string;
  downloadSample: string;
  extractButton: string;
  extracting: string;
  validationIssues: string;
  structuredResult: string;
  documentType: string;
  invoiceNumber: string;
  issueDate: string;
  dueDate: string;
  vendorName: string;
  customerName: string;
  subtotal: string;
  tax: string;
  total: string;
  currency: string;
  confidence: string;
  validationState: string;
  copyJson: string;
  downloadCsv: string;
  copied: string;
  copyFailed: string;
  footer: string;
  errNoFile: string;
  errInvalidType: string;
  errTooLarge: string;
  errUnexpected: string;
  stateValid: string;
  stateWarning: string;
  stateError: string;
  langSwitchLabel: string;
  langEn: string;
  langJa: string;
};

const en: Messages = {
  brand: "Sekimosoft · Portfolio Demo",
  title: "PDF Data Extraction Pipeline",
  description:
    "Upload a text-based PDF invoice and get validated structured fields — ready to copy as JSON or export as CSV.",
  demoNotice:
    "Demo only. Do not upload real customer documents. Files are processed in memory and not stored.",
  sectionUpload: "1. Upload PDF",
  dropHint: "Drag and drop a PDF here",
  browseFiles: "Browse files",
  supportedFormat: "Supported: text-based PDF only (no scanned images)",
  fileSizeLimit: "Max file size: 5 MB",
  selectedFile: "Selected file",
  removeFile: "Remove",
  downloadSample: "Download sample PDF",
  extractButton: "Extract data",
  extracting: "Extracting…",
  validationIssues: "Validation issues",
  structuredResult: "Structured result",
  documentType: "Document type",
  invoiceNumber: "Invoice number",
  issueDate: "Issue date",
  dueDate: "Due date",
  vendorName: "Vendor",
  customerName: "Customer",
  subtotal: "Subtotal",
  tax: "Tax",
  total: "Total",
  currency: "Currency",
  confidence: "Confidence",
  validationState: "Validation state",
  copyJson: "Copy JSON",
  downloadCsv: "Download CSV",
  copied: "Copied to clipboard",
  copyFailed: "Copy failed — select JSON manually",
  footer:
    "V1 supports a single synthetic invoice template. Not a universal AI PDF parser. Built by Sekimosoft.",
  errNoFile: "Select a PDF file first",
  errInvalidType: "Only PDF files are supported",
  errTooLarge: "File exceeds 5 MB limit",
  errUnexpected: "Extraction failed — try the sample PDF",
  stateValid: "Valid",
  stateWarning: "Warning",
  stateError: "Error",
  langSwitchLabel: "Language",
  langEn: "EN",
  langJa: "JP",
};

const ja: Messages = {
  brand: "Sekimosoft · ポートフォリオデモ",
  title: "PDF Data Extraction Pipeline",
  description:
    "テキストベースのPDF請求書をアップロードし、検証済みの構造化フィールドをJSONコピーまたはCSV出力できます。",
  demoNotice:
    "デモ用途のみ。実顧客の書類はアップロードしないでください。ファイルはメモリ上で処理され、保存されません。",
  sectionUpload: "1. PDFをアップロード",
  dropHint: "PDFをここにドラッグ＆ドロップ",
  browseFiles: "ファイルを選択",
  supportedFormat: "対応: テキストベースPDFのみ（スキャン画像不可）",
  fileSizeLimit: "最大ファイルサイズ: 5 MB",
  selectedFile: "選択中のファイル",
  removeFile: "削除",
  downloadSample: "サンプルPDFをダウンロード",
  extractButton: "データを抽出",
  extracting: "抽出中…",
  validationIssues: "検証結果",
  structuredResult: "構造化結果",
  documentType: "書類種別",
  invoiceNumber: "請求書番号",
  issueDate: "発行日",
  dueDate: "支払期日",
  vendorName: "請求元",
  customerName: "請求先",
  subtotal: "小計",
  tax: "税",
  total: "合計",
  currency: "通貨",
  confidence: "信頼度",
  validationState: "検証状態",
  copyJson: "JSONをコピー",
  downloadCsv: "CSVをダウンロード",
  copied: "クリップボードにコピーしました",
  copyFailed: "コピーに失敗しました — JSONを手動で選択してください",
  footer:
    "V1は合成請求書テンプレート1種のみ対応。万能AI PDFパーサーではありません。Sekimosoft制作。",
  errNoFile: "PDFファイルを選択してください",
  errInvalidType: "PDFファイルのみ対応しています",
  errTooLarge: "ファイルサイズが5 MBを超えています",
  errUnexpected: "抽出に失敗しました — サンプルPDFをお試しください",
  stateValid: "正常",
  stateWarning: "警告",
  stateError: "エラー",
  langSwitchLabel: "言語",
  langEn: "EN",
  langJa: "JP",
};

const dictionaries: Record<Locale, Messages> = { en, ja };

export function getMessages(locale: Locale): Messages {
  return dictionaries[locale] ?? en;
}

export function validationStateLabel(locale: Locale, state: string): string {
  const t = getMessages(locale);
  if (state === "valid") return t.stateValid;
  if (state === "warning") return t.stateWarning;
  return t.stateError;
}
