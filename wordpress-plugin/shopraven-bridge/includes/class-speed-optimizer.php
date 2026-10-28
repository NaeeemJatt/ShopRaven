<?php
/**
 * Built-In Website Speed Optimizer.
 * Replaces bulky speed plugins (Avada/WP Rocket) with lightweight native hooks.
 * Part of ShopRaven Bridge for nnstore.shop (Alippo Feature #21A).
 */

if (!defined('ABSPATH')) {
    exit;
}

class ShopRaven_Speed_Optimizer {

    public function __construct() {
        // Optimize LCP on product images
        add_filter('wp_get_attachment_image_attributes', array($this, 'optimize_lcp_product_images'), 10, 2);

        // Defer non-critical scripts
        add_filter('script_loader_tag', array($this, 'defer_non_critical_assets'), 10, 2);

        // Add preconnect headers for Google Fonts & CDN
        add_action('wp_head', array($this, 'add_performance_hints'), 1);
    }

    /**
     * Prioritizes Largest Contentful Paint (LCP) hero product image.
     */
    public function optimize_lcp_product_images($attr, $attachment) {
        if (is_product()) {
            global $product;
            if ($product && $attachment->ID === $product->get_image_id()) {
                // Ensure hero image loads instantly with high priority
                $attr['fetchpriority'] = 'high';
                $attr['decoding'] = 'async';
                unset($attr['loading']); // Remove lazy load on primary LCP image
            } else {
                $attr['loading'] = 'lazy';
                $attr['decoding'] = 'async';
            }
        }
        return $attr;
    }

    /**
     * Defers render-blocking scripts while preserving essential jQuery/cart hooks.
     */
    public function defer_non_critical_assets($tag, $handle) {
        if (is_admin()) {
            return $tag;
        }

        // Exclude critical scripts
        $critical = array('jquery', 'jquery-core', 'woocommerce', 'wc-cart-fragments');
        if (in_array($handle, $critical, true)) {
            return $tag;
        }

        // Add defer attribute if not already present
        if (strpos($tag, 'defer') === false && strpos($tag, 'async') === false) {
            return str_replace('<script ', '<script defer ', $tag);
        }

        return $tag;
    }

    /**
     * Injects DNS-prefetch and preconnect headers for third-party CDNs.
     */
    public function add_performance_hints() {
        echo '<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>' . "\n";
        echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
        echo '<link rel="dns-prefetch" href="https://connect.facebook.net">' . "\n";
        echo '<link rel="dns-prefetch" href="https://images.pexels.com">' . "\n";
    }
}

