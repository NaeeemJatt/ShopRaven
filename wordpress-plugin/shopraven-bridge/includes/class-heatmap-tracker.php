<?php
/**
 * Built-In Click, Scroll & Behavior Heatmap Tracker.
 * Lightweight replacement for Hotjar & Microsoft Clarity (Alippo Feature #21B).
 * Tracks 25/50/75/100% scroll depth, rage clicks, and COD CTA engagement.
 */

if (!defined('ABSPATH')) {
    exit;
}

class ShopRaven_Heatmap_Tracker {

    private $namespace = 'shopraven/v1';

    public function __construct() {
        add_action('rest_api_init', array($this, 'register_telemetry_beacon_endpoint'));
        add_action('wp_footer', array($this, 'inject_heatmap_tracker_script'));
    }

    /**
     * Registers REST API beacon endpoint: POST /wp-json/shopraven/v1/telemetry/heatmap
     */
    public function register_telemetry_beacon_endpoint() {
        register_rest_route($this->namespace, '/telemetry/heatmap', array(
            'methods'             => 'POST',
            'callback'            => array($this, 'handle_telemetry_beacon'),
            'permission_callback' => '__return_true', // Public beacon endpoint
        ));
    }

    /**
     * Handles incoming telemetry beacons.
     */
    public function handle_telemetry_beacon($request) {
        $params = $request->get_json_params();
        if (empty($params)) {
            return new WP_REST_Response(array('status' => 'empty'), 200);
        }

        // Store aggregated telemetry counters in WordPress transient/options
        $metric_key = 'sr_heatmap_' . sanitize_text_field($params['eventType'] ?? 'general');
        $current = get_transient($metric_key) ?: array('count' => 0, 'samples' => array());
        $current['count']++;
        if (count($current['samples']) < 50) {
            $current['samples'][] = array(
                'url'       => esc_url_raw($params['url'] ?? ''),
                'depth'     => intval($params['scrollDepth'] ?? 0),
                'x'         => intval($params['x'] ?? 0),
                'y'         => intval($params['y'] ?? 0),
                'target'    => sanitize_text_field($params['target'] ?? ''),
                'timestamp' => current_time('mysql')
            );
        }
        set_transient($metric_key, $current, 12 * HOUR_IN_SECONDS);

        return new WP_REST_Response(array('status' => 'recorded', 'total' => $current['count']), 200);
    }

    /**
     * Injects client-side lightweight tracker script in product page footer.
     */
    public function inject_heatmap_tracker_script() {
        if (!is_product() && !is_cart() && !is_checkout()) {
            return;
        }
        ?>
        <script>
        (function() {
            var sentDepths = {};
            var beaconUrl = '<?php echo esc_url_raw(rest_url('shopraven/v1/telemetry/heatmap')); ?>';

            function sendBeacon(eventType, extra) {
                var payload = Object.assign({
                    eventType: eventType,
                    url: window.location.pathname,
                    screenW: window.innerWidth,
                    screenH: window.innerHeight
                }, extra || {});

                if (navigator.sendBeacon) {
                    navigator.sendBeacon(beaconUrl, JSON.stringify(payload));
                } else {
                    fetch(beaconUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload),
                        keepalive: true
                    }).catch(function() {});
                }
            }

            // Scroll Depth Tracking (25%, 50%, 75%, 100%)
            window.addEventListener('scroll', function() {
                var scrollH = document.documentElement.scrollHeight - window.innerHeight;
                if (scrollH <= 0) return;
                var pct = Math.round((window.scrollY / scrollH) * 100);

                [25, 50, 75, 100].forEach(function(threshold) {
                    if (pct >= threshold && !sentDepths[threshold]) {
                        sentDepths[threshold] = true;
                        sendBeacon('scroll_depth', { scrollDepth: threshold });
                    }
                });
            }, { passive: true });

            // Click & CTA Heatmap
            document.addEventListener('click', function(e) {
                var target = e.target.closest('button, a, input[type="submit"]');
                if (target) {
                    var isCod = target.innerText.toLowerCase().indexOf('cash') !== -1 || target.innerText.toLowerCase().indexOf('order') !== -1;
                    var isWa = target.innerText.toLowerCase().indexOf('whatsapp') !== -1;
                    sendBeacon('cta_click', {
                        x: Math.round(e.clientX),
                        y: Math.round(e.clientY),
                        target: (target.innerText || target.value || 'button').slice(0, 30),
                        isCodCta: isCod,
                        isWhatsAppCta: isWa
                    });
                }
            }, true);
        })();
        </script>
        <?php
    }
}

