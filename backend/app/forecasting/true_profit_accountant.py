"""
True Net Profit & Hidden Cost Accountant (Alippo Feature #2).
Calculates real take-home profit taking into account HHC/Oshi wholesale costs,
courier dispatch charges, flyer packaging, and COD RTO return penalties.
"""

from typing import Dict, Any, List
from app.config import get_settings

settings = get_settings()

FLYER_PACKAGING_COST_PKR = 35.0
COURIER_DISPATCH_FEE_PKR = 150.0
COURIER_RTO_RETURN_PENALTY_PKR = 180.0  # Courier return penalty when parcel is rejected


class TrueProfitAccountant:
    """Calculates granular realized net profit per order and aggregated period PnL statements."""

    def compute_order_net_profit(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes exact realized profit for a single order.
        Status: 'delivered', 'rto', 'in_transit', 'cancelled'
        """
        status = order.get("status", "delivered").lower()
        sale_price = float(order.get("sale_price_pkr", 0.0))
        shipping_collected = float(order.get("shipping_fee_collected", settings.DEFAULT_DELIVERY_FEE_PKR))
        wholesale_cost = float(order.get("wholesale_cost_pkr", 0.0))
        packaging_cost = float(order.get("packaging_cost_pkr", FLYER_PACKAGING_COST_PKR))

        if status == "delivered":
            gross_revenue = sale_price + shipping_collected
            total_expenses = wholesale_cost + COURIER_DISPATCH_FEE_PKR + packaging_cost
            net_profit = gross_revenue - total_expenses
            profit_margin_pct = (net_profit / sale_price) * 100.0 if sale_price > 0 else 0.0

            return {
                "order_id": order.get("order_id"),
                "status": "delivered",
                "gross_revenue": gross_revenue,
                "wholesale_cost": wholesale_cost,
                "courier_paid": COURIER_DISPATCH_FEE_PKR,
                "packaging_cost": packaging_cost,
                "rto_loss": 0.0,
                "net_profit": round(net_profit, 2),
                "profit_margin_pct": round(profit_margin_pct, 2),
                "is_profitable": net_profit > 0,
            }

        elif status == "rto":
            # In an RTO, customer paid 0. Goods returned to supplier/warehouse.
            # Loss = Courier outbound + RTO return penalty + Flyer packaging damaged
            rto_loss = COURIER_DISPATCH_FEE_PKR + COURIER_RTO_RETURN_PENALTY_PKR + packaging_cost
            return {
                "order_id": order.get("order_id"),
                "status": "rto",
                "gross_revenue": 0.0,
                "wholesale_cost": 0.0,  # Item returned
                "courier_paid": COURIER_DISPATCH_FEE_PKR,
                "packaging_cost": packaging_cost,
                "rto_loss": rto_loss,
                "net_profit": -round(rto_loss, 2),
                "profit_margin_pct": -100.0,
                "is_profitable": False,
            }

        else:
            return {
                "order_id": order.get("order_id"),
                "status": status,
                "gross_revenue": 0.0,
                "wholesale_cost": wholesale_cost,
                "courier_paid": COURIER_DISPATCH_FEE_PKR,
                "packaging_cost": packaging_cost,
                "rto_loss": 0.0,
                "net_profit": 0.0,
                "profit_margin_pct": 0.0,
                "is_profitable": True,
            }

    def compute_period_pnl_statement(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generates comprehensive financial statement for an order cohort."""
        total_delivered = 0
        total_rto = 0
        total_in_transit = 0
        gross_sales = 0.0
        shipping_collected = 0.0
        wholesale_costs = 0.0
        courier_costs = 0.0
        rto_losses = 0.0
        net_profit_total = 0.0

        for o in orders:
            res = self.compute_order_net_profit(o)
            st = res["status"]
            if st == "delivered":
                total_delivered += 1
                gross_sales += float(o.get("sale_price_pkr", 0.0))
                shipping_collected += float(o.get("shipping_fee_collected", settings.DEFAULT_DELIVERY_FEE_PKR))
                wholesale_costs += res["wholesale_cost"]
                courier_costs += res["courier_paid"] + res["packaging_cost"]
                net_profit_total += res["net_profit"]
            elif st == "rto":
                total_rto += 1
                rto_losses += res["rto_loss"]
                net_profit_total += res["net_profit"]
            else:
                total_in_transit += 1

        total_orders = len(orders)
        rto_rate_pct = (float(total_rto) / float(total_orders) * 100.0) if total_orders > 0 else 0.0
        overall_margin_pct = (net_profit_total / gross_sales * 100.0) if gross_sales > 0 else 0.0

        return {
            "total_orders": total_orders,
            "delivered_count": total_delivered,
            "rto_count": total_rto,
            "in_transit_count": total_in_transit,
            "rto_rate_pct": round(rto_rate_pct, 1),
            "gross_product_sales_pkr": round(gross_sales, 2),
            "shipping_collected_pkr": round(shipping_collected, 2),
            "total_revenue_pkr": round(gross_sales + shipping_collected, 2),
            "supplier_costs_pkr": round(wholesale_costs, 2),
            "courier_and_flyer_expenses_pkr": round(courier_costs, 2),
            "rto_damage_losses_pkr": round(rto_losses, 2),
            "true_take_home_profit_pkr": round(net_profit_total, 2),
            "net_profit_margin_pct": round(overall_margin_pct, 2),
        }

