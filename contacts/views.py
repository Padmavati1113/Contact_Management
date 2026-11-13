
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Contact
from django.db.models.functions import Trim, Lower


# Dashboard and Contact Search
def dashboard(request):
    search_query = request.GET.get('q', '').strip()

    contacts = Contact.objects.annotate(
    clean_name=Lower(Trim('full_name'))
).order_by('clean_name')

    if search_query:
        contacts = contacts.filter(
            Q(full_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(company__icontains=search_query)
        )

    total_contacts = Contact.objects.count()

    return render(request, 'contacts/dashboard.html', {
        'total_contacts': total_contacts,
        'contacts': contacts,
        'search_query': search_query
    })


# Add New Contact
def add_contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        company = request.POST.get('company')
        address = request.POST.get('address')

        Contact.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            company=company,
            address=address
        )

        return redirect('dashboard')

    return render(request, 'contacts/add_contact.html')


# Edit Existing Contact
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        contact.full_name = request.POST.get('full_name')
        contact.phone = request.POST.get('phone')
        contact.email = request.POST.get('email')
        contact.company = request.POST.get('company')
        contact.address = request.POST.get('address')

        contact.save()

        return redirect('dashboard')

    return render(request, 'contacts/edit_contact.html', {
        'contact': contact
    })
# Delete Existing Contact
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        contact.delete()
        return redirect('dashboard')

    return redirect('dashboard')