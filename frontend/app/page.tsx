import Header from "@/app/components/header";
import ChatSection from "./components/chat-section";
import TeamIntroduction from "@/app/components/team-intro";
import ProjectIntroduction from "@/app/components/proj-intro";

// main chat page 
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center gap-10 p-24 background-gradient">
      <Header />
      <ProjectIntroduction/>
      <ChatSection />
      <TeamIntroduction/>
    </main>
  );
}

// import Link from 'next/link';

// export default function MainPage() {
//   return (
//     <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
//       <h1 className="text-4xl font-bold">Welcome to the Chat App</h1>
//       <p className="mt-2 text-xl">Navigate to the chat session below:</p>
//       <Link href="/chat">
//         <span className="mt-4 cursor-pointer rounded bg-blue-500 py-2 px-4 text-white hover:bg-blue-700 transition duration-200">
//           Go to Chat
//         </span>
//       </Link>
//     </div>
//   );
// }
