<?php
/**
 * Browser-Side Meta Pixel & Server CAPI Deduplication Bridge.
 * Part of ShopRaven Bridge for nnstore.shop (Alippo Feature #16B).
 */

if (!defined('ABSPATH')) {
    exit;
}

class ShopRaven_Meta_CAPI_Pixel {

    private $pixel_id;
    private $orchestrator_url;

    public function __construct() {
        $this->pixel_id = get_option('shopraven_meta_pixel_id', '123456789012345');
        $this->orchestrator_url = get_option('shopraven_orchestrator_url', 'http://shopraven-orchestrator:4000');

        // Hook into WP head for browser-side pixel
        add_action('wp_head', array($this, 'inject_pixel_head_script'));

        // Hook into WooCommerce purchase for server-side CAPI forwarding
        add_action('woocommerce_thankyou', array($this, 'forward_wc_purchase_to_capi'), 10, 1);
    }

    /**
     * Injects client-side Meta Pixel with dynamic event_id generator.
     */
    public function inject_pixel_head_script() {
        if (is_admin()) {
            return;
        }
        ?>
        <!-- ShopRaven Meta Pixel + CAPI Bridge -->
        <script>
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');

        fbq('init', '<?php echo esc_js($this->pixel_id); ?>');
        
        // Generate synchronized event_id for PageView
        window.shopRavenEventId = 'sr_pv_' + Date.now() + '_' + Math.floor(Math.random()*1000);
        fbq('track', 'PageView', {}, { eventID: window.shopRavenEventId });
        </script>
        <noscript>
            <img height="1" width="1" style="display:none"
                 src="https://www.facebook.com/tr?id=<?php echo esc_attr($this->pixel_id); ?>&ev=PageView&noscript=1"/>
        </noscript>
        <!-- End ShopRaven Meta Pixel -->
        <?php
    }

    /**
     * Forwards completed order to Node.js Orchestrator CAPI dispatcher for server-side recording.
     */
    public function forward_wc_purchase_to_capi($order_id) {
        if (!$order_id) {
            return;
        }

        $order = wc_get_order($order_id);
        if (!$order) {
            return;
        }

        // Shared deduplication key
        $event_id = 'order_' . $order_id;

        $payload = array(
            'eventName' => 'Purchase',
            'eventId'   => $event_id,
            'userData'  => array(
                'phone'     => $order->get_billing_phone(),
                'email'     => $order->get_billing_email(),
                'firstName' => $order->get_billing_first_name(),
                'lastName'  => $order->get_billing_last_name(),
                'city'      => $order->get_billing_city(),
                'ip'        => $order->get_customer_ip_address(),
                'userAgent' => $order->get_customer_user_agent()
            ),
            'customData' => array(
                'value'        => (float) $order->get_total(),
                'currency'     => $order->get_currency(),
                'order_id'     => $order_id,
                'shipping_fee' => (float) $order->get_shipping_total()
            )
        );

        // Async dispatch to Node.js orchestrator
        wp_remote_post($this->orchestrator_url . '/api/tracking/meta-capi', array(
            'method'      => 'POST',
            'timeout'     => 5,
            'redirection' => 5,
            'httpversion' => '1.0',
            'blocking'    => false,
            'headers'     => array('Content-Type' => 'application/json'),
            'body'        => wp_json_encode($payload)
        ));
    }
}

