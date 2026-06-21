import { useState } from 'react';
import { useFavourites } from '../hooks/useFavourites';
import { Trash2, Star, ShoppingBag, ArrowRight, X, Leaf } from 'lucide-react';
import { Link } from 'react-router-dom';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function Dashboard() {
  const { favourites, removeFavourite } = useFavourites();
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [priceListings, setPriceListings] = useState([]);
  const [loadingPrices, setLoadingPrices] = useState(false);

  const openProductModal = async (product) => {
    setSelectedProduct(product);
    setLoadingPrices(true);
    try {
      const res = await fetch(`${API_URL}/api/products/${product.id}/prices`);
      const listings = await res.json();
      setPriceListings(listings);
    } catch (e) {
      console.error("Failed to fetch prices:", e);
    } finally {
      setLoadingPrices(false);
    }
  };

  const closeProductModal = () => {
    setSelectedProduct(null);
    setPriceListings([]);
  };

  if (favourites.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
        <div className="w-24 h-24 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center mb-6">
          <ShoppingBag size={40} className="text-slate-300 dark:text-slate-600" />
        </div>
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">Your Favourites is Empty</h2>
        <p className="text-slate-600 dark:text-slate-400 mb-8 max-w-md">
          You haven't saved any products yet. Take a quiz to get personalized recommendations and save your favourites here!
        </p>
        <Link to="/" className="btn-primary inline-flex items-center gap-2">
          Take a Quiz <ArrowRight size={18} />
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full max-w-6xl mx-auto py-8 relative">
      <div className="mb-12 border-b border-slate-200 dark:border-slate-800 pb-6">
        <h1 className="text-4xl font-bold text-slate-900 dark:text-white flex items-center gap-3">
          Your Saved Products
        </h1>
        <p className="text-slate-600 dark:text-slate-400 mt-3 text-lg">
          Products you've saved from your recommendations to buy later.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {favourites.map(product => {
          const isSkin = product.category === 'skincare';
          const noImage = !product.image_url;

          return (
            <div 
              key={product.id} 
              className="glass-card dark:bg-slate-800/80 dark:border-slate-700 overflow-hidden hover:shadow-xl dark:hover:shadow-slate-900/50 transition-all duration-300 flex flex-col h-full border-2 border-transparent hover:border-slate-200 dark:hover:border-slate-600 cursor-pointer"
              onClick={() => openProductModal(product)}
            >
              {/* Image Section */}
              {!noImage ? (
                <div className="relative h-56 bg-slate-50 dark:bg-slate-900 overflow-hidden w-full flex items-center justify-center p-4">
                  <img 
                    src={product.image_url} 
                    alt={product.name}
                    className="max-h-full object-contain mix-blend-multiply dark:mix-blend-normal hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute top-3 left-3 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm px-2 py-1 rounded-md text-xs font-bold shadow-sm capitalize text-slate-700 dark:text-slate-300">
                    {product.routine_step.replace('_', ' ')}
                  </div>
                </div>
              ) : (
                <div className="relative h-24 bg-slate-50 dark:bg-slate-900 w-full flex items-center justify-center p-4">
                  <span className="text-slate-400 font-semibold italic text-sm">Ingredient based</span>
                </div>
              )}

              {/* Content Section */}
              <div className="p-5 flex flex-col flex-grow">
                <span className={`text-xs font-bold uppercase tracking-wider mb-2 ${isSkin ? 'text-indigo-600 dark:text-indigo-400' : 'text-rose-600 dark:text-rose-400'}`}>
                  {product.brand}
                </span>
                
                <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-3 leading-tight">{product.name}</h3>
                
                <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-100 dark:border-slate-700">
                  <span className="text-sm font-bold text-slate-900 dark:text-white">
                    ~₹{product.price}
                  </span>
                  
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFavourite(product.id);
                    }}
                    className="p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/30 rounded-lg transition-colors z-10"
                    aria-label="Remove from favourites"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Product Detail Modal */}
      {selectedProduct && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" onClick={closeProductModal}>
          <div className="bg-white dark:bg-slate-800 rounded-3xl overflow-hidden w-full max-w-3xl max-h-[90vh] flex flex-col md:flex-row shadow-2xl relative" onClick={e => e.stopPropagation()}>
            <button 
              onClick={closeProductModal}
              className="absolute top-4 right-4 z-10 w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-full flex items-center justify-center text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-slate-600"
            >
              <X size={20} />
            </button>
            
            {selectedProduct.image_url && (
              <div className="md:w-2/5 bg-slate-50 dark:bg-slate-900 relative p-6 flex items-center justify-center">
                <img src={selectedProduct.image_url} alt={selectedProduct.name} className="max-h-full max-w-full object-contain mix-blend-multiply dark:mix-blend-normal" />
              </div>
            )}
            
            <div className={`${selectedProduct.image_url ? 'md:w-3/5' : 'w-full'} p-8 overflow-y-auto`}>
              <span className="text-sm font-bold tracking-wider text-slate-400 uppercase">{selectedProduct.brand}</span>
              <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">{selectedProduct.name}</h2>
              
              <div className="flex items-center gap-4 mb-6 pb-6 border-b border-slate-100 dark:border-slate-700">
                <span className="text-sm font-semibold px-3 py-1 bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-300 rounded-md flex items-center gap-1">
                  <Star size={14} className="fill-amber-500" />
                  {selectedProduct.similarity_score}% Match
                </span>
              </div>
              
              <p className="text-slate-600 dark:text-slate-400 mb-6 leading-relaxed text-sm">{selectedProduct.description || "Formulated to target your specific concerns while respecting your skin's natural barrier."}</p>
              
              <div className="mb-8">
                <h4 className="text-sm font-bold text-slate-800 dark:text-white mb-3 uppercase flex items-center gap-2">
                  <Leaf size={16} className="text-emerald-500" /> 
                  Key Ingredients
                </h4>
                <div className="flex flex-wrap gap-2">
                  {selectedProduct.key_ingredients && selectedProduct.key_ingredients.split(',').map((ing, idx) => (
                    <span key={idx} className="text-xs font-bold px-3 py-1.5 rounded-lg bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300">
                      {ing.trim()}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="text-sm font-bold text-slate-800 dark:text-white mb-4 uppercase flex items-center gap-2">
                  <ShoppingBag size={16} className="text-emerald-500" />
                  Compare Prices
                </h4>
                
                {loadingPrices ? (
                  <div className="animate-pulse space-y-3">
                    {[1, 2, 3, 4].map(i => (
                      <div key={i} className="h-14 bg-slate-100 dark:bg-slate-700 rounded-xl"></div>
                    ))}
                  </div>
                ) : (
                  <div className="grid grid-cols-2 gap-3">
                    {[...priceListings].sort((a, b) => a.price - b.price).map((listing, index) => (
                      <a href="#" key={listing.id} className={`flex flex-col p-4 border rounded-xl transition-colors cursor-pointer ${index === 0 ? 'border-emerald-200 dark:border-emerald-700 bg-emerald-50 dark:bg-emerald-900/20 hover:bg-emerald-100 dark:hover:bg-emerald-900/40' : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 bg-white dark:bg-slate-800'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <span className={`font-bold text-sm ${index === 0 ? 'text-emerald-900 dark:text-emerald-400' : 'text-slate-800 dark:text-slate-300'}`}>{listing.platform}</span>
                          {index === 0 && (
                            <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-emerald-200 dark:bg-emerald-800 text-emerald-800 dark:text-emerald-100">
                              Best
                            </span>
                          )}
                        </div>
                        <span className={`font-bold text-lg ${index === 0 ? 'text-emerald-700 dark:text-emerald-300' : 'text-slate-900 dark:text-white'}`}>₹{listing.price.toFixed(2)}</span>
                      </a>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
