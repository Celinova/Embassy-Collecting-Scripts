// Add a new event listener for 'DOMContentLoaded'
document.addEventListener('DOMContentLoaded', function () {
    const targetUrl = 'https://www.nationstates.net/page=region_control/region=the_bottomless_pit';

    if (window.location.href === targetUrl) {
        window.close();
    }
});

document.addEventListener('keyup', function (event) {
    if (event.shiftKey || event.ctrlKey || event.altKey || document.activeElement.tagName == 'INPUT' || document.activeElement.tagName == 'TEXTAREA') {
        return;
    } else {
        switch (event.code) {
            case 'KeyR':
                if (window.location.href.includes("/region=") && !window.location.href.includes("page=region_admin")) {
                    window.location.assign(window.location.href.replace("/region=", "/page=region_admin/region="));
                } else if (window.location.href.includes("page=region_admin/region=")) {
                    // Click on the request embassies between my region and the target region button
                    document.getElementsByName('requestembassy')[0].click();
                }
                break;

            // ...other cases here...
        }
    }
});
