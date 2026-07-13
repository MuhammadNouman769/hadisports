from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .services import DashboardService

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all dashboard data
        context['stats'] = DashboardService.get_stats()
        context['recent_orders'] = DashboardService.get_recent_orders(limit=8)
        context['activity_log'] = DashboardService.get_activity_log(limit=15)
        context['chart_data'] = DashboardService.get_chart_data()
        context['top_products'] = DashboardService.get_top_products(limit=6)
        
        # Add page metadata
        context['page_title'] = 'Dashboard'
        context['page_subtitle'] = 'Overview of your store performance'
        
        return context

@method_decorator(staff_member_required, name='dispatch')
class WidgetsView(TemplateView):
    template_name = 'admin/widgets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Widgets'
        return context

@method_decorator(staff_member_required, name='dispatch')
class ChartsView(TemplateView):
    template_name = 'admin/charts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Charts'
        context['chart_data'] = DashboardService.get_chart_data(days=90)
        return context

# API endpoints for AJAX data
@staff_member_required
def api_stats(request):
    """API endpoint for statistics data"""
    return JsonResponse(DashboardService.get_stats())

@staff_member_required
def api_chart_data(request):
    """API endpoint for chart data"""
    days = request.GET.get('days', 30)
    try:
        days = int(days)
    except ValueError:
        days = 30
    return JsonResponse(DashboardService.get_chart_data(days=days))

@staff_member_required
def api_recent_orders(request):
    """API endpoint for recent orders"""
    limit = request.GET.get('limit', 10)
    try:
        limit = int(limit)
    except ValueError:
        limit = 10
    orders = DashboardService.get_recent_orders(limit=limit)
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'customer': order.user.username if order.user else 'Guest',
            'total': str(order.total_amount) if hasattr(order, 'total_amount') else '0.00',
            'status': order.status if hasattr(order, 'status') else 'pending',
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(order, 'created_at') else '',
        })
    return JsonResponse({'orders': data})