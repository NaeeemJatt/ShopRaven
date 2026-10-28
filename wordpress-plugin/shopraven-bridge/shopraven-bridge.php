<?php
/**
 * Plugin Name: ShopRaven Bridge for nnstore.shop
 * Plugin URI: https://nnstore.shop
 * Description: Autonomous Conversion Booster, Roman-Urdu Search Expansion, Cart Progress Bar, WhatsApp Restock Waitlists & 24/7 AI Product Assistant.
 * Version: 1.0.0
 * Author: Naeem Ashiq (ShopRaven AI)
 * Author URI: https://nnstore.shop
 * Text Domain: shopraven-bridge
 * Requires at least: 6.0
 * Requires PHP: 7.4
 * WC requires at least: 8.0
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

define('SHOPRAVEN_VERSION', '1.0.0');
define('SHOPRAVEN_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('SHOPRAVEN_PLUGIN_URL', plugin_dir_url(__FILE__));

// Require module components
require_once SHOPRAVEN_PLUGIN_DIR . 'includes/class-cart-progress-bar.php';
require_once SHOPRAVEN_PLUGIN_DIR . 'includes/class-prepaid-incentive.php';
require_once SHOPRAVEN_PLUGIN_DIR . 'includes/class-product-qa-bot.php';
require_once SHOPRAVEN_PLUGIN_DIR . 'includes/class-meta-capi-pixel.php';
require_once SHOPRAVEN_PLUGIN_DIR . 'includes/class-speed-optimizer.php';
require_once SHOPRAVEN_PLUGIN_DIR . 'includes/class-heatmap-tracker.php';

class ShopRavenBridge {
    private static $instance = null;

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        // Enqueue storefront assets
        add_action('wp_enqueue_scripts', array($this, 'enqueue_storefront_assets'));

        // Initialize features
        ShopRaven_Cart_Progress_Bar::init();
        ShopRaven_Prepaid_Incentive::init();
        ShopRaven_Product_QA_Bot::init();

        // Alippo Extended Growth Suite: CAPI, Speed Optimizer & Heatmap Tracker
        new ShopRaven_Meta_CAPI_Pixel();
        new ShopRaven_Speed_Optimizer();
        new ShopRaven_Heatmap_Tracker();

        // Alippo Feature #4: Roman-Urdu Search Expansion
        add_filter('posts_search', array($this, 'expand_roman_urdu_search_queries'), 20, 2);

        // Alippo Feature #8: Out-of-Stock WhatsApp waitlist capture form
        add_action('woocommerce_single_product_summary', array($this, 'render_out_of_stock_waitlist_form'), 35);

        // Social OpenGraph & WhatsApp Rich Preview Meta for viral social sharing
        add_action('wp_head', array($this, 'render_social_opengraph_meta'), 5);

        // Structured JSON-LD & Crawl Budget Protection in <head>
        add_action('wp_head', array($this, 'render_shopraven_head_seo'), 2);
    }

    public function enqueue_storefront_assets() {
        wp_enqueue_script(
            'shopraven-storefront',
            SHOPRAVEN_PLUGIN_URL . 'assets/shopraven-storefront.js',
            array('jquery'),
            SHOPRAVEN_VERSION,
            true
        );

        wp_localize_script('shopraven-storefront', 'shopraven_vars', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'rest_url' => esc_url_raw(rest_url('shopraven/v1/')),
            'free_shipping_threshold' => 2500,
            'flat_shipping_rate' => 150,
            'whatsapp_number' => '+923114618934'
        ));
    }

    /**
     * Injects OpenGraph & Twitter Card meta for high-converting WhatsApp link previews.
     */
    public function render_social_opengraph_meta() {
        if (function_exists('is_product') && is_product()) {
            global $product;
            if (!$product) return;
            $title = esc_attr($product->get_name());
            $price = esc_attr($product->get_price());
            $desc = wp_strip_all_tags($product->get_short_description() ?: $product->get_description());
            $desc = esc_attr(mb_substr($desc, 0, 150));
            $image_id = $product->get_image_id();
            $img_url = $image_id ? esc_url(wp_get_attachment_image_url($image_id, 'full')) : '';

            echo "\n<!-- ShopRaven OpenGraph Meta for WhatsApp Previews & Google -->\n";
            echo '<meta property="og:site_name" content="nnstore.shop" />' . "\n";
            echo '<meta property="og:type" content="product" />' . "\n";
            echo '<meta property="og:title" content="' . $title . ' - Rs. ' . number_format((float)$price) . ' | nnstore.shop" />' . "\n";
            echo '<meta property="og:description" content="' . $desc . ' | Flat Rs. 150 COD Nationwide" />' . "\n";
            if ($img_url) {
                echo '<meta property="og:image" content="' . $img_url . '" />' . "\n";
            }
            echo '<meta property="product:price:amount" content="' . $price . '" />' . "\n";
            echo '<meta property="product:price:currency" content="PKR" />' . "\n";
            echo '<meta name="twitter:card" content="summary_large_image" />' . "\n";
            echo "<!-- /ShopRaven OpenGraph Meta -->\n";
        }
    }

    /**
     * Renders Structured Data JSON-LD, Canonical URLs, and Crawl Budget Protection.
     */
    public function render_shopraven_head_seo() {
        // 1. Crawl budget preservation: Noindex thin search and checkout pages
        if (is_search() || (function_exists('is_cart') && is_cart()) || (function_exists('is_checkout') && is_checkout()) || (function_exists('is_account_page') && is_account_page())) {
            echo "\n<!-- ShopRaven Crawl Budget Protection -->\n";
            echo '<meta name="robots" content="noindex, follow" />' . "\n";
            return;
        }

        // 2. Product Structured Data & Canonical Tag
        if (function_exists('is_product') && is_product()) {
            global $product;
            if (!$product) return;
            $product_id = $product->get_id();

            // Self-referencing Canonical URL
            echo "\n<!-- ShopRaven Canonical & Schema Head Injection -->\n";
            echo '<link rel="canonical" href="' . esc_url(get_permalink($product_id)) . '" />' . "\n";

            // Output JSON-LD Schema from product meta (immune to wp_kses_post content stripping)
            $schema_json = get_post_meta($product_id, '_shopraven_json_ld_schema', true);
            if (!empty($schema_json)) {
                echo '<script type="application/ld+json">' . "\n" . $schema_json . "\n" . '</script>' . "\n";
            }
        }
    }

    /**
     * Roman-Urdu search query expansion filter.
     * Matches user search query against _shopraven_search_synonyms meta key.
     */
    public function expand_roman_urdu_search_queries($search, $wp_query) {
        global $wpdb;
        if (!is_admin() && $wp_query->is_main_query() && $wp_query->is_search()) {
            $query_term = $wp_query->get('s');
            if (!empty($query_term)) {
                $term = '%' . $wpdb->esc_like(sanitize_text_field($query_term)) . '%';
                $search .= " OR EXISTS (
                    SELECT 1 FROM {$wpdb->postmeta} 
                    WHERE {$wpdb->postmeta}.post_id = {$wpdb->posts}.ID 
                    AND {$wpdb->postmeta}.meta_key = '_shopraven_search_synonyms' 
                    AND {$wpdb->postmeta}.meta_value LIKE '{$term}'
                )";
            }
        }
        return $search;
    }

    /**
     * Renders WhatsApp Restock Waitlist widget if product is Out-of-Stock.
     */
    public function render_out_of_stock_waitlist_form() {
        global $product;
        if ($product && !$product->is_in_stock()) {
            $product_id = $product->get_id();
            ?>
            <div class="shopraven-waitlist-box" style="margin: 20px 0; padding: 16px; border: 2px dashed #22c55e; border-radius: 8px; background: #f0fdf4;">
                <h4 style="margin: 0 0 8px 0; color: #166534; font-size: 15px;">🔔 Back in Stock Alert on WhatsApp</h4>
                <p style="margin: 0 0 12px 0; font-size: 13px; color: #374151;">This item is currently sold out. Enter your WhatsApp number to receive an instant 1-tap checkout link when it is restocked:</p>
                <div style="display: flex; gap: 8px;">
                    <input type="tel" id="shopraven-waitlist-phone" placeholder="0312xxxxxxx" style="flex: 1; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px;" />
                    <button type="button" onclick="window.shopravenSubmitWaitlist(<?php echo esc_attr($product_id); ?>)" style="background: #22c55e; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer;">
                        Notify Me
                    </button>
                </div>
                <div id="shopraven-waitlist-msg" style="display: none; margin-top: 8px; font-size: 12px; color: #166534;"></div>
            </div>
            <?php
        }
    }
}

add_action('plugins_loaded', array('ShopRavenBridge', 'get_instance'));

