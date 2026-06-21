import { useState, useEffect } from 'react';

export function useFavourites() {
  const [favourites, setFavourites] = useState(() => {
    const saved = localStorage.getItem('barrierwise_favourites');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem('barrierwise_favourites', JSON.stringify(favourites));
  }, [favourites]);

  const addFavourite = (product) => {
    setFavourites(prev => {
      if (prev.find(p => p.id === product.id)) return prev;
      return [...prev, product];
    });
  };

  const removeFavourite = (productId) => {
    setFavourites(prev => prev.filter(p => p.id !== productId));
  };

  const isFavourite = (productId) => {
    return favourites.some(p => p.id === productId);
  };

  return { favourites, addFavourite, removeFavourite, isFavourite };
}
