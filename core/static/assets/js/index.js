/* global bootstrap: false */
(() => {
  'use strict'
  const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(tooltipTriggerEl => {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})()

// Récupérer l'URL actuelle
var currentUrl = window.location.pathname;

// Sélectionner tous les liens de la barre de navigation
var navLinks = document.querySelectorAll('.nav-link');

// Parcourir tous les liens et mettre à jour les classes en conséquence
navLinks.forEach(function(link) {
    var linkUrl = link.getAttribute('href');

    if (linkUrl === currentUrl) {
        link.classList.add('active');
    } else {
        link.classList.remove('active');
        link.classList.add('text-white');
    }
});

