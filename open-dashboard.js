const { chromium } = require('playwright');

async function openDashboard() {
  console.log('🚀 Launching PriceLabs Dashboard...\n');

  // Launch browser in headed mode (visible window)
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100 // Slight delay for visibility
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });

  const page = await context.newPage();

  console.log('📡 Navigating to dashboard...');
  await page.goto('http://localhost:5050/listingv5.html?listing_id=676dc2687292010012976878');

  console.log('⏳ Waiting for dashboard to load...');
  // Wait for the pricing table to have data
  await page.waitForSelector('#pricing-table-body', { timeout: 10000 });
  await page.waitForFunction(() => {
    const tbody = document.querySelector('#pricing-table-body');
    return tbody && tbody.querySelectorAll('tr').length > 0;
  }, { timeout: 15000 });

  console.log('✅ Dashboard loaded successfully!\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('🎯 TESTING INSTRUCTIONS:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
  console.log('📊 Booking Window Risk Feature:');
  console.log('   • Look for the PURPLE column titled "Booking Window"');
  console.log('   • It appears after the "vs Top End" column');
  console.log('   • Shows green risk badges (LOW, MEDIUM, HIGH, VERY HIGH)');
  console.log('');
  console.log('🖱️  Interactive Testing:');
  console.log('   • HOVER over any green badge to see tooltips');
  console.log('   • Tooltips display booking window details (e.g., "60+ days")');
  console.log('   • Test multiple rows to see different risk levels');
  console.log('');
  console.log('🎨 Visual Checks:');
  console.log('   • Purple header background for "Booking Window" column');
  console.log('   • Consistent badge styling across rows');
  console.log('   • Smooth tooltip appearance on hover');
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('⌨️  Press Ctrl+C in this terminal to close the browser');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  // Keep the browser open until user interrupts
  await new Promise((resolve) => {
    process.on('SIGINT', async () => {
      console.log('\n\n🛑 Closing browser...');
      await browser.close();
      console.log('✅ Browser closed. Goodbye!');
      process.exit(0);
    });
  });
}

// Error handling
openDashboard().catch(async (error) => {
  console.error('❌ Error opening dashboard:', error.message);
  console.error('\n💡 Troubleshooting:');
  console.error('   1. Make sure the Flask server is running on port 5050');
  console.error('   2. Check that listingv5.html exists and is accessible');
  console.error('   3. Verify the listing_id is valid');
  console.error('   4. Ensure Playwright is installed: npm install playwright');
  process.exit(1);
});
