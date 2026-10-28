<?php
/**
 * Converting Cart Progress Bar (Alippo Feature #10).
 * Displays real-time progress towards Free Shipping (Rs. 2,500 threshold).
 */

if (!defined('ABSPATH')) {
    exit;
}

class ShopRaven_Cart_Progress_Bar {

    const FREE_SHIPPING_THRESHOLD = 2500;

    public static function init() {
        add_action('woocommerce_before_cart_contents', array(__CLASS__, 'render_progress_bar'));
        add_action('woocommerce_widget_shopping_cart_before_buttons', array(__CLASS__, 'render_progress_bar'));
        add_filter('woocommerce_package_rates', array(__CLASS__, 'apply_free_shipping_above_threshold'), 10, 2);
    }

    public static function render_progress_bar() {
        if (!WC()->cart) return;

        $cart_total = WC()->cart->get_displayed_subtotal();
        $threshold = self::FREE_SHIPPING_THRESHOLD;
        $remaining = max(0, $threshold - $cart_total);
        $percent = min(100, round(($cart_total / $threshold) * 100));

        ?>
        <div class="shopraven-cart-progress-container" style="margin: 16px 0; padding: 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;">
            <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; color: #1e293b; margin-bottom: 8px;">
                <?php if ($remaining > 0): ?>
                    <span>Add <strong>Rs. <?php echo esc_html(number_format($remaining)); ?></strong> more to unlock <strong>FREE Delivery</strong>! (Save Rs. 150)</span>
                <?php else: ?>
                    <span style="color: #16a34a;">🎉 Congratulations! You have unlocked <strong>FREE Delivery</strong> across Pakistan!</span>
                <?php endif; ?>
                <span><?php echo esc_html($percent); ?>%</span>
            </div>
            <div style="width: 100%; height: 8px; background: #e2e8f0; border-radius: 9999px; overflow: hidden;">
                <div style="width: <?php echo esc_attr($percent); ?>%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981); transition: width 0.3s ease;"></div>
            </div>
        </div>
        <?php
    }

    public static function apply_free_shipping_above_threshold($rates, $package) {
        $cart_total = WC()->cart ? WC()->cart->get_displayed_subtotal() : 0;

        if ($cart_total >= self::FREE_SHIPPING_THRESHOLD) {
            foreach ($rates as $rate_id => $rate) {
                if ('flat_rate' === $rate->method_id) {
                    $rates[$rate_id]->cost = 0;
                    $rates[$rate_id]->label = 'Free Shipping (Over Rs. 2,500)';
                }
            }
        }

        return $rates;
    }
}

