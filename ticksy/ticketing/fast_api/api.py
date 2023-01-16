from django.http import JsonResponse
from fastapi import FastAPI
from ..models import Tickets
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
    ticket = get_object_or_404(Tickets, id=ticket_id)
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
    return JsonResponse(data=ticket_information)