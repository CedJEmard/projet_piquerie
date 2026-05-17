// Mobile navigation
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
}


// Reusable modal helper
function setupModal({
    modalId,
    openSelector,
    closeSelectors = []
}) {
    const modal = document.getElementById(modalId);
    const openButtons = document.querySelectorAll(openSelector);

    if (!modal || openButtons.length === 0) {
        return;
    }

    function openModal() {
        modal.classList.add('active');
    }

    function closeModal() {
        modal.classList.remove('active');
    }

    openButtons.forEach(button => {
        button.addEventListener('click', openModal);
    });

    closeSelectors.forEach(selector => {
        const closeButton = document.querySelector(selector);

        if (closeButton) {
            closeButton.addEventListener('click', closeModal);
        }
    });

    modal.addEventListener('click', event => {
        if (event.target === modal) {
            closeModal();
        }
    });
}


// Appointment modal
setupModal({
    modalId: 'bookingModal',
    openSelector: '.open-booking',
    closeSelectors: ['#closeModal', '#closeModalMobile']
});


// Medical document modal
const documentModal = document.getElementById('documentModal');

const openDocumentModal =
    document.getElementById('openDocumentModal');

const closeDocumentModal =
    document.getElementById('closeDocumentModal');

if (
    documentModal &&
    openDocumentModal &&
    closeDocumentModal
) {

    openDocumentModal.addEventListener('click', () => {
        documentModal.classList.add('active');
    });

    closeDocumentModal.addEventListener('click', () => {
        documentModal.classList.remove('active');
    });

    documentModal.addEventListener('click', event => {

        if (event.target === documentModal) {
            documentModal.classList.remove('active');
        }

    });

}