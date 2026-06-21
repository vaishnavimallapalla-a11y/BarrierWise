import { useNavigate } from 'react-router-dom';
import { Sparkles, Droplets } from 'lucide-react';

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="w-full max-w-4xl mx-auto flex flex-col items-center justify-center text-center">
      <div className="mb-12 space-y-4">
        <h1 className="text-5xl md:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-rose-500 pb-2">
          BarrierWise
        </h1>
        <p className="text-lg md:text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
          Discover personalized routines for your unique skin and hair needs, powered by intelligent ingredient matching.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 w-full">
        {/* Skincare Card */}
        <button 
          onClick={() => navigate('/quiz/skincare')}
          className="glass-card dark:bg-slate-800/80 dark:border-slate-700 group p-8 text-left transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-indigo-500/20 active:scale-95 border-2 border-transparent hover:border-indigo-100 dark:hover:border-indigo-500 flex flex-col items-start gap-4"
        >
          <div className="w-16 h-16 rounded-2xl bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400 flex items-center justify-center group-hover:bg-indigo-600 dark:group-hover:bg-indigo-500 group-hover:text-white transition-colors">
            <Sparkles size={32} />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-800 dark:text-white mb-2">Skincare Path</h2>
            <p className="text-slate-600 dark:text-slate-400">Find products tailored to your exact skin type and concerns.</p>
          </div>
        </button>

        {/* Haircare Card */}
        <button 
          onClick={() => navigate('/quiz/haircare')}
          className="glass-card dark:bg-slate-800/80 dark:border-slate-700 group p-8 text-left transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-rose-500/20 active:scale-95 border-2 border-transparent hover:border-rose-100 dark:hover:border-rose-500 flex flex-col items-start gap-4"
        >
          <div className="w-16 h-16 rounded-2xl bg-rose-100 dark:bg-rose-900/50 text-rose-600 dark:text-rose-400 flex items-center justify-center group-hover:bg-rose-600 dark:group-hover:bg-rose-500 group-hover:text-white transition-colors">
            <Droplets size={32} />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-800 dark:text-white mb-2">Haircare Path</h2>
            <p className="text-slate-600 dark:text-slate-400">Understand your scalp and hair porosity for the perfect routine.</p>
          </div>
        </button>
      </div>
    </div>
  );
}
