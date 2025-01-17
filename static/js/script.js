// Scroll Progress Indicator
const progressBar = document.querySelector('.progress-bar');

window.addEventListener('scroll', () => {
    const scrollTotal = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPosition = window.scrollY;
    const scrollPercentage = (scrollPosition / scrollTotal) * 100;
    if (progressBar) {
        progressBar.style.width = scrollPercentage + '%';
    }
});

// Hide preloader
window.addEventListener('load', () => {
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        preloader.style.display = 'none';
    }
});

// Light/Dark Mode Toggle
const toggleButton = document.querySelector('.toggle-mode');
const body = document.body;

// Load saved theme from localStorage
window.addEventListener('load', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
    }
});

if (toggleButton) {
    toggleButton.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        // Save the mode preference in localStorage
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
    });
}

// Scroll to top
const upButton = document.querySelector('#up-button');
if (upButton) {
    upButton.addEventListener('click', () => {
        window.scrollTo({ insetBlockStart: 0, behavior: 'smooth' });
    });
}

// Hide and show header on scroll
let lastScrollTop = 0;
const header = document.querySelector('header');

window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    if (header) {
        if (scrollTop > lastScrollTop) {
            header.classList.add('hidden');
        } else {
            header.classList.remove('hidden');
        }
    }
    lastScrollTop = scrollTop;

    // Show or hide the up button
    if (upButton) {
        if (scrollTop > 100) {
            upButton.style.display = 'block';
        } else {
            upButton.style.display = 'none';
        }
    }
});

// Chat functionality
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatBody = document.getElementById('chatBody');
    
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message
    appendMessage('user', message);
    userInput.value = '';

    try {
        const response = await fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        appendMessage('bot', data.response);
    } catch (error) {
        console.error('Error:', error);
        appendMessage('bot', 'Sorry, something went wrong!');
    }
}

function appendMessage(sender, message) {
    const chatBody = document.getElementById('chatBody');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = message;
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Initialize chat modal
document.addEventListener('DOMContentLoaded', function() {
    const chatModal = document.getElementById('chatModal');
    chatModal.addEventListener('shown.bs.modal', function() {
        document.getElementById('userInput').focus();
    });
});