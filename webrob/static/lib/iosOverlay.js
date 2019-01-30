// TODO

function createIOSPageOverlay() {
    const page = this.getPageContainer();

    if (page) {
        const pageOverlay = this.createOverlayDiv();
        page.appendChild(pageOverlay);
        const spinner = createSpinner();
        pageOverlay.appendChild(spinner.el);
    }
}

function getPageContainer() {
    return document.getElementById('page');
}

function createOverlayDiv() {
    const pageOverlay = document.createElement('div');

    pageOverlay.setAttribute('id', 'page-overlay');
    pageOverlay.className = 'ios-overlay ios-overlay-hide div-overlay';
    pageOverlay.innerHTML += '<span class="title">Please select an Episode</span>';
    pageOverlay.style.display = 'none';

    return pageOverlay;
}

function showPageOverlay(text) {
    const pageOverlay = this.getPageOverlayDivFromDoc();
    if (this.isOverlayDisabled(pageOverlay)) {
        this.setOverlayClassToShow(pageOverlay, text);
        this.setPageOverlayEnabled(true);
    }
}

function getPageOverlayDivFromDoc() {
    return document.getElementById('page-overlay');
}

function isOverlayDisabled(pageOverlay) {
    return pageOverlay && !this.getPageOverlayEnabled();
}

function getPageOverlayEnabled() {
    return this.that.pageOverlayEnabled;
}

function setPageOverlayEnabled(setEnabled) {
    this.that.pageOverlayEnabled = setEnabled;
}

function setOverlayClassToShow(pageOverlay, text) {
    pageOverlay.children[0].innerHTML = text;
    pageOverlay.style.display = 'block';
    pageOverlay.className = pageOverlay.className.replace('hide', 'show');
    pageOverlay.style.pointerEvents = 'auto';
}

function hidePageOverlay() {
    const pageOverlay = this.getPageOverlayDivFromDoc();
    if (this.isOverlayEnabled(pageOverlay)) {
        this.setOverlayClassToHide(pageOverlay);
        this.setPageOverlayEnabled(false);
    }
}

function isOverlayEnabled(pageOverlay) {
    return pageOverlay && this.getPageOverlayEnabled();
}

function setOverlayClassToHide(pageOverlay) {
    // pageOverlay.style.display = 'none';
    pageOverlay.className = pageOverlay.className.replace('show', 'hide');
    pageOverlay.style.pointerEvents = 'none';
}
