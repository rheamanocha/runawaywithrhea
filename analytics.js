/* Google Analytics 4 for runawaywithrhea.com.
   Set GA_ID to the Measurement ID (looks like G-XXXXXXXXXX) from
   GA4 > Admin > Data streams > your web stream. Until it is set, this file does nothing. */
(function () {
  var GA_ID = 'G-MLG85954FP';

  if (!/^G-[A-Z0-9]{6,}$/.test(GA_ID) || GA_ID === 'G-XXXXXXXXXX') { return; }

  // Stay quiet while previewing locally or on a non-production host.
  var host = location.hostname;
  if (host !== 'runawaywithrhea.com' && host !== 'www.runawaywithrhea.com') { return; }

  // Respect Do Not Track / Global Privacy Control.
  if (navigator.doNotTrack === '1' || navigator.globalPrivacyControl) { return; }

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag('js', new Date());
  gtag('config', GA_ID);

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
  document.head.appendChild(s);
})();
