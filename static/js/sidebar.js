document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const a = sidebar.querySelectorAll('a');
    const i = sidebar.querySelectorAll('i');
    const img = sidebar.querySelectorAll('img');
    const toggleBtn = document.getElementById('toggleSidebar');
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        setTimeout(() => {
        sidebar.classList.add('collapsed');
       if(sidebar.classList.contains('collapsed')) {
            a.forEach(link => {
                link.classList.add('icon');
            });
            i.forEach(icon => {
                icon.classList.add('i');
            });
            img.forEach(image => {
                image.classList.add('i');
            });
            localStorage.setItem('sidebarCollapsed', 'true');
        }
    });
    }

    toggleBtn.addEventListener('click', function() {
        if (window.innerWidth <= 768) {
            toggleMobileMenu();
        } else {
            sidebar.classList.toggle('collapsed');
            if(sidebar.classList.contains('collapsed')) {
            a.forEach(link => {
                link.classList.add('icon');
            });
            i.forEach(icon => {
                icon.classList.add('i');
            });
            img.forEach(image => {
                image.classList.add('i');
            });
            localStorage.setItem('sidebarCollapsed', 'true');
        }
        else{
            a.forEach(link => {
                link.classList.remove('icon');
            });
            i.forEach(icon => {
                icon.classList.remove('i');
            });
            img.forEach(image => {
                image.classList.remove('i');
            });
            localStorage.setItem('sidebarCollapsed', 'false');
        }
        }
    });
    
    if (mobileMenuToggle) {
        a.forEach(link => {
                link.classList.remove('icon');
            });
            i.forEach(icon => {
                icon.classList.remove('i');
            });
            img.forEach(image => {
                image.classList.remove('i');
            });
        mobileMenuToggle.addEventListener('click', function() {
            toggleMobileMenu();
        });
    }
    
    function toggleMobileMenu() {
        sidebar.classList.toggle('show');
         a.forEach(link => {
                link.classList.remove('icon');
            });
            i.forEach(icon => {
                icon.classList.remove('i');
            });
            img.forEach(image => {
                image.classList.remove('i');
            });
        const menuOverlay = document.getElementById('menuOverlay');
        if (menuOverlay) {
            menuOverlay.classList.toggle('visible', sidebar.classList.contains('show'));
        }
        
        const menuIcon = sidebar.classList.contains('show') ? 'fa-times' : 'fa-bars';
        
        if (mobileMenuToggle) {
            mobileMenuToggle.innerHTML = `<i class="fas ${menuIcon}"></i>`;
        }
        
        toggleBtn.innerHTML = `<i class="fas ${menuIcon}"></i>`;
        
        document.body.classList.toggle('menu-open', sidebar.classList.contains('show'));
    }
        const preservedHtml = toggleBtn.innerHTML;

    function checkScreenSize() {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('collapsed');
            sidebar.classList.remove('show');
            if (mobileMenuToggle) {
                mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
                mobileMenuToggle.classList.add('visible');
            }


            toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
            
            document.body.classList.remove('menu-open');
        } else {
            sidebar.classList.remove('show');
            if(toggleBtn.classList.contains('collapsed')) {
                  a.forEach(link => {
                link.classList.add('icon');
            });
            i.forEach(icon => {
                icon.classList.add('i');
            });
            img.forEach(image => {
                image.classList.add('i');
            });
            }
            else{
                  a.forEach(link => {
                link.classList.remove('icon');
            });
            i.forEach(icon => {
                icon.classList.remove('i');
            });
            img.forEach(image => {
                image.classList.remove('i');
            });
            }
            if (mobileMenuToggle) {
                mobileMenuToggle.classList.remove('visible');
                mobileMenuToggle.classList.add('hidden');

            }
            
            if(preservedHtml !== "") {
             toggleBtn.innerHTML = preservedHtml;
             console.log(preservedHtml);
            }

            document.body.classList.remove('menu-open');
        }
    }
    
    checkScreenSize();
    
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(checkScreenSize, 250);
    });
    
    document.addEventListener('click', function(event) {
        if (window.innerWidth <= 768 && 
            sidebar.classList.contains('show') &&
            !sidebar.contains(event.target) && 
            !toggleBtn.contains(event.target) &&
            (!mobileMenuToggle || !mobileMenuToggle.contains(event.target))) {
            
            toggleMobileMenu();
        }
    });
    
    const menuOverlay = document.getElementById('menuOverlay');
    if (menuOverlay) {
        menuOverlay.addEventListener('click', function() {
            if (sidebar.classList.contains('show')) {
                toggleMobileMenu();
            }
        });
    }
    
    sidebar.addEventListener('click', function(event) {
        event.stopPropagation();
    });
    
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && sidebar.classList.contains('show') && window.innerWidth <= 768) {
            toggleMobileMenu();
        }
    });
    
    let touchStartX = 0;
    let touchEndX = 0;
    
    document.addEventListener('touchstart', function(event) {
        touchStartX = event.changedTouches[0].screenX;
    }, false);
    
    document.addEventListener('touchend', function(event) {
        touchEndX = event.changedTouches[0].screenX;
        handleSwipe();
    }, false);
    
    function handleSwipe() {
        const swipeThreshold = 100;
        
        if (touchStartX - touchEndX > swipeThreshold && sidebar.classList.contains('show')) {
            toggleMobileMenu();
        }
        
        if (touchEndX - touchStartX > swipeThreshold && !sidebar.classList.contains('show') && window.innerWidth <= 768) {
            toggleMobileMenu();
        }
    }
    
    const menuItems = document.querySelectorAll('.sidebar-menu a');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth <= 768 && sidebar.classList.contains('show')) {
                setTimeout(function() {
                    toggleMobileMenu();
                }, 150);
            }
        });
    });
});
