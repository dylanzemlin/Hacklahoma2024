import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"] });

export default function Home() {
    return (
        <main className={`flex min-h-screen flex-col items-center justify-center p-24 ${inter.className}`}>
            <div className="relative flex place-items-center before:absolute">
                <h1 className="text-6xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-br from-sky-500 to-blue-500 dark:from-sky-900 dark:to-blue-900">
                    Rosie
                </h1>
            </div>
        </main>
    );
}
