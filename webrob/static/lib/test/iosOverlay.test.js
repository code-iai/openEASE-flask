const iosOverlay = require('../pageOverlay');
const client = require('../client_tmp');

let KNOWROB_CLIENT;

// normally this is an html-container of the DOM
const CORRECT_PAGE_OVERLAY = '<div id="page-overlay" class="ios-overlay ios-overlay-hide div-overlay" style="display: none">\n'
    + '    <span class="title">Please select an Episode</span>\n'
    + '</div>';
const EMPTY_PAGE_OVERLAY = undefined;

// TODO: When Knowrob.init is implemented correctly, setup has to be mocked to save time
beforeEach(() => {
    KNOWROB_CLIENT = new client.KnowrobClient({});

    setupTestDOM();
});

function setupTestDOM() {
    const page = document.createElement('div');
    document.body.appendChild(page);
}

afterEach(() => {
    tearDownTestDOM();
});

function tearDownTestDOM() {
    document.body.innerHTML = '';
}

function isDiv(container) {
    return container instanceof HTMLDivElement;
}

test('createIOSPageOverlay', () => {

});

test('createOverlayDiv', () => {
    const overlayDiv = iosOverlay.createOverlayDiv();

    expect(overlayDiv).toBeTruthy();
    expect(isDiv(overlayDiv)).toBe(true);
    expect(overlayDiv.id).toBe('page-overlay');
});

test('isPageOverlayEnabled', () => {
    KNOWROB_CLIENT.setPageOverlayEnabled(false);
    expect(KNOWROB_CLIENT.isOverlayEnabled(EMPTY_PAGE_OVERLAY)).toBeFalsy();
    expect(KNOWROB_CLIENT.isOverlayEnabled(CORRECT_PAGE_OVERLAY)).toBeFalsy();

    KNOWROB_CLIENT.setPageOverlayEnabled(true);
    expect(KNOWROB_CLIENT.isOverlayEnabled(EMPTY_PAGE_OVERLAY)).toBeFalsy();
    expect(KNOWROB_CLIENT.isOverlayEnabled(CORRECT_PAGE_OVERLAY)).toBe(true);
});

test('isPageOverlayDisabled', () => {
    KNOWROB_CLIENT.setPageOverlayEnabled(false);
    expect(KNOWROB_CLIENT.isOverlayDisabled(EMPTY_PAGE_OVERLAY)).toBeFalsy();
    expect(KNOWROB_CLIENT.isOverlayDisabled(CORRECT_PAGE_OVERLAY)).toBe(true);

    KNOWROB_CLIENT.setPageOverlayEnabled(true);
    expect(KNOWROB_CLIENT.isOverlayDisabled(EMPTY_PAGE_OVERLAY)).toBeFalsy();
    expect(KNOWROB_CLIENT.isOverlayDisabled(CORRECT_PAGE_OVERLAY)).toBeFalsy();
});

test('showPageOverlay', () => {

});

test('hidePageOverlay', () => {

});

test('setOverlayClassToShow', () => {

});

test('setOverlayClassToHide', () => {

});
