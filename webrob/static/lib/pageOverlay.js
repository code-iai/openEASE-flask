// TODO: See whether this has to stay global or can just be an import
const spinner = require('./spinner');

// TODO: replace in method alteration of parameters with returning a new object
class pageOverlay {
    constructor() {
        this.pageOverlayEnabled = false;
    }

    getPageOverlayEnabled() {
        return this.pageOverlayEnabled;
    }

    setPageOverlayEnabled(setEnabled) {
        this.pageOverlayEnabled = setEnabled;
    }

    createIOSPageOverlay() {
        const page = this.getPageContainer();

        if (page) {
            const pageOverlay = pageOverlay.createOverlayDiv();
            page.appendChild(pageOverlay);
            const spinner = createSpinner();
            pageOverlay.appendChild(spinner.el);
        }
    }

    static getPageContainer() {
        return document.getElementById('page');
    }

    static createOverlayDiv() {
        const pageOverlay = document.createElement('div');

        pageOverlay.setAttribute('id', 'page-overlay');
        pageOverlay.className = 'ios-overlay ios-overlay-hide div-overlay';
        pageOverlay.innerHTML += '<span class="title">Please select an Episode</span>';
        pageOverlay.style.display = 'none';

        return pageOverlay;
    }

    showPageOverlay(text) {
        let pageOverlay = this.getPageOverlayDivFromDoc();
        if (this.isOverlayDisabled(pageOverlay)) {
            pageOverlay = this.setOverlayClassToShow(pageOverlay, text);
            this.setPageOverlayEnabled(true);
        }
    }

    static getPageOverlayDivFromDoc() {
        return document.getElementById('page-overlay');
    }

    isOverlayDisabled(pageOverlay) {
        return pageOverlay && !this.getPageOverlayEnabled();
    }

    setOverlayClassToShow(pageOverlay, text) {
        pageOverlay.children[0].innerHTML = text;
        pageOverlay.style.display = 'block';
        pageOverlay.className = pageOverlay.className.replace('hide', 'show');
        pageOverlay.style.pointerEvents = 'auto';
    }

    hidePageOverlay() {
        const pageOverlay = this.getPageOverlayDivFromDoc();
        if (this.isOverlayEnabled(pageOverlay)) {
            this.setOverlayClassToHide(pageOverlay);
            this.setPageOverlayEnabled(false);
        }
    }

    isOverlayEnabled(pageOverlay) {
        return pageOverlay && this.getPageOverlayEnabled();
    }

    setOverlayClassToHide(pageOverlay) {
        // pageOverlay.style.display = 'none';
        pageOverlay.className = pageOverlay.className.replace('show', 'hide');
        pageOverlay.style.pointerEvents = 'none';
    }
}

module.exports = pageOverlay;
