import { useState, useEffect } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { RotateCcw, CheckCircle, Leaf, Percent, Star, X, ShoppingBag, Sparkles, Heart } from 'lucide-react';
import { useFavourites } from '../hooks/useFavourites';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function Results() {
  const { category } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  
  const data = location.state?.data;
  const viewMode = location.state?.viewMode || 'products';
  const { isFavourite, addFavourite, removeFavourite } = useFavourites();
  
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [priceListings, setPriceListings] = useState([]);
  const [loadingPrices, setLoadingPrices] = useState(false);
  const [toastMessage, setToastMessage] = useState('');

  if (!data) {
    return (
      <div className="text-center mt-20">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">No results found</h2>
        <button onClick={() => navigate('/')} className="btn-primary">Go Home</button>
      </div>
    );
  }

  const { result_type, products, home_remedies } = data || {};
  const safeProducts = Array.isArray(products) ? products : [];
  const isSkin = category === 'skincare';

  const routineOrderSkin = ['cleanser', 'toner', 'serum', 'moisturizer', 'sunscreen', 'eye_cream'];
  const routineOrderHair = ['shampoo', 'conditioner', 'hair_mask', 'serum', 'oil', 'leave_in_conditioner'];
  const routineOrder = isSkin ? routineOrderSkin : routineOrderHair;

  const groupedProducts = {};
  routineOrder.forEach(step => {
    groupedProducts[step] = safeProducts.filter(p => p.routine_step === step);
  });

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

  const showToast = (message) => {
    setToastMessage(message);
    setTimeout(() => setToastMessage(''), 3000);
  };

  const toggleFavourite = (e, product) => {
    e.stopPropagation();
    if (isFavourite(product.id)) {
      removeFavourite(product.id);
      showToast('Removed from favourites');
    } else {
      addFavourite(product);
      showToast('Added to your favourites!');
    }
  };

  const renderProductCard = (product, type) => {
    if (!product) return null;
    
    const noImage = !product.image_url;
    const favourited = isFavourite(product.id);

    return (
      <div 
        key={product.id} 
        className="glass-card dark:bg-slate-800/80 dark:border-slate-700 overflow-hidden hover:shadow-xl dark:hover:shadow-slate-900/50 transition-all duration-300 cursor-pointer group flex flex-col h-full border-2 border-transparent hover:border-slate-200 dark:hover:border-slate-600 relative"
        onClick={() => openProductModal(product)}
      >
        <div className={`text-center py-2 text-xs font-bold uppercase tracking-wider text-white ${type === 'budget' ? 'bg-emerald-500 dark:bg-emerald-600' : 'bg-purple-600 dark:bg-purple-700'}`}>
          {type === 'budget' ? 'Budget Friendly' : 'Premium Choice'}
        </div>

        <button 
          onClick={(e) => toggleFavourite(e, product)}
          className="absolute top-10 right-3 z-10 w-8 h-8 bg-white/80 dark:bg-slate-800/80 backdrop-blur rounded-full flex items-center justify-center text-rose-500 hover:bg-white dark:hover:bg-slate-700 shadow-sm"
        >
          <Heart size={16} className={favourited ? "fill-rose-500" : ""} />
        </button>

        {!noImage ? (
          <div className="relative h-64 bg-slate-50 dark:bg-slate-900 overflow-hidden w-full flex items-center justify-center p-4">
            <img 
              src={product.image_url} 
              alt={product.name}
              className="max-h-full object-contain group-hover:scale-105 transition-transform duration-500 mix-blend-multiply dark:mix-blend-normal"
            />
          </div>
        ) : (
          <div className="relative h-24 bg-slate-50 dark:bg-slate-900 w-full flex items-center justify-center p-4">
            <span className="text-slate-400 dark:text-slate-500 font-semibold italic">Ingredient based recommendation</span>
          </div>
        )}

        <div className="p-6 flex flex-col flex-grow">
          <div className="flex items-center justify-between mb-2">
            <span className={`text-xs font-bold uppercase tracking-wider ${isSkin ? 'text-indigo-600 dark:text-indigo-400' : 'text-rose-600 dark:text-rose-400'}`}>
              {product.brand}
            </span>
          </div>
          
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-4 leading-tight">{product.name}</h3>
          
          <div className="flex flex-wrap gap-2 mb-4">
            {product.key_ingredients && product.key_ingredients.split(',').slice(0, 3).map((ing, idx) => (
              <span key={idx} className={`text-[10px] uppercase tracking-wide font-bold px-2 py-1 rounded-md ${isSkin ? 'bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300' : 'bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300'}`}>
                {ing.trim()}
              </span>
            ))}
          </div>
          
          <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-100 dark:border-slate-700">
            <div className="flex items-center gap-1 text-sm font-semibold text-slate-700 dark:text-slate-300">
              <Star size={16} className="fill-amber-400 text-amber-400" />
              {product.similarity_score}% Match
            </div>
            <span className="text-sm font-bold text-slate-900 dark:text-white">
              ~₹{product.price}
            </span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="w-full max-w-6xl mx-auto flex flex-col pb-20 pt-8 relative">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-20 left-1/2 transform -translate-x-1/2 z-50 bg-slate-900 dark:bg-white text-white dark:text-slate-900 px-6 py-3 rounded-full shadow-xl font-bold transition-all animate-bounce">
          {toastMessage}
        </div>
      )}

      <div className="text-center mb-16">
        <span className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-bold tracking-wide mb-6 ${isSkin ? 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300' : 'bg-rose-100 dark:bg-rose-900/50 text-rose-700 dark:text-rose-300'}`}>
          <CheckCircle size={16} />
          ANALYSIS COMPLETE
        </span>
        <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4">
          Your Profile: <span className={isSkin ? 'text-indigo-600 dark:text-indigo-400' : 'text-rose-600 dark:text-rose-400 capitalize'}>{result_type}</span>
        </h1>
      </div>

      {viewMode === 'products' && (
      <div className="mb-16">
        <div className="mb-8 border-b border-slate-200 dark:border-slate-700 pb-4">
          <h2 className="text-3xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Sparkles className={isSkin ? 'text-indigo-500' : 'text-rose-500'} />
            Recommended Routine
          </h2>
          <p className="text-slate-600 dark:text-slate-400 mt-2 text-lg">Compare options for each step of your routine.</p>
        </div>

        <div className="flex flex-col gap-12">
          {routineOrder.map(step => {
            const stepProducts = groupedProducts[step];
            if (!stepProducts || stepProducts.length === 0) return null;
            
            const budgetProd = stepProducts.find(p => p.budget_tier === 'budget') || stepProducts[0];
            const premiumProd = stepProducts.find(p => p.budget_tier === 'premium') || (stepProducts.length > 1 ? stepProducts[1] : null);

            return (
              <div key={step} className="bg-white/50 dark:bg-slate-800/30 p-6 rounded-3xl border border-slate-100 dark:border-slate-700 shadow-sm">
                <h3 className="text-2xl font-bold text-slate-800 dark:text-white mb-6 capitalize px-2 flex items-center gap-2">
                  <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm text-white ${isSkin ? 'bg-indigo-500' : 'bg-rose-500'}`}>
                    {routineOrder.indexOf(step) + 1}
                  </span>
                  {step.replace('_', ' ')}
                </h3>
                
                <div className="grid md:grid-cols-2 gap-6">
                  {renderProductCard(budgetProd, 'budget')}
                  {premiumProd && premiumProd.id !== budgetProd.id && renderProductCard(premiumProd, 'premium')}
                </div>
              </div>
            );
          })}
        </div>
      </div>
      )}

      {viewMode === 'remedies' && home_remedies && home_remedies.length > 0 && (
        <div className="mb-16 bg-emerald-50/50 dark:bg-emerald-900/10 p-8 rounded-3xl border border-emerald-100 dark:border-emerald-900/30">
          <div className="flex items-center justify-between mb-8 border-b border-emerald-200 dark:border-emerald-800 pb-4">
            <h2 className="text-3xl font-bold text-emerald-800 dark:text-emerald-400 flex items-center gap-2">
              <Leaf className="text-emerald-500" /> Natural Remedies
            </h2>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {home_remedies.map(remedy => (
              <div key={remedy.id} className="bg-white dark:bg-slate-800 border border-emerald-100 dark:border-emerald-800/50 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow flex flex-col">
                {remedy.image_url && (
                  <div className="h-48 bg-slate-100 dark:bg-slate-900 relative">
                    <img src={remedy.image_url} alt={remedy.title} className="w-full h-full object-cover" />
                  </div>
                )}
                <div className="p-6 flex-1 flex flex-col">
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">{remedy.title}</h3>
                  <p className="text-slate-600 dark:text-slate-400 mb-6 leading-relaxed flex-1 text-sm">{remedy.instructions}</p>
                  
                  <div className="pt-4 border-t border-slate-100 dark:border-slate-700">
                    <h4 className="text-xs font-bold text-emerald-600 dark:text-emerald-400 mb-2 uppercase flex items-center gap-1">
                       Ingredients Needed
                    </h4>
                    <p className="font-semibold text-slate-800 dark:text-slate-200 text-sm">{remedy.ingredients_used}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-8 text-center">
        <button 
          onClick={() => navigate('/')}
          className="bg-slate-900 dark:bg-white hover:bg-slate-800 dark:hover:bg-slate-200 text-white dark:text-slate-900 px-8 py-4 rounded-xl font-bold text-lg inline-flex items-center gap-2 shadow-lg transition-transform hover:scale-105"
        >
          <RotateCcw size={20} />
          Retake Quiz
        </button>
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
                <span className={`text-sm font-semibold px-3 py-1 rounded-md ${selectedProduct.budget_tier === 'budget' ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-800 dark:text-emerald-300' : 'bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-300'}`}>
                  {selectedProduct.budget_tier === 'budget' ? 'Budget' : 'Premium'}
                </span>
              </div>
              
              <p className="text-slate-600 dark:text-slate-400 mb-6 leading-relaxed text-sm">{selectedProduct.description || "Formulated to target your specific concerns while respecting your skin's natural barrier."}</p>
              
              <div className="mb-8">
                <h4 className="text-sm font-bold text-slate-800 dark:text-white mb-3 uppercase flex items-center gap-2">
                  <Leaf size={16} className={isSkin ? 'text-indigo-500' : 'text-rose-500'} /> 
                  Key Ingredients
                </h4>
                <div className="flex flex-wrap gap-2">
                  {selectedProduct.key_ingredients && selectedProduct.key_ingredients.split(',').map((ing, idx) => (
                    <span key={idx} className={`text-xs font-bold px-3 py-1.5 rounded-lg ${isSkin ? 'bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300' : 'bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300'}`}>
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
