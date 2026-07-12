let clicked = false;

document.querySelectorAll('.skill').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.classList.toggle('clicked');

        clicked = !clicked;
        btn.dataset.umamiEvent = clicked ? 'Cerrar descripción de habilidad' : 'Abrir descripción de habilidad';
    });
});