import { Link, useLocation } from 'react-router-dom';
import { Sun, Moon, Heart, Home } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';
import { useFavourites } from '../hooks/useFavourites';

export default function Navbar() {
  const { isDark, toggleTheme } = useTheme();
  const { favourites } = useFavourites();
  const location = useLocation();

  return (
    <nav className="w-full bg-white/80 dark:bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 border-b border-slate-200 dark:border-slate-800 transition-colors duration-300">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center text-white font-bold text-lg group-hover:scale-105 transition-transform">
            B
          </div>
          <span className="text-xl font-bold text-slate-900 dark:text-white">BarrierWise</span>
        </Link>
        
        <div className="flex items-center gap-4">
          <Link 
            to="/" 
            className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium transition-colors ${location.pathname === '/' ? 'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
          >
            <Home size={18} />
            <span className="hidden sm:inline">Home</span>
          </Link>
          
          <Link 
            to="/dashboard" 
            className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium transition-colors ${location.pathname === '/dashboard' ? 'text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-900/30' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
          >
            <div className="relative">
              <Heart size={18} className={favourites.length > 0 ? "fill-rose-500 text-rose-500" : ""} />
              {favourites.length > 0 && (
                <span className="absolute -top-1 -right-2 w-4 h-4 bg-rose-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                  {favourites.length}
                </span>
              )}
            </div>
            <span className="hidden sm:inline">Favourites</span>
          </Link>

          <button 
            onClick={toggleTheme}
            className="p-2 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            aria-label="Toggle theme"
          >
            {isDark ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </div>
      </div>
    </nav>
  );
}
