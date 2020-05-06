(function($) {
  "use strict"; // Start of use strict


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

  // Populate task modal when a task is double clicked
//  $(document).on('click', '.task-card .card-body a', function(e) {
//    var taskTitle = this.dataset.tasktitle
//
//    var modal = $('#createTaskModalCenter')
//    var titleInput = modal.find('#title-name')
//    titleInput.value = taskTitle
//
//  });

    $('#createTaskModalCenter').on('show.bs.modal', function (e){
        var linkClicked = e.relatedTarget

       var taskTitle = linkClicked.dataset.tasktitle
       $(this).find('#title-name').val(linkClicked.dataset.tasktitle)
       $(this).find('#status-task').val(linkClicked.dataset.status)
       $(this).find('#description-text').val(linkClicked.dataset.description)
       $(this).find('#project-name').val(linkClicked.dataset.projectname)
//       data-description = {{task.description}}
//       data-projectname="{{ task.project.name }}"
//       data-estimated_hours="{{ task.estimated_hours }}"

    })

})(jQuery); // End of use strict
