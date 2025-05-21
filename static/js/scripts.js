document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.custom-dashboard .tab');

    if (performance.navigation.type === 1) {
        console.log("Page was reloaded");
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const tabName = e.target.textContent.trim().toLowerCase();

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

            const csrftoken = getCookie('csrftoken');

            fetch("/set-tab-session/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ tab: tabName })
            }).then(() => {
                window.location.reload();
            });

        });
    });
});
