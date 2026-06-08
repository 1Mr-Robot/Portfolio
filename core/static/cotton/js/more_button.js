// Estado global: si las cards extra están expandidas o no
let expanded = false;

// Actualiza las cards que llevarán la clase .extra
function updateCardExtras(section, target) {
    const cards = document.querySelectorAll(target);
    const width = window.innerWidth;

    // >=1400px  -> primeras 4 no tienen .extra
    // 992-1399  -> primeras 3 no tienen .extra
    // 768-991   -> primeras 4 no tienen .extra
    // <=767     -> primeras 3 no tienen .extra
    let visibleCount;
    if (section == 'projects') {
        visibleCount = (width >= 1400 || (width >= 768 && width <= 991)) ? 4 : 3;
    } else {
        visibleCount = 2;
    }

    cards.forEach((card, idx) => {
        if (idx < visibleCount) {
            card.classList.remove('extra');
        } else {
            card.classList.add('extra');

            // Reaplicar estado si está expandido
            if (expanded) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        }
    });
}

// Resize con debounce (pero sin romper estado)
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        updateCardExtras('projects', '#card_container .card');
    }, 150);
});

document.addEventListener('DOMContentLoaded', () => {
    const processedSections = new Set();

    // Botón mostrar/ocultar
    document.querySelectorAll('.more_btn').forEach(btn => {
        const section = btn.dataset.section
        const target = btn.dataset.target

        if (!processedSections.has(section)) {
            processedSections.add(section);

            updateCardExtras(section, target);
        }

        btn.addEventListener('click', () => {
            expanded = !expanded;

            const section = btn.dataset.section
            const extras = document.querySelectorAll(`#${section} .extra`);
            extras.forEach(element => {
                element.classList.toggle('active', expanded);
            });

            const icon = btn.querySelector('.more_btn_icon');
            const text = btn.querySelector('.more_btn_text');

            if (icon) icon.classList.toggle('rotated', expanded);
            if (text) text.classList.add('changed');

            setTimeout(() => {
                if (text) {
                    text.textContent = expanded ? btn.dataset.show : btn.dataset.hidden;
                    text.classList.remove('changed');
                }
            }, 250);
        });
    });
});