
// Light/Dark Mode Toggle
const toggleButton = document.querySelector('.toggle-mode');
const body = document.body;

toggleButton.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    // Optional: Save the mode preference in localStorage
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});

// Load saved theme from localStorage
window.addEventListener('load', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
    }
});

// Scroll to Top Button
const scrollToTopButton = document.querySelector('.scroll-to-top');

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        scrollToTopButton.style.display = 'block';
    } else {
        scrollToTopButton.style.display = 'none';
    }
});

scrollToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Scroll Progress Indicator
const progressBar = document.querySelector('.progress-bar');

window.addEventListener('scroll', () => {
    const scrollTotal = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPosition = window.scrollY;
    const scrollPercentage = (scrollPosition / scrollTotal) * 100;
    progressBar.style.width = scrollPercentage + '%';
});

// Preloader
const preloader = document.querySelector('.preloader');

window.addEventListener('load', () => {
    preloader.style.visibility = 'hidden'; // Hide preloader when the page is loaded
});

// Optionally, show the preloader for a set period before hiding
window.addEventListener('load', () => {
    setTimeout(() => {
        preloader.style.visibility = 'hidden';
    }, 1000); // Wait 1 second before hiding
});