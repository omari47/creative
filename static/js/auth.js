document.addEventListener('DOMContentLoaded', function() {
    // Add animation delay to feature items
    // const featureItems = document.querySelectorAll('.feature-item');
    // featureItems.forEach((item, index) => {
    //     item.style.setProperty('--i', index);
    // });

    // Form submission animation
    const loginForm = document.getElementById('loginForm');
    const loginButton = loginForm.querySelector('.btn-auth');

    loginForm.addEventListener('submit', function(e) {
        // Don't prevent default - let form submit normally

        // Add loading animation to button
        loginButton.classList.add('submitting');
        loginButton.querySelector('.btn-text').textContent = 'Logging in...';

        // Add a small shake animation to input fields that are empty
        const inputs = loginForm.querySelectorAll('input[required]');
        inputs.forEach(input => {
            if (!input.value) {
                input.parentElement.classList.add('shake');
                setTimeout(() => {
                    input.parentElement.classList.remove('shake');
                }, 500);
            }
        });
    });

    // Input animations
    const inputs = document.querySelectorAll('.input-icon-wrapper input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
});