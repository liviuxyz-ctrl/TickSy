from django.http import JsonResponse
from fastapi import FastAPI
from ..models import Tickets
from ..views import logger


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
            logger.debug(ticket.due_datetime.year)
            team_name = ticket.responsible_team_id.team_name
            employee_name = ticket.responsible_employee_id.full_name
            due_date = ticket.due_datetime.strftime("%c")
            creation_time = ticket.created_at.strftime("%c")
            ticket_information = {
                "ticket_id": str(ticket_id),
                "user_full_name": ticket.user_full_name,
                "user_email": ticket.user_email,
                "created_at": creation_time,
                "due_datetime": due_date,
                "finish_at": ticket.finish_at,
                "status": ticket.status,
                "importance": ticket.importance,
                "responsible_team_name": team_name,
                "responsible_employee_name": employee_name,
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

@app.get("/ticket-count")
def retrieve_ticket_count(request):
    if request.session.get('login_state', default=False):
        ticket_count = Tickets.objects.count()

        return JsonResponse(data={
            'number_of_tickets': ticket_count})

    else:
        logger.debug(f"Number of tickets deny, user not logged in!")
        api_deny_response = {
            "ticket_lookup_deny": True
        }
        return JsonResponse(data=api_deny_response)
