// Wrapping the entire code within an IIFE to avoid polluting the global scope.
(() => {
  // Wait for the DOM content to load before executing JavaScript
  document.addEventListener('DOMContentLoaded', init);

  // Function to initialise the scripts
  function init() {
    // Identify button
    const button = document.querySelector('.btn');
    // Add event listeners directly without check
    button.addEventListener('click', bindButtonClickEvent);
    button.addEventListener('touchstart', bindTouchEvent, { passive: false });

    // Attach scroll event to body
    document.querySelector('body').addEventListener('wheel', bindScrollEvent, { passive: true });
}

  // Handler for click event
  const bindButtonClickEvent = () => {
    alert('Welcome and thank you for trying register in my platform 🤩');
  }

  // Handler for touchstart event
  const bindTouchEvent = (e) => {
    e.preventDefault();
    console.log('Touch started!');
  }

  // Handler for wheel(scroll) event
  const bindScrollEvent = () => {
    console.log('Scrolled!');
  }

  // Handler for pagehide event
  const pagehideHandler = () => {
    console.log('User navigate away from the page!');
  }
 
  // Always good to have a pagehide event listener 
  window.addEventListener('pagehide', () => {
    chrome.runtime.onMessage.removeListener(handleExtensionEvents);
  });
})();