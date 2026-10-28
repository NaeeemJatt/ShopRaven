<?php
/**
 * Prepaid Incentive & COD-to-Prepaid Split (Alippo Feature #11).
 * Displays top-bar banner and waives the Rs. 150 delivery fee when paying prepaid.
 */

if (!defined('ABSPATH')) {
    exit;
}

class ShopRaven_Prepaid_Incentive {

    public static function init() {
        add_action('wp_body_open', array(__CLASS__, 'render_top_bar_banner'));
        add_action('woocommerce_cart_calculate_fees', array(__CLASS__, 'apply_prepaid_shipping_waiver'), 20);
    }

    public static function render_top_bar_banner() {
        ?>
        <div id="shopraven-prepaid-banner" style="background: #0f172a; color: #ffffff; text-align: center; padding: 8px 12px; font-size: 13px; font-weight: 500;">
            <span>⚡ <strong>Save Rs. 150!</strong> Pay via <strong>Raast / EasyPaisa / JazzCash</strong> & get <strong>FREE SHIPPING</strong> nationwide! Flat Rs. 150 on COD.</span>
        </div>
        <?php
    }

    public static function apply_prepaid_shipping_waiver($cart) {
        if (is_admin() && !defined('DOING_AJAX')) return;

        // Check selected payment gateway
        $chosen_payment = WC()->session ? WC()->session->get('chosen_payment_method') : '';

        // If paying via direct bank transfer / Raast / EasyPaisa, provide Rs. 150 discount to offset shipping
        $prepaid_gateways = array('bacs', 'easypaisa', 'jazzcash', 'raast');
        if (in_array($chosen_payment, $prepaid_gateways)) {
            $discount_amount = -150;
            $cart->add_fee(__('Prepaid Incentive (Shipping Waived)', 'shopraven-bridge'), $discount_amount, false);
        }
    }
}

