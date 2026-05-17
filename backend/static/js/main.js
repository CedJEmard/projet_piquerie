// MOBILE MENU
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
}


// MODAL HELPERS
function openModal(modal) {
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modal) {
    if (modal) {
        modal.classList.remove('active');
    }
}


// BOOKING MODAL
const bookingModal = document.getElementById('bookingModal');
const openBookingButtons = document.querySelectorAll('.open-booking');
const closeBookingModal = document.getElementById('closeModal');

openBookingButtons.forEach(button => {
    button.addEventListener('click', () => {
        openModal(bookingModal);
    });
});

if (closeBookingModal) {
    closeBookingModal.addEventListener('click', () => {
        closeModal(bookingModal);
    });
}

if (bookingModal) {
    bookingModal.addEventListener('click', event => {
        if (event.target === bookingModal) {
            closeModal(bookingModal);
        }
    });
}


// DOCUMENT MODAL
const documentModal = document.getElementById('documentModal');
const openDocumentModal = document.getElementById('openDocumentModal');
const closeDocumentModal = document.getElementById('closeDocumentModal');

if (documentModal && openDocumentModal && closeDocumentModal) {
    openDocumentModal.addEventListener('click', () => {
        openModal(documentModal);
    });

    closeDocumentModal.addEventListener('click', () => {
        closeModal(documentModal);
    });

    documentModal.addEventListener('click', event => {
        if (event.target === documentModal) {
            closeModal(documentModal);
        }
    });
}


// BOOKING WIZARD
const bookingSteps = document.querySelectorAll('.booking-step');
const bookingNextButtons = document.querySelectorAll('.booking-next');
const bookingNextStep1 = bookingNextButtons[0];
const bookingNextStep2 = bookingNextButtons[1];
const bookingNextStep3 = bookingNextButtons[2];
const bookingBackButton = document.getElementById('bookingBackButton');

let currentBookingStep = 1;

function showBookingStep(stepNumber) {
    currentBookingStep = stepNumber;

    bookingSteps.forEach(step => {
        step.classList.toggle(
            'active',
            Number(step.dataset.step) === currentBookingStep
        );
    });

    if (bookingBackButton) {
        bookingBackButton.classList.toggle(
            'visible',
            currentBookingStep > 1
        );
    }
}

function updateBookingButtons() {

    if (bookingNextStep1) {

        bookingNextStep1.disabled = !(
            regionSelect.value &&
            serviceSelect.value
        );

    }

    if (bookingNextStep2) {

        bookingNextStep2.disabled =
            !appointmentDatePicker.value;

    }

    if (bookingNextStep3) {

        bookingNextStep3.disabled =
            !selectedAppointmentDate.value;

    }

}

function canGoNext() {
    if (currentBookingStep === 1) {
        return regionSelect.value && serviceSelect.value;
    }

    if (currentBookingStep === 2) {
        return appointmentDatePicker.value;
    }

    if (currentBookingStep === 3) {
        return selectedAppointmentDate.value;
    }

    return true;
}

bookingNextButtons.forEach(button => {
    button.addEventListener('click', () => {
        if (!canGoNext()) {
            alert('Veuillez compléter cette étape avant de continuer.');
            return;
        }

        if (currentBookingStep < 4) {
            showBookingStep(currentBookingStep + 1);
        }
    });
});

if (bookingBackButton) {
    bookingBackButton.addEventListener('click', () => {
        if (currentBookingStep > 1) {
            showBookingStep(currentBookingStep - 1);
        }
    });
}

showBookingStep(1);


// CALENDAR + TIME SLOTS
const regionSelect = document.getElementById('regionSelect');
const serviceSelect = document.getElementById('serviceSelect');
const calendarGrid = document.getElementById('calendarGrid');
const calendarTitle = document.getElementById('calendarTitle');
const prevMonth = document.getElementById('prevMonth');
const nextMonth = document.getElementById('nextMonth');
const appointmentDatePicker = document.getElementById('appointmentDatePicker');
const timeSlots = document.getElementById('timeSlots');
const selectedAppointmentDate = document.getElementById('selectedAppointmentDate');

