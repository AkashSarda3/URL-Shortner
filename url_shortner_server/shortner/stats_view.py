import csv
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.views.generic import View
from django.shortcuts import redirect, render
from django.urls import reverse
from datetime import datetime
from shortner.models import Link

class StatsView(View):
    """StatsView is responsible for displaying and exporting link statistics"""

    def get(self, request: HttpRequest):
        """Handles GET requests to display link statistics or export CSV"""
        username = request.session.get('username', '')
        if not username:
            return redirect('signin')

        if request.path.endswith('/export-csv/'):
            return self.export_csv(request)

        list_of_links = Link.objects.filter(username=username).order_by('-ctr')
        context = {'list_of_links': []}

        for link_obj in list_of_links:
            context['list_of_links'].append({
                'long_url': link_obj.long_url,
                'short_url': request.build_absolute_uri('/') + 'stub/' + link_obj.stub,
                'special_code': link_obj.special_code,
                'ctr': link_obj.ctr
            })

        context['list_of_links'] = sorted(context['list_of_links'],
                                          key=lambda d: d['ctr'], reverse=True)
        
        # Add CSV export URL to the context
        context['csv_export_url'] = reverse('export_csv')

        return render(request, "homepages/urlstats.html", context=context)

    def export_csv(self, request: HttpRequest):
        """Exports link statistics as CSV with date and time in filename"""
        username = request.session.get('username', '')
        if not username:
            return redirect('signin')

        list_of_links = Link.objects.filter(username=username).order_by('-ctr')

        # Generate filename with current date and time
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"link_statistics_{current_datetime}.csv"

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(['Long URL', 'Short URL','CTR'])

        for link_obj in list_of_links:
            writer.writerow([
                link_obj.long_url,
                request.build_absolute_uri('/') + 'stub/' + link_obj.stub,
                link_obj.ctr
            ])

        return response
