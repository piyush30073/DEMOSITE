import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "AdmissionFlow", description: "Student admission management CRM" };
export default function RootLayout({children}:{children:React.ReactNode}) {
 return <html lang="en"><body>{children}</body></html>;
}