let currentCalendarDate = new Date();

function formatDateForApi(date) {
    return date.toISOString().split('T')[0];
}

async function renderCalendar() {
    if (!calendarGrid || !calendarTitle) {
        return;
    }

    calendarGrid.innerHTML = '';

    const year = currentCalendarDate.getFullYear();
    const month = currentCalendarDate.getMonth();

    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);

    calendarTitle.textContent = firstDay.toLocaleDateString('fr-CA', {
        month: 'long',
        year: 'numeric'
    });

    const startOffset = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;

    for (let i = 0; i < startOffset; i++) {
        const empty = document.createElement('div');
        calendarGrid.appendChild(empty);
    }

    const monthValue =
    `${year}-${String(month + 1).padStart(2, '0')}`;

let availableDays = [];

if (
    regionSelect.value &&
    serviceSelect.value
) {

    const response = await fetch(
        `/api/jours-disponibles/?region=${regionSelect.value}&service=${serviceSelect.value}&month=${monthValue}`
    );

    const data = await response.json();

    availableDays = data.days;

}

for (let day = 1; day <= lastDay.getDate(); day++) {

    const date = new Date(year, month, day);

    const isoDate = formatDateForApi(date);

    const button = document.createElement('button');

    button.type = 'button';

    button.className = 'calendar-day';

    button.textContent = day;

    const isAvailable =
        availableDays.includes(isoDate);

    if (isAvailable) {

        button.classList.add('available');

        button.addEventListener('click', async () => {

            document
                .querySelectorAll('.calendar-day')
                .forEach(btn => {
                    btn.classList.remove('selected');
                });

            button.classList.add('selected');

            appointmentDatePicker.value = isoDate;

            await loadTimeSlots(isoDate);

            showBookingStep(3);

        });

    } else {

        button.classList.add('disabled');

    }

    calendarGrid.appendChild(button);

}
}

async function loadTimeSlots(date) {
    if (
        !regionSelect ||
        !serviceSelect ||
        !timeSlots ||
        !selectedAppointmentDate
    ) {
        return;
    }

    timeSlots.innerHTML = '';

    const response = await fetch(
        `/api/disponibilites/?region=${regionSelect.value}&service=${serviceSelect.value}&date=${date}`
    );

    const data = await response.json();

    if (data.slots.length === 0) {
        timeSlots.innerHTML = '<p>Aucune disponibilité pour cette journée.</p>';
        return;
    }

    data.slots.forEach(slot => {
        const button = document.createElement('button');

        button.type = 'button';
        button.className = 'time-slot';
        button.textContent = slot.label;

        button.addEventListener('click', () => {
            document.querySelectorAll('.time-slot').forEach(btn => {
                btn.classList.remove('selected');
            });

            button.classList.add('selected');

            selectedAppointmentDate.value = slot.value;

            setTimeout(() => {
                showBookingStep(4);
            }, 200);
        });

        timeSlots.appendChild(button);
    });
}

if (prevMonth) {
    prevMonth.addEventListener('click', () => {
        currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
        renderCalendar();
    });
}

if (nextMonth) {
    nextMonth.addEventListener('click', () => {
        currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
        renderCalendar();
    });
}

if (regionSelect && serviceSelect) {

    regionSelect.addEventListener('change', () => {

        renderCalendar();

        updateBookingButtons();

    });

    serviceSelect.addEventListener('change', () => {

        renderCalendar();

        updateBookingButtons();

    });

}

renderCalendar();

const bookingForm = document.getElementById('bookingForm');

if (bookingForm) {
    bookingForm.addEventListener('submit', event => {
        if (!selectedAppointmentDate.value) {
            event.preventDefault();
            alert('Veuillez choisir une heure de rendez-vous.');
        }
    });
}