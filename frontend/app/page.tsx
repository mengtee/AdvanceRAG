import Header from "@/app/components/header";
import ChatSection from "./components/chat-section";

// main chat page 
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center gap-10 p-24 background-gradient">
      <Header />
      <ChatSection />
    </main>
  );
}
