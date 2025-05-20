document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.custom-dashboard .tab');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => {
                if (t !== tab) {
                    t.classList.remove(
                        'bg-white', 'shadow-xs', 'text-font-important-light', 'hover:bg-white',
                        'dark:bg-base-900', 'dark:hover:bg-base-900', 'dark:text-font-important-dark'
                    );
                    t.classList.add(
                        'text-font-subtle-light', 'dark:text-font-subtle-dark',
                        'hover:bg-base-700/[.04]', 'dark:hover:bg-white/[.04]'
                    );
                }
            });

            tab.classList.remove(
                'text-font-subtle-light', 'dark:text-font-subtle-dark',
                'hover:bg-base-700/[.04]', 'dark:hover:bg-white/[.04]'
            );
            tab.classList.add(
                'bg-white', 'shadow-xs', 'text-font-important-light', 'hover:bg-white',
                'dark:bg-base-900', 'dark:hover:bg-base-900', 'dark:text-font-important-dark'
            );
        });
    });
});
