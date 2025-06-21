// Modern JavaScript Enhancements (Fixed for Portfolio Modals)
(function($) {
  "use strict";

  // Navbar Shrink Effect
  $(window).scroll(function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  });

  // Enhanced Form Handling
  $("#contactForm").on("submit", function(e) {
    var $button = $("#sendMessageButton");
    var originalText = $button.html();

    // Add loading state
    $button.addClass("btn-loading").prop("disabled", true);

    // Reset after form submission
    setTimeout(function() {
      $button.removeClass("btn-loading").html(originalText).prop("disabled", false);
    }, 3000);
  });

  // --- REMOVED: Old conflicting smooth scroll handler ---

})(jQuery);

// Enhanced, conflict-free smooth scroll for nav links
(function($) {
  "use strict";
  // Remove default Agency scroll/collapse handlers
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').off('click');
  $('.js-scroll-trigger').off('click');

  // Add improved smooth scroll that collapses nav after scroll (mobile)
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').on('click', function(e) {
    var pathname = location.pathname.replace(/^\//, '');
    var linkPath = this.pathname.replace(/^\//, '');
    if (pathname === linkPath && location.hostname === this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        e.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top - 54 // adjust if your navbar height is different
        }, 800, "easeInOutExpo", function() {
          // Collapse menu after scroll completes (for mobile)
          if ($('.navbar-collapse').hasClass('show')) {
            $('.navbar-collapse').collapse('hide');
          }
        });
        return false;
      }
    }
  });
})(jQuery);

// Portfolio Modal: Blur-up and Lazy Load Enhancements (if you have this section)
(function($) {
  "use strict";

  // Portfolio Modal Image Lazy Loading + Blur-up
  $('.portfolio-modal').on('show.bs.modal', function(e) {
    var $img = $(this).find('img.lazy');
    if ($img.length && !$img.hasClass('loaded')) {
      $img.each(function() {
        var $imgEl = $(this);
        $imgEl.attr('src', $imgEl.data('src'));
        $imgEl.on('load', function() {
          $imgEl.addClass('loaded');
        });
      });
    }
  });

  // Optionally, reset the image if needed on modal close
  // $('.portfolio-modal').on('hidden.bs.modal', function(e) {
  //   var $img = $(this).find('img.lazy.loaded');
  //   $img.removeClass('loaded');
  // });

})(jQuery);

