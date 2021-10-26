
// Typing effect Imgtxt
var i = 0;
var txt = 'LOC 3.0';
var speed = 100;

function typeWriter() {
  if (i < txt.length) {
   // document.getElementById("maintext").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}


/* Get the offset position(i.e after which height we want
to change colour).  */

function StickyHeader() {
  var header = document.getElementById("header") ;
  var sticky = header.offsetTop + 300 ;

if (window.pageYOffset > sticky) {
  // header.style.backgroundColor=" rgba(7, 18, 54, 0.904)";
     header.classList.add("scrollHeader") ;
} else {
  // header.style.backgroundColor=" rgba(0, 0, 0, 0.00)";
     header.classList.remove("scrollHeader") ;

  }
}
