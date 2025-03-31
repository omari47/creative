from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Workshop, Registration


def workshop_list(request):
    """View all workshops"""
    upcoming_workshops = Workshop.objects.filter(date__gte=timezone.now()).order_by('date')
    past_workshops = Workshop.objects.filter(date__lt=timezone.now()).order_by('-date')

    context = {
        'upcoming_workshops': upcoming_workshops,
        'past_workshops': past_workshops,
    }
    return render(request, 'workshops/workshop_list.html', context)


def workshop_detail(request, workshop_id):
    """View a specific workshop"""
    workshop = get_object_or_404(Workshop, id=workshop_id)

    # Check if user is registered
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(
            user=request.user,
            workshop=workshop
        ).exists()

    context = {
        'workshop': workshop,
        'is_registered': is_registered,
    }
    return render(request, 'workshops/workshop_detail.html', context)


@login_required
def register_workshop(request, workshop_id):
    """Register for a workshop"""
    workshop = get_object_or_404(Workshop, id=workshop_id)

    # Check if already registered
    if Registration.objects.filter(user=request.user, workshop=workshop).exists():
        messages.info(request, 'You are already registered for this workshop.')
        return redirect('workshops:detail', workshop_id=workshop_id)

    # Check if seats available
    if workshop.seats_available <= 0:
        messages.error(request, 'Sorry, this workshop is fully booked.')
        return redirect('workshops:detail', workshop_id=workshop_id)

    # Create registration
    Registration.objects.create(
        user=request.user,
        workshop=workshop,
        payment_status='pending'
    )

    # Reduce seats available
    workshop.seats_available -= 1
    workshop.save()

    messages.success(request, 'You have been registered for the workshop!')
    # Redirect to payment if needed
    # return redirect('payments:workshop_payment', workshop_id=workshop_id)
    return redirect('workshops:detail', workshop_id=workshop_id)


@login_required
def cancel_registration(request, workshop_id):
    """Cancel workshop registration"""
    workshop = get_object_or_404(Workshop, id=workshop_id)
    registration = get_object_or_404(Registration, user=request.user, workshop=workshop)

    # Only allow cancellation if it's not completed payment
    if registration.payment_status == 'completed':
        messages.error(request, 'You cannot cancel a completed registration.')
        return redirect('workshops:detail', workshop_id=workshop_id)

    # Delete registration
    registration.delete()

    # Increase seats available
    workshop.seats_available += 1
    workshop.save()

    messages.success(request, 'Your registration has been cancelled.')
    return redirect('workshops:detail', workshop_id=workshop_id)


@login_required
def my_workshops(request):
    """View user's registered workshops"""
    registrations = Registration.objects.filter(user=request.user).order_by('workshop__date')

    context = {'registrations': registrations}
    return render(request, 'workshops/my_workshops.html', context)