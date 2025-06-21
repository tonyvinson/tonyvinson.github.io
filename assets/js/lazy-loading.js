// Lazy Loading with Intersection Observer
// Save this as: assets/js/lazy-loading.js

(function() {
  'use strict';

  // Check if browser supports Intersection Observer
  if ('IntersectionObserver' in window) {
    // Modern browsers - use Intersection Observer
    const imageObserver = new IntersectionObserver(function(entries, observer) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          const img = entry.target;
          
          // Load the image
          img.src = img.dataset.src;
          
          // If srcset exists, set it
          if (img.dataset.srcset) {
            img.srcset = img.dataset.srcset;
          }
          
          // Add loaded class for CSS transition
          img.classList.add('lazy-loaded');
          img.classList.remove('lazy');
          
          // Remove placeholder
          img.style.backgroundImage = 'none';
          
          // Stop observing this image
          observer.unobserve(img);
          
          // Fire custom event
          img.dispatchEvent(new Event('lazyloaded'));
        }
      });
    }, {
      // Start loading 50px before the image enters viewport
      rootMargin: '50px 0px',
      threshold: 0.01
    });

    // Observe all lazy images
    const lazyImages = document.querySelectorAll('img.lazy');
    lazyImages.forEach(function(img) {
      imageObserver.observe(img);
    });

  } else {
    // Fallback for older browsers - load all images immediately
    const lazyImages = document.querySelectorAll('img.lazy');
    lazyImages.forEach(function(img) {
      img.src = img.dataset.src;
      if (img.dataset.srcset) {
        img.srcset = img.dataset.srcset;
      }
      img.classList.add('lazy-loaded');
      img.classList.remove('lazy');
    });
  }

  // Native lazy loading support check
  if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
      if (img.dataset.src && !img.src) {
        img.src = img.dataset.src;
      }
    });
  } else {
    // Browser doesn't support native lazy loading
    // Our IntersectionObserver code above will handle it
  }

  // Preload critical images (like hero images)
  const criticalImages = document.querySelectorAll('img[data-critical="true"]');
  criticalImages.forEach(function(img) {
    if (img.dataset.src) {
      img.src = img.dataset.src;
      img.classList.add('lazy-loaded');
      img.classList.remove('lazy');
    }
  });

})();
