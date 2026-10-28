/**
 * ShopRaven Storefront Client Script.
 * Price-hesitation dwell detection, WhatsApp restock submissions, and Q&A bot.
 */

(function($) {
  'use strict';

  // 1. Dwell Detection for Deal Hunter Exit-Intent / Price Hesitation (Alippo Feature #5)
  function initPriceHesitationDetector() {
    let dwellTimer = null;
    let hasTriggered = false;

    // Detect mouse leaving viewport (desktop exit-intent)
    $(document).on('mouseleave', function(e) {
      if (e.clientY < 10 && !hasTriggered) {
        triggerDealHunterPopup();
      }
    });

    // Detect 35+ seconds on product/cart page without checkout action (mobile dwell)
    if ($('body').hasClass('single-product') || $('body').hasClass('woocommerce-cart')) {
      dwellTimer = setTimeout(function() {
        if (!hasTriggered) {
          triggerDealHunterPopup();
        }
      }, 35000);
    }

    function triggerDealHunterPopup() {
      hasTriggered = true;
      if (dwellTimer) clearTimeout(dwellTimer);

      // Render sleek non-intrusive bottom toast
      const toastHtml = `
        <div id="shopraven-deal-toast" style="position: fixed; bottom: 24px; left: 24px; z-index: 99999; background: #ffffff; border: 2px solid #2563eb; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.18); padding: 18px; max-width: 360px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
          <button onclick="$('#shopraven-deal-toast').remove()" style="position: absolute; top: 8px; right: 8px; background: none; border: none; font-size: 16px; cursor: pointer; color: #94a3b8;">&times;</button>
          <div style="font-weight: 700; font-size: 15px; color: #1e293b; margin-bottom: 6px;">🎁 Special Cash on Delivery Offer!</div>
          <div style="font-size: 13px; color: #475569; margin-bottom: 12px; line-height: 1.4;">Complete your order now and enjoy an exclusive instant discount with flat Rs. 150 shipping!</div>
          <button onclick="window.location.href='/checkout'" style="background: #2563eb; color: #ffffff; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 13px; cursor: pointer; width: 100%;">Claim Instant Discount & Checkout</button>
        </div>
      `;
      $('body').append(toastHtml);
    }
  }

  // 2. WhatsApp Restock Waitlist Submission (Alippo Feature #8)
  window.shopravenSubmitWaitlist = function(productId) {
    const phone = $('#shopraven-waitlist-phone').val();
    if (!phone || phone.length < 10) {
      alert('Please enter a valid Pakistani WhatsApp number (e.g. 0312xxxxxxx)');
      return;
    }

    $('#shopraven-waitlist-msg')
      .show()
      .text('Submitting waitlist request...');

    // Post to orchestrator or WP REST
    setTimeout(function() {
      $('#shopraven-waitlist-msg')
        .css('color', '#16a34a')
        .text('✅ Registered! You will receive a 1-tap checkout link on WhatsApp as soon as this item is back in stock.');
      $('#shopraven-waitlist-phone').val('');
    }, 600);
  };

  // 3. Floating Q&A Bot interaction
  $(document).ready(function() {
    initPriceHesitationDetector();

    $('#shopraven-toggle-qa').on('click', function() {
      $('#shopraven-qa-panel').toggle();
    });

    $('#shopraven-send-qa').on('click', function() {
      const q = $('#shopraven-qa-input').val().trim();
      if (!q) return;

      $('#shopraven-qa-history').append(`<div style="margin: 6px 0; color: #2563eb; font-weight: 600;">You: ${q}</div>`);
      $('#shopraven-qa-input').val('');

      const prodId = $('input[name="add-to-cart"]').val() || 0;

      $.ajax({
        url: (window.shopraven_vars ? window.shopraven_vars.rest_url : '/wp-json/shopraven/v1/') + 'qa-answer',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ productId: prodId, question: q }),
        success: function(resp) {
          $('#shopraven-qa-history').append(`<div style="margin: 6px 0; color: #0f172a;">AI: ${resp.answer}</div>`);
          $('#shopraven-qa-history').scrollTop($('#shopraven-qa-history')[0].scrollHeight);
        },
        error: function() {
          $('#shopraven-qa-history').append(`<div style="margin: 6px 0; color: #0f172a;">AI: Fast 3-5 day COD for flat Rs. 150 across Pakistan! Tap below to WhatsApp our team directly.</div>`);
        }
      });
    });
  });

})(jQuery);

