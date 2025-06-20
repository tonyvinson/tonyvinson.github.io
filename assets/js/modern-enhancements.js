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

  // Smooth Scroll Enhancement - FIXED to exclude modal triggers
  $('a[href*="#"]').not('[href="#"]').not('[data-toggle="modal"]').not('.portfolio-link').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 54)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

})(jQuery);
