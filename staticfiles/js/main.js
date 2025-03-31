// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Animated elements on scroll
    const animateElements = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');

        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (elementPosition < windowHeight - 100) {
                element.classList.add('animated');
            }
        });
    };

    // Header scroll effect
    const header = document.querySelector('header');

    const headerScrollEffect = () => {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    // Mobile navigation toggle
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (mobileNavToggle) {
        mobileNavToggle.addEventListener('click', function() {
            if (mainNav.style.display === 'flex') {
                mainNav.style.display = 'none';
                this.innerHTML = '<i class="fas fa-bars"></i>';
            } else {
                mainNav.style.display = 'flex';
                this.innerHTML = '<i class="fas fa-times"></i>';
            }
        });
    }

    // Newsletter form submission with AJAX
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = this.querySelector('input[name="email"]').value;
            const csrfToken = this.querySelector('input[name="csrfmiddlewaretoken"]').value;

            fetch(this.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `email=${encodeURIComponent(email)}`
            })
            .then(response => response.json())
            .then(data => {
                // Create a notification element
                const notification = document.createElement('div');
                notification.className = data.success ? 'notification success' : 'notification error';
                notification.textContent = data.message;

                // Append to body
                document.body.appendChild(notification);

                // Show with animation
                setTimeout(() => {
                    notification.classList.add('show');
                }, 10);

                // Remove after 3 seconds
                setTimeout(() => {
                    notification.classList.remove('show');
                    setTimeout(() => {
                        document.body.removeChild(notification);
                    }, 300);
                }, 3000);

                if (data.success) {
                    this.reset();
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    // Add .animate-on-scroll class to elements that should animate
    const addAnimationClasses = () => {
        document.querySelectorAll('.section-title, .trailer-card, .portfolio-item, .workshop-card, .stat-item').forEach(element => {
            element.classList.add('animate-on-scroll');
        });
    };

    // Run once on load
    addAnimationClasses();
    headerScrollEffect();
    animateElements();

    // Add event listeners
    window.addEventListener('scroll', headerScrollEffect);
    window.addEventListener('scroll', animateElements);
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && mainNav) {
            mainNav.style.display = '';
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add parallax effect to hero section
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.scrollY;
            hero.style.backgroundPositionY = scrollPosition * 0.5 + 'px';
        });
    }
});

// Add additional class to the appropriate sections
document.addEventListener('DOMContentLoaded', function() {
    // Mark sections for animations
    const sections = document.querySelectorAll('section');
    sections.forEach((section, index) => {
        if (index % 2 === 0) {
            section.classList.add('section-light');
        } else {
            section.classList.add('section-dark');
        }
    });
});
// Initialize Swiper slider for trailers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Swiper
    const trailersSlider = new Swiper('.trailers-slider', {
        slidesPerView: 1,
        spaceBetween: 30,
        centeredSlides: true,
        loop: true,
        loopAdditionalSlides: 30,
        speed: 800,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            992: {
                slidesPerView: 3,
                spaceBetween: 30,
            },
        },
        on: {
            init: function() {
                // Add index as custom property for staggered animations
                document.querySelectorAll('.swiper-slide').forEach((slide, index) => {
                    slide.style.setProperty('--index', index);
                });
            },
        },
    });

    // Handle trailer modal
    const trailerModal = document.getElementById('trailerModal');
    const trailerFrame = document.getElementById('trailerFrame');
    const trailerModalTitle = document.getElementById('trailerModalTitle');
    const closeModal = document.querySelector('.close-modal');

    // Open modal when watch button is clicked
    document.querySelectorAll('.btn-watch').forEach(button => {
        button.addEventListener('click', function() {
            const trailerUrl = this.getAttribute('data-trailer-url');
            const trailerTitle = this.getAttribute('data-trailer-title');

            // Set iframe source to YouTube or Vimeo URL
            // Convert URL to embed format if needed
            let embedUrl = trailerUrl;

            // Handle YouTube links
            if (trailerUrl.includes('youtube.com/watch?v=')) {
                const videoId = trailerUrl.split('v=')[1].split('&')[0];
                embedUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
            }
            // Handle Vimeo links
            else if (trailerUrl.includes('vimeo.com/')) {
                const videoId = trailerUrl.split('/').pop();
                embedUrl = `https://player.vimeo.com/video/${videoId}?autoplay=1`;
            }

            trailerFrame.src = embedUrl;
            trailerModalTitle.textContent = trailerTitle;

            // Show modal with animation
            trailerModal.classList.add('show');

            // Prevent body scrolling
            document.body.style.overflow = 'hidden';
        });
    });

    // Close modal when close button is clicked
    if (closeModal) {
        closeModal.addEventListener('click', function() {
            closeTrailerModal();
        });
    }

    // Close modal when clicking outside content
    if (trailerModal) {
        trailerModal.addEventListener('click', function(e) {
            if (e.target === trailerModal) {
                closeTrailerModal();
            }
        });
    }

    // Close modal when ESC key is pressed
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && trailerModal.classList.contains('show')) {
            closeTrailerModal();
        }
    });

    function closeTrailerModal() {
        trailerModal.classList.remove('show');
        setTimeout(() => {
            trailerFrame.src = '';
        }, 300);
        document.body.style.overflow = '';
    }
});
// Notification CSS to add to your main.css
document.head.insertAdjacentHTML('beforeend', `
<style>
.notification {
    position: fixed;
    bottom: 30px;
    right: 30px;
    padding: 15px 25px;
    border-radius: 8px;
    color: white;
    font-weight: 500;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    transform: translateY(100px);
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    z-index: 9999;
}

.notification.success {
    background: linear-gradient(to right, #28a745, #218838);
}

.notification.error {
    background: linear-gradient(to right, #dc3545, #c82333);
}

.notification.show {
    transform: translateY(0);
    opacity: 1;
}

/* Additional animation classes */
.animate-on-scroll {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease, transform 0.8s ease;
}

.animate-on-scroll.animated {
    opacity: 1;
    transform: translateY(0);
}

/*.trailer-card.animate-on-scroll {*/
/*    transition-delay: calc(0.1s * var(--index, 0));*/
/*}*/

/*.portfolio-item.animate-on-scroll {*/
/*    transition-delay: calc(0.15s * var(--index, 0));*/
/*}*/

/*.workshop-card.animate-on-scroll {*/
/*    transition-delay: calc(0.2s * var(--index, 0));*/
/*}*/
</style>
`);