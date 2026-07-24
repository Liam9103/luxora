document.addEventListener('DOMContentLoaded', function () {
    AOS.init({
        duration: 800,
        once: true,
    });

    // فرمت خودکار شماره کارت در درگاه بانکی فیک
    const cardInput = document.querySelector('.card-input');
    if (cardInput) {
        cardInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '').slice(0, 16);
            e.target.value = value.replace(/(.{4})/g, '$1 ').trim();
        });
    }

    // افکت تغییر نوبار هنگام اسکرول
    window.addEventListener('scroll', function () {
        const navbar = document.querySelector('.custom-navbar');
        if (navbar) {
            navbar.style.boxShadow = window.scrollY > 50 ? '0 5px 20px rgba(0,0,0,0.3)' : 'none';
        }
    });
});