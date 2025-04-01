// Modal functionality
function showLoginModal() {
  document.getElementById('loginModal').classList.add('active');
  document.body.style.overflow = 'hidden'; // Prevent scrolling
}

function showRegisterModal() {
  document.getElementById('registerModal').classList.add('active');
  document.body.style.overflow = 'hidden'; // Prevent scrolling
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.remove('active');
  document.body.style.overflow = ''; // Re-enable scrolling
}

// Handle clicks outside the modal to close it
document.addEventListener('click', function(event) {
  const loginModal = document.getElementById('loginModal');
  const registerModal = document.getElementById('registerModal');

  if (event.target === loginModal) {
    closeModal('loginModal');
  }

  if (event.target === registerModal) {
    closeModal('registerModal');
  }
});

// Handle Escape key to close modals
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    closeModal('loginModal');
    closeModal('registerModal');
  }
});

// Form animation effects
document.addEventListener('DOMContentLoaded', function() {
  // Add focus line animation to all inputs in modals
  const modalInputs = document.querySelectorAll('.modal-container input');

  modalInputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.nextElementSibling.style.width = '100%';
    });

    input.addEventListener('blur', function() {
      if (this.value.length === 0) {
        this.nextElementSibling.style.width = '0';
      }
    });

    // Check if input already has value on page load
    if (input.value.length > 0) {
      input.nextElementSibling.style.width = '100%';
    }
  });

  // Ajax form submission to prevent page reload
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');

  if (loginForm) {
    loginForm.addEventListener('submit', handleFormSubmit);
  }

  if (registerForm) {
    registerForm.addEventListener('submit', handleFormSubmit);
  }

  function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const url = form.getAttribute('action');
    const formData = new FormData(form);

    fetch(url, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.location.reload(); // Reload page to show authenticated state
      } else {
        // Show error messages
        const messageContainer = form.querySelector('.auth-messages');
        messageContainer.innerHTML = ''; // Clear previous messages

        if (data.errors) {
          const errorDiv = document.createElement('div');
          errorDiv.className = 'auth-message error';
          errorDiv.innerHTML = `
            <i class="fas fa-exclamation-circle"></i>
            <p>${data.errors}</p>
          `;
          messageContainer.appendChild(errorDiv);
        }
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  // Show modals if URL parameters indicate so
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('login') === 'true') {
    showLoginModal();
  }
  if (urlParams.get('register') === 'true') {
    showRegisterModal();
  }
});