<?php
/**
 * 24/7 On-Page Product Q&A Bot (Alippo Feature #13).
 * Floating AI assistant on single product pages answering buyer questions instantly.
 */

if (!defined('ABSPATH')) {
    exit;
}

class ShopRaven_Product_QA_Bot {

    public static function init() {
        add_action('wp_footer', array(__CLASS__, 'render_product_assistant_widget'));
        add_action('rest_api_init', array(__CLASS__, 'register_rest_qa_endpoint'));
    }

    public static function register_rest_qa_endpoint() {
        register_rest_route('shopraven/v1', '/qa-answer', array(
            'methods' => 'POST',
            'callback' => array(__CLASS__, 'handle_qa_query'),
            'permission_callback' => '__return_true',
        ));
    }

    public static function handle_qa_query($request) {
        $params = $request->get_json_params();
        $product_id = isset($params['productId']) ? intval($params['productId']) : 0;
        $question = isset($params['question']) ? sanitize_text_field($params['question']) : '';

        $product = wc_get_product($product_id);
        $title = $product ? $product->get_name() : 'This item';
        $price = $product ? $product->get_price() : '0';

        $q_lower = strtolower($question);

        if (strpos($q_lower, 'delivery') !== false || strpos($q_lower, 'shipping') !== false || strpos($q_lower, 'kahan') !== false) {
            $answer = "We deliver nationwide across Pakistan in 3-5 business days. Delivery is a flat Rs. 150 for Cash-on-Delivery, or completely FREE if you order above Rs. 2,500!";
        } elseif (strpos($q_lower, 'price') !== false || strpos($q_lower, 'kitne') !== false) {
            $answer = "The price of {$title} is Rs. " . number_format($price) . " on nnstore.shop with Cash-on-Delivery.";
        } elseif (strpos($q_lower, 'original') !== false || strpos($q_lower, 'warranty') !== false || strpos($q_lower, 'guarantee') !== false) {
            $answer = "Yes! All products at nnstore.shop are factory-checked with a 7-day checking warranty. You pay upon delivery.";
        } else {
            $answer = "Great question! {$title} is in stock with 3-5 day COD. For custom inquiries, tap the WhatsApp button below to speak directly with our team.";
        }

        return rest_ensure_response(array(
            'answer' => $answer,
            'whatsapp_link' => 'https://wa.me/923124999196?text=' . rawurlencode("Hi nnstore.shop! I have a question about {$title}: {$question}")
        ));
    }

    public static function render_product_assistant_widget() {
        if (!is_product()) return;

        global $product;
        $product_id = $product ? $product->get_id() : 0;
        ?>
        <div id="shopraven-qa-bubble" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
            <button id="shopraven-toggle-qa" style="background: #2563eb; color: #fff; border: none; width: 56px; height: 56px; border-radius: 50%; box-shadow: 0 4px 12px rgba(37,99,235,0.4); cursor: pointer; font-size: 24px; display: flex; align-items: center; justify-content: center;">
                💬
            </button>
            <div id="shopraven-qa-panel" style="display: none; position: absolute; bottom: 70px; right: 0; width: 320px; background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); padding: 16px; font-family: sans-serif;">
                <div style="font-weight: 700; font-size: 14px; margin-bottom: 8px; color: #0f172a;">ShopRaven AI Assistant (nnstore.shop)</div>
                <div style="font-size: 12px; color: #64748b; margin-bottom: 12px;">Instant answers on delivery, pricing, and specs:</div>
                <div id="shopraven-qa-history" style="max-height: 140px; overflow-y: auto; font-size: 13px; margin-bottom: 12px; line-height: 1.4;">
                    <p style="margin: 0; color: #334155;">👋 Ask me anything about this product or nationwide delivery!</p>
                </div>
                <div style="display: flex; gap: 6px;">
                    <input type="text" id="shopraven-qa-input" placeholder="Ask a question..." style="flex: 1; padding: 6px 10px; font-size: 13px; border: 1px solid #cbd5e1; border-radius: 6px;" />
                    <button type="button" id="shopraven-send-qa" style="background: #2563eb; color: #fff; border: none; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer;">Send</button>
                </div>
                <div style="margin-top: 10px; text-align: center;">
                    <a href="https://wa.me/923124999196" target="_blank" style="font-size: 11px; color: #16a34a; text-decoration: none; font-weight: 600;">
                        📱 WhatsApp Human Support (+92 312 4999196)
                    </a>
                </div>
            </div>
        </div>
        <?php
    }
}

