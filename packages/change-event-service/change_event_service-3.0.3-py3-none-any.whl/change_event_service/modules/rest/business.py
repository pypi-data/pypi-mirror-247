from http import HTTPStatus

from flask_smorest import abort

from change_event_service.database import db
from change_event_service.modules.rest.models import ChangeEventModel
from change_event_service.modules.rest.utils import ResponseObject, PaginationObject
from sqlalchemy import and_, or_, text


def create_change_event(args):
    """
    Create a change event
    """
    try:
        change_event = ChangeEventModel(**args)
        db.session.add(change_event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message='Error creating change event', exc=e)
    return ResponseObject(message='Change event created', statusCode=HTTPStatus.CREATED)


def get_change_event(change_event_id):
    """
    Get a change event by id
    """
    try:
        change_event = ChangeEventModel.query.filter_by(id=change_event_id).first()
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message='Error getting change event', exc=e)
    if not change_event:
        abort(HTTPStatus.NOT_FOUND, message='Change event not found')
    return ResponseObject(data=change_event, statusCode=HTTPStatus.OK)


def delete_change_event(change_event_id):
    """
    Delete a change event by id
    """
    try:
        change_event = ChangeEventModel.query.filter_by(id=change_event_id).first()
    except Exception as e:
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message='Error deleting change event', exc=e)

    if not change_event:
        abort(HTTPStatus.NOT_FOUND, message='Change event not found')
    db.session.delete(change_event)
    db.session.commit()
    return ResponseObject(message='Change event deleted', statusCode=HTTPStatus.OK)


def filter_change_events(args, pagination_params):
    """
    Filter change events
    """

    filter_args = args.copy()
    event_time = filter_args.pop('event_time', None)
    tag = filter_args.pop('tag', None)
    object_names = filter_args.pop('object_name', None)
    event_types = filter_args.pop('event_type', None)
    ip = filter_args.pop('ip', None)
    change_events = []
    pagination_data = None
    q = ChangeEventModel.query

    if tag:
        q = q.filter(ChangeEventModel.tag_tsv.match('&'.join(tag)))

        for _tag in tag:
            q = q.filter(text(f"'{_tag.strip()}' = any(string_to_array(tbl_audit_log.tag, ','))"))

    if event_types:
        q = q.filter(ChangeEventModel.event_type.in_(event_types))

    if object_names:
        q = q.filter(ChangeEventModel.object_name.in_(object_names))

    if event_time:
        start_date = event_time[0]
        end_date = event_time[1]
        q = q.filter(and_(ChangeEventModel.event_time >= start_date, ChangeEventModel.event_time <= end_date))

    if ip:
        q = q.filter(ChangeEventModel.ip.like(f"%{ip}%"))

    try:
        if filter_args:
            change_events = q.filter_by(**filter_args)\
                .order_by(ChangeEventModel.event_time.desc())\
                .paginate(page=pagination_params.page, per_page=pagination_params.page_size)

            pagination_data = PaginationObject(page=change_events.page, total=change_events.total,
                                               total_pages=change_events.pages)
            change_events = change_events.items
        else:
            change_events = q\
                .order_by(ChangeEventModel.event_time.desc())\
                .paginate(page=pagination_params.page, per_page=pagination_params.page_size)
            pagination_data = PaginationObject(page=change_events.page, total=change_events.total,
                                               total_pages=change_events.pages)
            change_events = change_events.items

    except Exception as e:
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message='Error filtering change events', exc=e)
    return ResponseObject(data=change_events, page=pagination_data, statusCode=HTTPStatus.OK)
