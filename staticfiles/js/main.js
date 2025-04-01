// // static/js/main.js
//
// document.addEventListener('DOMContentLoaded', function() {
//     // Animated elements on scroll
//     const animateElements = () => {
//         const elements = document.querySelectorAll('.animate-on-scroll');
//
//         elements.forEach(element => {
//             const elementPosition = element.getBoundingClientRect().top;
//             const windowHeight = window.innerHeight;
//
//             if (elementPosition < windowHeight - 100) {
//                 element.classList.add('animated');
//             }
//         });
//     };
//
//     // Header scroll effect
//     const header = document.querySelector('header');
//
//     const headerScrollEffect = () => {
//         if (window.scrollY > 100) {
//             header.classList.add('scrolled');
//         } else {
//             header.classList.remove('scrolled');
//         }
//     };
//
//     // Mobile navigation toggle
//     const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
//     const mainNav = document.querySelector('.main-nav');
//
//     if (mobileNavToggle) {
//         mobileNavToggle.addEventListener('click', function() {
//             if (mainNav.style.display === 'flex') {
//                 mainNav.style.display = 'none';
//                 this.innerHTML = '<i class="fas fa-bars"></i>';
//             } else {
//                 mainNav.style.display = 'flex';
//                 this.innerHTML = '<i class="fas fa-times"></i>';
//             }
//         });
//     }
//
//     // Newsletter form submission with AJAX
//     const newsletterForm = document.querySelector('.newsletter-form');
//     if (newsletterForm) {
//         newsletterForm.addEventListener('submit', function(e) {
//             e.preventDefault();
//
//             const email = this.querySelector('input[name="email"]').value;
//             const csrfToken = this.querySelector('input[name="csrfmiddlewaretoken"]').value;
//
//             fetch(this.action, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/x-www-form-urlencoded',
//                     'X-CSRFToken': csrfToken
//                 },
//                 body: `email=${encodeURIComponent(email)}`
//             })
//             .then(response => response.json())
//             .then(data => {
//                 // Create a notification element
//                 const notification = document.createElement('div');
//                 notification.className = data.success ? 'notification success' : 'notification error';
//                 notification.textContent = data.message;
//
//                 // Append to body
//                 document.body.appendChild(notification);
//
//                 // Show with animation
//                 setTimeout(() => {
//                     notification.classList.add('show');
//                 }, 10);
//
//                 // Remove after 3 seconds
//                 setTimeout(() => {
//                     notification.classList.remove('show');
//                     setTimeout(() => {
//                         document.body.removeChild(notification);
//                     }, 300);
//                 }, 3000);
//
//                 if (data.success) {
//                     this.reset();
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//             });
//         });
//     }
//
//     // Add .animate-on-scroll class to elements that should animate
//     const addAnimationClasses = () => {
//         document.querySelectorAll('.section-title, .trailer-card, .portfolio-item, .workshop-card, .stat-item').forEach(element => {
//             element.classList.add('animate-on-scroll');
//         });
//     };
//
//     // Run once on load
//     addAnimationClasses();
//     headerScrollEffect();
//     animateElements();
//
//     // Add event listeners
//     window.addEventListener('scroll', headerScrollEffect);
//     window.addEventListener('scroll', animateElements);
//     window.addEventListener('resize', function() {
//         if (window.innerWidth > 768 && mainNav) {
//             mainNav.style.display = '';
//         }
//     });
//
//     // Smooth scrolling for anchor links
//     document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//         anchor.addEventListener('click', function(e) {
//             e.preventDefault();
//
//             const targetId = this.getAttribute('href');
//             if (targetId === '#') return;
//
//             const targetElement = document.querySelector(targetId);
//             if (targetElement) {
//                 window.scrollTo({
//                     top: targetElement.offsetTop - 100,
//                     behavior: 'smooth'
//                 });
//             }
//         });
//     });
//
//     // Add parallax effect to hero section
//     const hero = document.querySelector('.hero');
//     if (hero) {
//         window.addEventListener('scroll', function() {
//             const scrollPosition = window.scrollY;
//             hero.style.backgroundPositionY = scrollPosition * 0.5 + 'px';
//         });
//     }
// });
//
// // Add additional class to the appropriate sections
// document.addEventListener('DOMContentLoaded', function() {
//     // Mark sections for animations
//     const sections = document.querySelectorAll('section');
//     sections.forEach((section, index) => {
//         if (index % 2 === 0) {
//             section.classList.add('section-light');
//         } else {
//             section.classList.add('section-dark');
//         }
//     });
// });
// // Initialize Swiper slider for trailers
// document.addEventListener('DOMContentLoaded', function() {
//     // Initialize Swiper
//     const trailersSlider = new Swiper('.trailers-slider', {
//         slidesPerView: 1,
//         spaceBetween: 30,
//         centeredSlides: true,
//         loop: true,
//         loopAdditionalSlides: 30,
//         speed: 800,
//         autoplay: {
//             delay: 5000,
//             disableOnInteraction: false,
//         },
//         pagination: {
//             el: '.swiper-pagination',
//             clickable: true,
//         },
//         navigation: {
//             nextEl: '.swiper-button-next',
//             prevEl: '.swiper-button-prev',
//         },
//         breakpoints: {
//             640: {
//                 slidesPerView: 2,
//                 spaceBetween: 20,
//             },
//             992: {
//                 slidesPerView: 3,
//                 spaceBetween: 30,
//             },
//         },
//         on: {
//             init: function() {
//                 // Add index as custom property for staggered animations
//                 document.querySelectorAll('.swiper-slide').forEach((slide, index) => {
//                     slide.style.setProperty('--index', index);
//                 });
//             },
//         },
//     });
//
//     // Handle trailer modal
//     const trailerModal = document.getElementById('trailerModal');
//     const trailerFrame = document.getElementById('trailerFrame');
//     const trailerModalTitle = document.getElementById('trailerModalTitle');
//     const closeModal = document.querySelector('.close-modal');
//
//     // Open modal when watch button is clicked
//     document.querySelectorAll('.btn-watch').forEach(button => {
//         button.addEventListener('click', function() {
//             const trailerUrl = this.getAttribute('data-trailer-url');
//             const trailerTitle = this.getAttribute('data-trailer-title');
//
//             // Set iframe source to YouTube or Vimeo URL
//             // Convert URL to embed format if needed
//             let embedUrl = trailerUrl;
//
//             // Handle YouTube links
//             if (trailerUrl.includes('youtube.com/watch?v=')) {
//                 const videoId = trailerUrl.split('v=')[1].split('&')[0];
//                 embedUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
//             }
//             // Handle Vimeo links
//             else if (trailerUrl.includes('vimeo.com/')) {
//                 const videoId = trailerUrl.split('/').pop();
//                 embedUrl = `https://player.vimeo.com/video/${videoId}?autoplay=1`;
//             }
//
//             trailerFrame.src = embedUrl;
//             trailerModalTitle.textContent = trailerTitle;
//
//             // Show modal with animation
//             trailerModal.classList.add('show');
//
//             // Prevent body scrolling
//             document.body.style.overflow = 'hidden';
//         });
//     });
//
//     // Close modal when close button is clicked
//     if (closeModal) {
//         closeModal.addEventListener('click', function() {
//             closeTrailerModal();
//         });
//     }
//
//     // Close modal when clicking outside content
//     if (trailerModal) {
//         trailerModal.addEventListener('click', function(e) {
//             if (e.target === trailerModal) {
//                 closeTrailerModal();
//             }
//         });
//     }
//
//     // Close modal when ESC key is pressed
//     document.addEventListener('keydown', function(e) {
//         if (e.key === 'Escape' && trailerModal.classList.contains('show')) {
//             closeTrailerModal();
//         }
//     });
//
//     function closeTrailerModal() {
//         trailerModal.classList.remove('show');
//         setTimeout(() => {
//             trailerFrame.src = '';
//         }, 300);
//         document.body.style.overflow = '';
//     }
// });
// // Notification CSS to add to your main.css
// document.head.insertAdjacentHTML('beforeend', `
// <style>
// .notification {
//     position: fixed;
//     bottom: 30px;
//     right: 30px;
//     padding: 15px 25px;
//     border-radius: 8px;
//     color: white;
//     font-weight: 500;
//     box-shadow: 0 5px 15px rgba(0,0,0,0.3);
//     transform: translateY(100px);
//     opacity: 0;
//     transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
//     z-index: 9999;
// }
//
// .notification.success {
//     background: linear-gradient(to right, #28a745, #218838);
// }
//
// .notification.error {
//     background: linear-gradient(to right, #dc3545, #c82333);
// }
//
// .notification.show {
//     transform: translateY(0);
//     opacity: 1;
// }
//
// /* Additional animation classes */
// .animate-on-scroll {
//     opacity: 0;
//     transform: translateY(30px);
//     transition: opacity 0.8s ease, transform 0.8s ease;
// }
//
// .animate-on-scroll.animated {
//     opacity: 1;
//     transform: translateY(0);
// }
//
// /*.trailer-card.animate-on-scroll {*/
// /*    transition-delay: calc(0.1s * var(--index, 0));*/
// /*}*/
//
// /*.portfolio-item.animate-on-scroll {*/
// /*    transition-delay: calc(0.15s * var(--index, 0));*/
// /*}*/
//
// /*.workshop-card.animate-on-scroll {*/
// /*    transition-delay: calc(0.2s * var(--index, 0));*/
// /*}*/
// </style>
// `);
// Initialized on document load
document.addEventListener('DOMContentLoaded', function() {
    // Header scroll effect
    const header = document.querySelector('header');
    const scrollThreshold = 100;

    function handleScroll() {
        if (window.scrollY > scrollThreshold) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }

    // Mobile navigation toggle
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (mobileNavToggle) {
        mobileNavToggle.addEventListener('click', function() {
            const isVisible = mainNav.style.display === 'flex';
            mainNav.style.display = isVisible ? 'none' : 'flex';
            this.innerHTML = isVisible ?
                '<i class="fas fa-bars"></i>' :
                '<i class="fas fa-times"></i>';
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Initialize Swiper for trailers
    if (typeof Swiper !== 'undefined' && document.querySelector('.trailers-slider')) {
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
            }
        });
    }

    // Handle trailer modal
    const trailerModal = document.getElementById('trailerModal');
    const trailerFrame = document.getElementById('trailerFrame');
    const trailerModalTitle = document.getElementById('trailerModalTitle');
    const closeModalBtn = document.querySelector('.close-modal');

    if (trailerModal) {
        // Open modal when watch button is clicked
        document.querySelectorAll('.btn-watch').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const trailerUrl = this.getAttribute('data-trailer-url');
                const trailerTitle = this.getAttribute('data-trailer-title');

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
                if (trailerModalTitle) trailerModalTitle.textContent = trailerTitle || 'Trailer';

                // Show modal with animation
                trailerModal.classList.add('show');

                // Prevent body scrolling
                document.body.style.overflow = 'hidden';
            });
        });

        // Close modal when close button is clicked
        if (closeModalBtn) {
            closeModalBtn.addEventListener('click', closeTrailerModal);
        }

        // Close modal when clicking outside content
        trailerModal.addEventListener('click', function(e) {
            if (e.target === trailerModal) {
                closeTrailerModal();
            }
        });

        // Close modal when ESC key is pressed
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && trailerModal.classList.contains('show')) {
                closeTrailerModal();
            }
        });
    }

    function closeTrailerModal() {
        if (!trailerModal) return;
        trailerModal.classList.remove('show');
        setTimeout(() => {
            trailerFrame.src = '';
        }, 300);
        document.body.style.overflow = '';
    }

    // Payment Tab Switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Add active class to current button and corresponding pane
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab') + '-tab';
            const pane = document.getElementById(tabId);
            if (pane) pane.classList.add('active');
        });
    });

    // Newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Extract form data
            const formData = new FormData(this);
            const email = formData.get('email');

            if (!email || !validateEmail(email)) {
                showNotification('error', 'Please enter a valid email address');
                return;
            }

            // AJAX form submission
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('success', data.message || 'Successfully subscribed!');
                    this.reset();
                } else {
                    showNotification('error', data.error || 'Subscription failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('error', 'An error occurred. Please try again.');
            });
        });
    }

    // Utility functions
    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    function showNotification(type, message) {
        // Create notification element if it doesn't exist
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        // Show with animation
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        // Auto-remove after delay
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    }

    // Initialize animations and handlers
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && mainNav) {
            mainNav.style.display = '';
        }
    });

    // Run once on page load
    handleScroll();
});
// Remove or comment out the mobile navigation toggle code
// Instead, add this for smooth horizontal scrolling
document.addEventListener('DOMContentLoaded', function() {
    // Horizontal nav scroll buttons for small screens
    const mainNav = document.querySelector('.main-nav');

    if (mainNav && window.innerWidth <= 768) {
        // Add smooth scrolling for nav items
        mainNav.addEventListener('wheel', function(e) {
            if (e.deltaY !== 0) {
                e.preventDefault();
                this.scrollLeft += e.deltaY;
            }
        });

        // Optional: Scroll to active menu item on page load
        const activeItem = mainNav.querySelector('li a.active');
        if (activeItem) {
            activeItem.scrollIntoView({ behavior: 'smooth', inline: 'center' });
        }
    }

    // Other existing code...
});
// Mobile navigation toggle for horizontal menu
document.addEventListener('DOMContentLoaded', function() {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (mobileNavToggle && mainNav) {
        mobileNavToggle.addEventListener('click', function() {
            const isVisible = mainNav.style.display === 'flex';

            if (isVisible) {
                mainNav.style.display = 'none';
                this.innerHTML = '<i class="fas fa-bars"></i>';
            } else {
                mainNav.style.display = 'flex';
                this.innerHTML = '<i class="fas fa-times"></i>';

                // Scroll to active menu item if exists
                const activeItem = mainNav.querySelector('li a.active');
                if (activeItem) {
                    setTimeout(() => {
                        activeItem.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
                    }, 100);
                }
            }
        });

        // Handle horizontal scrolling when menu is open
        mainNav.addEventListener('wheel', function(e) {
            if (e.deltaY !== 0) {
                e.preventDefault();
                this.scrollLeft += e.deltaY;
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768 &&
                mainNav.style.display === 'flex' &&
                !mainNav.contains(e.target) &&
                e.target !== mobileNavToggle) {
                mainNav.style.display = 'none';
                mobileNavToggle.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });

        // Close menu when window is resized to desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                mainNav.style.display = '';
                mobileNavToggle.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });
    }
});
// Mobile navigation toggle for horizontal menu
document.addEventListener('DOMContentLoaded', function() {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (mobileNavToggle && mainNav) {
        // Toggle menu visibility when clicking the button
        mobileNavToggle.addEventListener('click', function() {
            const isVisible = mainNav.style.display === 'flex';

            if (isVisible) {
                mainNav.style.display = 'none';
                this.innerHTML = '<i class="fas fa-bars"></i>';
            } else {
                mainNav.style.display = 'flex';
                this.innerHTML = '<i class="fas fa-times"></i>';
            }
        });

        // Handle horizontal scrolling when menu is open
        mainNav.addEventListener('wheel', function(e) {
            if (e.deltaY !== 0) {
                e.preventDefault();
                this.scrollLeft += e.deltaY;
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768 &&
                mainNav.style.display === 'flex' &&
                !mainNav.contains(e.target) &&
                e.target !== mobileNavToggle) {
                mainNav.style.display = 'none';
                mobileNavToggle.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });

        // Reset display property when resizing to desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                mainNav.style.display = '';
                mobileNavToggle.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });
    }
});
