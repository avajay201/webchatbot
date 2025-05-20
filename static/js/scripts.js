document.addEventListener('DOMContentLoaded', ()=>{
    const tabs = document.querySelectorAll('.custom-dashboard .tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', e => {
            tabs.forEach(t => t.classList.remove('active', 'shadow-lg'));
            tab.classList.add('active', 'shadow-lg');
        });
    });
})