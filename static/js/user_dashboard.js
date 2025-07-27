        function toggleReservations() {
            const container = document.getElementById('reservations-container');
            const toggleText = document.getElementById('reservation-toggle-text');
            
            if (container.style.display === 'none') {
                container.style.display = 'grid';
                toggleText.textContent = 'Collapse';
            } else {
                container.style.display = 'none';
                toggleText.textContent = 'Expand';
            }
        }
        
        function searchParkingLots() {
            const searchButton = document.getElementById('search-button');
            const buttonText = searchButton.innerHTML;
            searchButton.innerHTML = '<span class="loading-spinner"></span>';
            searchButton.disabled = true;
            
            setTimeout(() => {
                const searchInput = document.getElementById('search-input').value.toLowerCase();
                const parkingCards = document.querySelectorAll('#parking-lots .parking-card');
                let foundCount = 0;
                
                parkingCards.forEach(card => {
                    const location = card.getAttribute('data-location').toLowerCase();
                    const pincode = card.getAttribute('data-pincode').toLowerCase();
                    
                    if (location.includes(searchInput) || pincode.includes(searchInput)) {
                        card.style.display = 'block';
                        card.style.animation = 'none';
                        card.offsetHeight; 
                        card.style.animation = 'fadeIn 0.5s ease forwards';
                        foundCount++;
                    } else {
                        card.style.display = 'none';
                    }
                });
                
                if (foundCount === 0) {
                    if (!document.getElementById('no-results')) {
                        const noResults = document.createElement('div');
                        noResults.id = 'no-results';
                        noResults.className = 'empty-state';
                        noResults.innerHTML = `
                            <i class="fas fa-search empty-state-icon"></i>
                            <h3>No Results Found</h3>
                            <p>We couldn't find any parking lots matching your search. Try different keywords or clear your search.</p>
                            <button class="empty-state-action" onclick="resetSearch()">Clear Search</button>
                        `;
                        document.getElementById('parking-lots').appendChild(noResults);
                    }
                } else {
                    const noResults = document.getElementById('no-results');
                    if (noResults) {
                        noResults.remove();
                    }
                }
                
                searchButton.innerHTML = buttonText;
                searchButton.disabled = false;
            }, 500);
        }
        
        function resetSearch() {
            document.getElementById('search-input').value = '';
            searchParkingLots();
            
            const filterItems = document.querySelectorAll('.filter-item');
            filterItems.forEach(item => {
                item.classList.remove('active');
            });
            filterItems[0].classList.add('active');
        }
        
        function handleNoResults(foundCount, filterType, filterValue) {
            if (foundCount === 0) {
                if (!document.getElementById('no-results')) {
                    const noResults = document.createElement('div');
                    noResults.id = 'no-results';
                    noResults.className = 'empty-state';
                    
                    let message = '';
                    let icon = 'fas fa-filter';
                    
                    if (filterType === 'price') {
                        icon = 'fas fa-rupee-sign';
                        if (filterValue === 'low') {
                            message = 'No parking lots with low prices found.';
                        } else if (filterValue === 'medium') {
                            message = 'No parking lots with medium prices found.';
                        } else if (filterValue === 'high') {
                            message = 'No parking lots with high prices found.';
                        }
                    } else if (filterType === 'availability') {
                        icon = 'fas fa-parking';
                        message = filterValue === 'high' ? 
                            'No parking lots with high availability found.' : 
                            'No parking lots with low availability found.';
                    }
                    
                    noResults.innerHTML = `
                        <i class="${icon} empty-state-icon"></i>
                        <h3>No Results Found</h3>
                        <p>${message} Try a different filter.</p>
                        <button class="empty-state-action" onclick="resetSearch()">Clear Filters</button>
                    `;
                    document.getElementById('parking-lots').appendChild(noResults);
                }
            } else {
                const noResults = document.getElementById('no-results');
                if (noResults) {
                    noResults.remove();
                }
            }
        }
        
        function filterByPrice(priceRange) {
            const parkingCards = document.querySelectorAll('#parking-lots .parking-card');
            const filterItems = document.querySelectorAll('.filter-item');
            
            filterItems.forEach(item => {
                item.classList.remove('active');
            });
            event.currentTarget.classList.add('active');
            
            let foundCount = 0;
            
            parkingCards.forEach(card => {
                const price = parseFloat(card.getAttribute('data-price'));
                
                if (priceRange === 'all') {
                    card.style.display = 'block';
                    foundCount++;
                } else if (priceRange === 'low' && price < 100) {
                    card.style.display = 'block';
                    foundCount++;
                } else if (priceRange === 'medium' && price >= 100 && price < 500) {
                    card.style.display = 'block';
                    foundCount++;
                } else if (priceRange === 'high' && price >= 500) {
                    card.style.display = 'block';
                    foundCount++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            handleNoResults(foundCount, 'price', priceRange);
        }
        
        function filterByAvailability(availabilityLevel) {
            const parkingCards = document.querySelectorAll('#parking-lots .parking-card');
            const filterItems = document.querySelectorAll('.filter-item');
            
            filterItems.forEach(item => {
                item.classList.remove('active');
            });
            event.currentTarget.classList.add('active');
            
            let foundCount = 0;
            
            parkingCards.forEach(card => {
                const availability = parseFloat(card.getAttribute('data-availability'));
                
                if (availabilityLevel === 'high' && availability >= 0.5) {
                    card.style.display = 'block';
                    foundCount++;
                } else if (availabilityLevel === 'low' && availability < 0.5) {
                    card.style.display = 'block';
                    foundCount++;
                } else if (availabilityLevel === 'all') {
                    card.style.display = 'block';
                    foundCount++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            handleNoResults(foundCount, 'availability', availabilityLevel);
        }
        
        let sortAscending = true;
        function toggleSortOrder() {
            sortAscending = !sortAscending;
            const parkingCardsContainer = document.getElementById('parking-lots');
            const parkingCards = Array.from(parkingCardsContainer.querySelectorAll('.parking-card'));
            
            parkingCards.sort((a, b) => {
                const priceA = parseFloat(a.getAttribute('data-price'));
                const priceB = parseFloat(b.getAttribute('data-price'));
                
                return sortAscending ? priceA - priceB : priceB - priceA;
            });
            
            document.querySelector('#sort-toggle span').textContent = sortAscending ? 'Sort by Price ↑' : 'Sort by Price ↓';
            
            parkingCards.forEach(card => {
                parkingCardsContainer.appendChild(card);
            });
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            const searchInput = document.getElementById('search-input');
            searchInput.addEventListener('keyup', function(event) {
                if (event.key === 'Enter') {
                    searchParkingLots();
                }
            });
            
            const filterItems = document.querySelectorAll('.filter-item');
            filterItems.forEach(item => {
                item.setAttribute('tabindex', '0');
                item.addEventListener('keydown', function(event) {
                    if (event.key === 'Enter' || event.key === ' ') {
                        event.preventDefault();
                        this.click();
                    }
                });
            });
        });
        
        function refreshReservations() {
            const refreshIcon = document.querySelector('.section-action i.fa-sync-alt');
            refreshIcon.classList.add('refreshing');
            
            fetch(window.location.href)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    
                    const newReservationsContainer = doc.querySelector('#reservations-container');
                    
                    const currentReservationsContainer = document.querySelector('#reservations-container');
                    
                    if (newReservationsContainer && currentReservationsContainer) {
                        currentReservationsContainer.innerHTML = newReservationsContainer.innerHTML;
                    }
                    
                    const newStatsCards = doc.querySelector('.dashboard-stats');
                    const currentStatsCards = document.querySelector('.dashboard-stats');
                    
                    if (newStatsCards && currentStatsCards) {
                        currentStatsCards.innerHTML = newStatsCards.innerHTML;
                    }
                    
                    const costUpdateInfo = document.querySelector('.cost-update-info');
                    costUpdateInfo.innerHTML = '<i class="fas fa-check-circle"></i> Data refreshed successfully! Current charges are now up-to-date.';
                    costUpdateInfo.style.backgroundColor = 'rgba(32, 201, 151, 0.1)';
                    costUpdateInfo.style.color = '#20c997';
                    
                    setTimeout(() => {
                        costUpdateInfo.innerHTML = '<i class="fas fa-info-circle"></i> Costs are automatically updated every 10 seconds. Click <b>Refresh</b> to see the latest amounts immediately.';
                        costUpdateInfo.style.backgroundColor = 'rgba(74, 111, 255, 0.1)';
                        costUpdateInfo.style.color = '#4a6fff';
                    }, 3000);
                })
                .catch(error => {
                    console.error('Error refreshing data:', error);
                    const costUpdateInfo = document.querySelector('.cost-update-info');
                    costUpdateInfo.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Could not refresh data. Please try again.';
                    costUpdateInfo.style.backgroundColor = 'rgba(220, 53, 69, 0.1)';
                    costUpdateInfo.style.color = '#dc3545';
                })
                .finally(() => {
                    setTimeout(() => refreshIcon.classList.remove('refreshing'), 1000);
                });
        }