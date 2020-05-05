(function($) {
  "use strict"; // Start of use strict
  
  // Open the create task modal
//   $('#createTaskModalCenter').on('show.bs.modal', function (event) {
//   	var button = $(event.relatedTarget) // Button that triggered the modal
//   	var recipient = button.data('whatever') // Extract info from data-* attributes
//   	// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
//   	// Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//   	var modal = $(this)
//   	modal.find('.modal-title').text('Something')
//   	//modal.find('.modal-body input').val(recipient)
//   })
	

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    //$(".sidebar").toggleClass("toggled");
     if ($(".sidebar").hasClass("toggled")) {
       $('.sidebar .collapse').collapse('hide');
     };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  setTimeout(function(){
      $('#message').fadeOut('slow')
  }, 3000);

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict
