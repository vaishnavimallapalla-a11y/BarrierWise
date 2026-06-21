import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Landing from './components/Landing';
import Quiz from './components/Quiz';
import Results from './components/Results';
import Dashboard from './components/Dashboard';
import Navbar from './components/Navbar';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 transition-colors duration-300">
        <Navbar />
        {/* Background decorative elements */}
        <div className="fixed top-[-20%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-indigo-200/40 dark:bg-indigo-900/20 blur-[100px] -z-10 mix-blend-multiply dark:mix-blend-screen pointer-events-none"></div>
        <div className="fixed bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] rounded-full bg-rose-200/40 dark:bg-rose-900/20 blur-[100px] -z-10 mix-blend-multiply dark:mix-blend-screen pointer-events-none"></div>
        
        <main className="container mx-auto px-4 py-8 relative z-10 min-h-[calc(100vh-4rem)] flex flex-col items-center justify-center">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/quiz/:category" element={<Quiz />} />
            <Route path="/results/:category" element={<Results />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
