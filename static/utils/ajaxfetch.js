document.addEventListener("DOMContentLoaded", function () {
        let currentContent = document.documentElement.outerHTML;
    
    function extractMainContent(htmlString) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlString, "text/html");
        const mainContent = doc.querySelector("form") ;
        return mainContent ? mainContent.innerHTML : "";
    }
    
    function checkForUpdates() {
        fetch(window.location.href, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            },
            cache: "no-store"
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            const fetchedMainContent = extractMainContent(html);
            const currentMainContent = extractMainContent(currentContent);
            
            if (fetchedMainContent !== currentMainContent) {
                updateDynamicElements(html);
                console.log(html);
                currentContent = html;
            }
        })
        .catch(error => {
            console.error("Error checking for updates:", error);
            window.href.reload();
        });
    }
    
    function updateDynamicElements(html) {
        const parser = new DOMParser();
        const newDoc = parser.parseFromString(html, "text/html");
        
        updateElement("form", newDoc);
        reinitializeScripts();
    }
    
    function updateElement(selector, newDoc) {
        const currentElement = document.querySelector(selector);
        const newElement = newDoc.querySelector(selector);
        
        if (currentElement && newElement && currentElement.innerHTML !== newElement.innerHTML) {
            currentElement.innerHTML = newElement.innerHTML;
        }
    }
    
    function reinitializeScripts() {
        const event = new Event('contentUpdated');
        document.dispatchEvent(event);
    }

 
    setInterval(checkForUpdates, 10000);

    checkForUpdates();
});