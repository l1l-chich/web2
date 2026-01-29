// Кнопка открытия/закрытия сайдбара
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');

if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        sidebar.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    });
}

// Кнопка "Вверх"
const btnUp = document.getElementById('btnUp');

if (btnUp) {
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 400) {
            btnUp.classList.add('show');
        } else {
            btnUp.classList.remove('show');
        }
    });

    btnUp.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Подсветка активной секции (только на главной странице)
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('nav a[data-section]');

    if (sections.length === 0 || navLinks.length === 0) {
        return; // Если нет секций или ссылок, выходим
    }

    const updateActiveLink = () => {
        const scrollPosition = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => link.classList.remove('active'));

                const activeLink = document.querySelector(`nav a[data-section="${sectionId}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    };

    window.addEventListener('scroll', updateActiveLink);
    updateActiveLink();

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            setTimeout(updateActiveLink, 500);
        });
    });
});