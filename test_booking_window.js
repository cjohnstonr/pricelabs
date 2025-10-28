const playwright = require('playwright');

(async () => {
    const browser = await playwright.chromium.launch();
    const context = await browser.newContext({
        viewport: { width: 1400, height: 900 }
    });
    const page = await context.newPage();

    // Capture console messages
    page.on('console', msg => {
        console.log('[BROWSER]', msg.type(), msg.text());
    });

    // Capture errors
    page.on('pageerror', error => {
        console.error('[PAGE ERROR]', error.message);
    });

    try {
        console.log('Navigating to page...');
        await page.goto('http://localhost:5050/listingv5.html?listing_id=676dc2687292010012976878', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });

        console.log('Waiting for dashboard to load...');
        await page.waitForSelector('#dashboard', { state: 'visible', timeout: 60000 });

        console.log('Waiting for pricing table...');
        await page.waitForSelector('#pricing-table-body tr', { timeout: 30000 });

        console.log('Taking screenshot...');
        await page.screenshot({ path: 'test_booking_window_full.png', fullPage: true });

        console.log('Success! Screenshot saved as test_booking_window_full.png');
    } catch (error) {
        console.error('Error:', error.message);
        await page.screenshot({ path: 'test_booking_window_error.png', fullPage: true });
    } finally {
        await browser.close();
    }
})();
