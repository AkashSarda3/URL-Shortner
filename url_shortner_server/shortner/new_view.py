"""new_view module defines the NewView view"""

import csv
from django.http import HttpRequest, HttpResponseBadRequest
from django.views.generic import View
from django.shortcuts import redirect
from shortner.models import Link

class NewView(View):
    """NewView is responsible for the creation of new shortened links"""

    def post(self, request: HttpRequest):
        """Create a new link"""
        username = request.session.get('username')
        if not username:
            return redirect('signin')

        
        if request.FILES.get('file'):  # Handle CSV file uploads
            uploaded_file = request.FILES['file']
            if uploaded_file.name.endswith('.csv'):
                try:
                    csv_reader = csv.DictReader(uploaded_file.read().decode('utf-8').splitlines())
                    existing_stubs = set(Link.objects.values_list('stub', flat=True)) # pylint: disable=no-member
                    for row in csv_reader:
                        long_url = next((value for key, value in row.items() if 'link' in key), None)
                        custom_stub = row.get('stub', '').strip()
                        if long_url:
                            link = Link(long_url=long_url, username=username)
                            if custom_stub:
                                if custom_stub in existing_stubs:
                                    return HttpResponseBadRequest(f"Custom stub '{custom_stub}' is already in use.")
                                existing_stubs.add(custom_stub)
                                link.save_custom(custom_stub)
                            else:
                                link.save()

                except Exception as e:
                    return HttpResponseBadRequest(f"Error processing file: {str(e)}")
            else:
                return HttpResponseBadRequest("Uploaded file is not a CSV.")
            
        elif 'long-url' in request.POST:  # Handle manual URL submissions
            long_urls = request.POST['long-url'].split(',')
            custom_stubs = request.POST.get('custom-stub', '').split(',')
            custom_stubs = [stub.strip() for stub in custom_stubs][:len(long_urls)]

            for index, long_url in enumerate(long_urls):
                long_url = long_url.strip()
                if not long_url:
                    continue
                link = Link(long_url=long_url, username=username)
                if index < len(custom_stubs) and custom_stubs[index]:
                    custom_stub = custom_stubs[index]
                    if Link.objects.filter(stub=custom_stub).exists(): # pylint: disable=no-member
                        return HttpResponseBadRequest(f"Custom stub '{custom_stub}' is already in use.")
                    link.save_custom(custom_stub)
                else:
                    link.save()

        return redirect('list')