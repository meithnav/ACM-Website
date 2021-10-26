

/* Get the offset position(i.e after which height we want
to change colour).  */

function StickyHeader() {
  var header = document.getElementById("header") ;
  var sticky = header.offsetTop + 40 ;

if (window.pageYOffset > sticky) {
  // header.style.backgroundColor=" rgba(7, 18, 54, 0.904)";
     header.classList.add("scrollHeader") ;
} else {
  // header.style.backgroundColor=" rgba(0, 0, 0, 0.00)";
     header.classList.remove("scrollHeader") ;

  }
}

//MODAL BOX


// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demo");
  var captionText = document.getElementById("caption");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}
