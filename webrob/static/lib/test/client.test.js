const client = require('../client');

test('isPageOverlayDisabled', () => {
    const knowrobClient = new client();

    const correctPageOverlay = 'this is not empty';    // normally this is an html-container of the DOM
    const emptyPageOverlay = undefined;

    expect(knowrobClient.isPageOverlayDisabled(emptyPageOverlay, isDisabled = true)).toBe(false);
    expect(knowrobClient.isPageOverlayDisabled(emptyPageOverlay, isDisabled = false)).toBe(false);

    expect(knowrobClient.isPageOverlayDisabled(correctPageOverlay, isDisabled = true)).toBe();
    expect(knowrobClient.isPageOverlayDisabled(correctPageOverlay, isDisabled = false)).toBe();
});
