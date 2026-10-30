import "./globals.css";
import Shell from "../components/Shell";
export const metadata = { title: "VFS AI Engine" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body><Shell>{children}</Shell></body></html>;
}
