
function closepopup(){
   var popup =  document.getElementById('popupbox');
   var openpopupbox =  document.getElementById('openpopupbox');
   var outeropenpopupbox =  document.getElementById('outerpopup');

   openpopupbox.style.display="block" ;
   popup.style.transform = "translateX(100rem)" ;

}

function openpopup(){

   var popup =  document.getElementById('popupbox');
   var openpopupbox =  document.getElementById('openpopupbox');

   openpopupbox.style.display="none" ;
   popup.style.display="flow-root" ;
   popup.style.transform = "translateX(0rem)" ;

 }

// Typing effect Imgtxt
var i = 0;
var txt = 'ASSOCIATION FOR COMPUTING MACHINERY';
var speed = 100;

function typeWriter() {
  if (i < txt.length) {
    document.getElementById("maintext").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}


/* Get the offset position(i.e after which height we want
to change colour).  */

function StickyHeader() {
  var header = document.getElementById("header") ;
  var sticky = header.offsetTop + 500 ;

if (window.pageYOffset > sticky) {
  // header.style.backgroundColor=" rgba(7, 18, 54, 0.904)";
     header.classList.add("scrollHeader") ;
} else {
  // header.style.backgroundColor=" rgba(0, 0, 0, 0.00)";
     header.classList.remove("scrollHeader") ;

  }
}
