document.addEventListener('DOMContentLoaded', () => {
    const navMenu = document.getElementById('nav-menu');
    const underline = document.getElementById('nav-underline');
    const links = navMenu.querySelectorAll('.nav-link');
    let activeLink = links[0];
    let currentContent = document.getElementById('content-inicio');
    let isAnimating = false;

    function moveUnderlineTo(element, show = true) {
        const rect = element.getBoundingClientRect();
        const parentRect = navMenu.getBoundingClientRect();
        underline.style.left = (rect.left - parentRect.left) + "px";
        underline.style.width = rect.width + "px";
        underline.style.opacity = show ? 1 : 0;
    }

    moveUnderlineTo(activeLink, true);

    links.forEach(link => {
        // 🟦 Hover visual
        link.addEventListener('mouseover', () => moveUnderlineTo(link, true));
        link.addEventListener('mouseout', () => moveUnderlineTo(activeLink, true));

        // 🟨 Clic para cambiar sección
        link.addEventListener('click', function (e) {
            e.preventDefault();
            if (isAnimating) return;

            const target = this.getAttribute('data-target');
            const newContent = document.getElementById('content-' + target);

            if (newContent !== currentContent) {
                isAnimating = true;
                const direction = Array.from(links).indexOf(this) > Array.from(links).indexOf(activeLink) ? 'right' : 'left';

                currentContent.classList.add(direction === 'right' ? 'animate-slide-out-left' : 'animate-slide-out-right');

                currentContent.addEventListener('animationend', () => {
                    currentContent.classList.add('hidden');
                    currentContent.classList.remove('animate-slide-out-left', 'animate-slide-out-right');

                    newContent.classList.remove('hidden');
                    newContent.classList.add(direction === 'right' ? 'animate-slide-in-right' : 'animate-slide-in-left');

                    newContent.addEventListener('animationend', () => {
                        newContent.classList.remove('animate-slide-in-right', 'animate-slide-in-left');
                        isAnimating = false;
                    }, { once: true });

                    currentContent = newContent;
                    activeLink = link;
                    moveUnderlineTo(link, true);
                }, { once: true });
            }
        });
    });
});
