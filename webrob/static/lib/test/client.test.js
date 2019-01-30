const client = require('../client_tmp');

test('isPageOverlayEnabled', () => {
    const knowrobClient = new client.KnowrobClient({});

    const correctPageOverlay = 'this is not empty';    // normally this is an html-container of the DOM
    const emptyPageOverlay = undefined;

    knowrobClient.that.pageOverlayEnabled = false;
    expect(knowrobClient.isOverlayEnabled(emptyPageOverlay)).toBeFalsy();
    expect(knowrobClient.isOverlayEnabled(correctPageOverlay)).toBeFalsy();

    knowrobClient.that.pageOverlayEnabled = true;
    expect(knowrobClient.isOverlayEnabled(emptyPageOverlay)).toBeFalsy();
    expect(knowrobClient.isOverlayEnabled(correctPageOverlay)).toBe(true);
});

test('isPageOverlayDisabled', () => {
    const knowrobClient = new client.KnowrobClient({});

    const correctPageOverlay = 'this is not empty';    // normally this is an html-container of the DOM
    const emptyPageOverlay = undefined;

    knowrobClient.that.pageOverlayEnabled = false;
    expect(knowrobClient.isOverlayDisabled(emptyPageOverlay)).toBeFalsy();
    expect(knowrobClient.isOverlayDisabled(correctPageOverlay)).toBe(true);

    knowrobClient.that.pageOverlayEnabled = true;
    expect(knowrobClient.isOverlayDisabled(emptyPageOverlay)).toBeFalsy();
    expect(knowrobClient.isOverlayDisabled(correctPageOverlay)).toBeFalsy();
});
