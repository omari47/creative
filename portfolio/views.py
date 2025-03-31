from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import PortfolioItem, Category


def portfolio_list(request):
    """View all portfolio items"""
    items = PortfolioItem.objects.all()
    categories = Category.objects.all()

    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)

    context = {
        'items': items,
        'categories': categories,
        'active_category': category_slug,
    }
    return render(request, 'portfolio/portfolio_list.html', context)


def portfolio_detail(request, item_id):
    """View a specific portfolio item"""
    item = get_object_or_404(PortfolioItem, id=item_id)
    context = {'item': item}
    return render(request, 'portfolio/portfolio_detail.html', context)