"""delete_view module defines the view that user wants to delete"""

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import View
from shortner.models import Link
import json
from django.shortcuts import redirect


class DeleteView(View):
    """DeleteView is responsible for deletion of the shortened links"""

    def get(self, request: HttpRequest, special_code: str):
        """delete handles requests to be deleted /delete"""
        special_codes = special_code
        try:
            member = Link.objects.get(special_code=special_codes) # pylint: disable=no-member
            member.delete()
            return redirect("list")
        except Exception as e:
            error_msg = {"exception": str(e)}
            return HttpResponse(json.dumps(error_msg), status=404)
