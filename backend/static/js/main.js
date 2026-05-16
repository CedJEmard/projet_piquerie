const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
}

const modal = document.getElementById('bookingModal');

const openButtons = document.querySelectorAll('.open-booking');

const closeModal = document.getElementById('closeModal');

const closeModalMobile = document.getElementById('closeModalMobile');

if (modal) {

    openButtons.forEach(button => {

        button.addEventListener('click', () => {
            modal.classList.add('active');
        });

    });

    if (closeModal) {

        closeModal.addEventListener('click', () => {
            modal.classList.remove('active');
        });

    }

    if (closeModalMobile) {

        closeModalMobile.addEventListener('click', () => {
            modal.classList.remove('active');
        });

    }

    modal.addEventListener('click', event => {

        if (event.target === modal) {
            modal.classList.remove('active');
        }

    });
}