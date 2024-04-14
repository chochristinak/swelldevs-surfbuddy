jQuery(window).load(function ($) {
    var images = [];
  
    // iterate over your selection
    $('#background img').each(function () {
      // save source to list
      images.push(this.src);
    });
    $.backstretch(body.background);
});