from fastapi import APIRouter
from sqlalchemy.orm import registry as reg_class

from . import _routes, _models, _events
from ..infrastructure.events.dispatcher import EventDispatcher


def load_module(router: APIRouter, registry: reg_class, event_dispatcher: EventDispatcher):
	router.include_router(_routes.router)

	_models.load_models(registry)
	_events.load_handler_events(event_dispatcher)
