import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TruthResolve",
  description: "Consensus-backed real-world claim verification on GenLayer",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
