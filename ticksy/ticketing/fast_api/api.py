from django.http import JsonResponse
from fastapi import FastAPI
from ..models import Tickets
from ..views import logger
from django.shortcuts import get_object_or_404


app = FastAPI()

class TicketInfo(Tickets):
    user_full_name : str
    user_email : str
    created_at : str
    due_datetime : str
    finish_at : str
    status : str
    importance : str
    responsible_team_id : str
    responsible_employee_id : str
    description : str

@app.get("/ticket/{ticket_id}")
def lookup_ticket(request, ticket_id : int):
    if request.session.get('login_state', default=False):

        try:
            ticket = Tickets.objects.get(id=ticket_id)
            ticket_information = {
                "user_full_name": ticket.user_full_name,
                "user_email": ticket.user_email,
                "created_at": ticket.created_at,
                "due_datetime": ticket.due_datetime,
                "finish_at": ticket.finish_at,
                "status": ticket.status,
                "importance": ticket.importance,
                "responsible_team_id": ticket.responsible_team_id.id,
                "responsible_employee_id": ticket.responsible_employee_id.id,
                "description": ticket.description
            }
        except:
            ticket_information = {
                "ticket_lookup_failure":  True,
                "reason": f"No ticket with id '{ticket_id}' found!"
            }

        return JsonResponse(data=ticket_information)

    else:
        logger.debug(f"Team lookup deny, user not logged in!")
        api_deny_response = {
            "ticket_lookup_deny": True
        }
        return JsonResponse(data=api_deny_response)
