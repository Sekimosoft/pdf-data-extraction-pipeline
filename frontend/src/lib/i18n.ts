export type Locale = "en" | "ja";

export const DEFAULT_LOCALE: Locale = "en";

export type Messages = {
  brand: string;
  title: string;
  description: string;
  scopeTitle: string;
  scopeTextBased: string;
  scopeNoOcr: string;
  scopeInvoiceTemplates: string;
  scopeTextPreview: string;
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
  textPreviewResult: string;
  pageCount: string;
  characterCount: string;
  documentStatus: string;
  textPreviewLabel: string;
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
  errExtractionFailed: string;
  errValidationFailed: string;
  stateValid: string;
  stateWarning: string;
  stateError: string;
  langSwitchLabel: string;
  langEn: string;
  langJa: string;
};

const en: Messages = {
  brand: "Sekimosoft · Portfolio Demo",
  title: "PDF Invoice Extraction Pipeline",
  description:
    "Extract text from any text-based PDF and structured fields from supported invoice templates.",
  scopeTitle: "Supported scope (V1.1)",
  scopeTextBased: "Text-based PDFs only",
  scopeNoOcr: "No scanned images / OCR",
  scopeInvoiceTemplates: "Structured invoice extraction supports demo EN/JP invoice templates",
  scopeTextPreview: "Other text PDFs receive a text extraction preview — not structured invoice fields",
  demoNotice:
    "Demo only. Do not upload real customer documents. Files are processed in memory and not stored.",
  sectionUpload: "1. Upload PDF",
  dropHint: "Drag and drop a PDF here",
  browseFiles: "Browse files",
  supportedFormat: "Text-based PDF only (no scanned images)",
  fileSizeLimit: "Max file size: 5 MB",
  selectedFile: "Selected file",
  removeFile: "Remove",
  downloadSample: "Download sample invoice PDF",
  extractButton: "Extract data",
  extracting: "Extracting…",
  validationIssues: "Validation issues",
  structuredResult: "Structured invoice result",
  textPreviewResult: "Text extraction preview",
  pageCount: "Page count",
  characterCount: "Character count",
  documentStatus: "Document status",
  textPreviewLabel: "Text preview",
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
    "Not a universal AI PDF parser. Invoice templates are synthetic demo fixtures only. Built by Sekimosoft.",
  errNoFile: "Select a PDF file first",
  errInvalidType: "Only PDF files are supported",
  errTooLarge: "File exceeds 5 MB limit",
  errExtractionFailed: "Could not extract text from this PDF — scanned documents are not supported in V1",
  errValidationFailed: "Invoice validation failed — check the issues below or try the sample invoice PDF",
  stateValid: "Valid",
  stateWarning: "Warning",
  stateError: "Error",
  langSwitchLabel: "Language",
  langEn: "EN",
  langJa: "JP",
};

const ja: Messages = {
  brand: "Sekimosoft · ポートフォリオデモ",
  title: "PDF請求書データ抽出パイプライン",
  description:
    "テキストPDFから内容を抽出し、対応する請求書形式は構造化データへ変換します。",
  scopeTitle: "対応範囲（V1.1）",
  scopeTextBased: "テキストベースPDFのみ",
  scopeNoOcr: "スキャン画像 / OCR非対応",
  scopeInvoiceTemplates: "構造化請求書抽出はデモ用EN/JP請求書テンプレートのみ",
  scopeTextPreview: "その他のテキストPDFはテキスト抽出プレビューを表示（請求書フィールドは出力しません）",
  demoNotice:
    "デモ用途のみ。実顧客の書類はアップロードしないでください。ファイルはメモリ上で処理され、保存されません。",
  sectionUpload: "1. PDFをアップロード",
  dropHint: "PDFをここにドラッグ＆ドロップ",
  browseFiles: "ファイルを選択",
  supportedFormat: "テキストベースPDFのみ（スキャン画像不可）",
  fileSizeLimit: "最大ファイルサイズ: 5 MB",
  selectedFile: "選択中のファイル",
  removeFile: "削除",
  downloadSample: "サンプル請求書PDFをダウンロード",
  extractButton: "データを抽出",
  extracting: "抽出中…",
  validationIssues: "検証結果",
  structuredResult: "構造化請求書結果",
  textPreviewResult: "テキスト抽出プレビュー",
  pageCount: "ページ数",
  characterCount: "文字数",
  documentStatus: "文書ステータス",
  textPreviewLabel: "テキストプレビュー",
  documentType: "書類種別",
  invoiceNumber: "請求書番号",
  issueDate: "発行日",
  dueDate: "支払期日",
  vendorName: "請求元",
  customerName: "請求先",
  subtotal: "小計",
  tax: "消費税",
  total: "合計",
  currency: "通貨",
  confidence: "信頼度",
  validationState: "検証状態",
  copyJson: "JSONをコピー",
  downloadCsv: "CSVをダウンロード",
  copied: "クリップボードにコピーしました",
  copyFailed: "コピーに失敗しました — JSONを手動で選択してください",
  footer:
    "万能AI PDFパーサーではありません。請求書テンプレートは合成デモデータのみです。Sekimosoft制作。",
  errNoFile: "PDFファイルを選択してください",
  errInvalidType: "PDFファイルのみ対応しています",
  errTooLarge: "ファイルサイズが5 MBを超えています",
  errExtractionFailed: "PDFからテキストを抽出できませんでした — V1ではスキャン文書非対応です",
  errValidationFailed: "請求書の検証に失敗しました — 下記を確認するかサンプル請求書PDFをお試しください",
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
