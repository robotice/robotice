#
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Robotice exception subclasses"""

import functools
import sys

import six
from six.moves.urllib import parse as urlparse

from robotice.common.i18n import _

import logging

_FATAL_EXCEPTION_FORMAT_ERRORS = False


LOG = logging.getLogger(__name__)


class RedirectException(Exception):
    def __init__(self, url):
        self.url = urlparse.urlparse(url)


class KeystoneError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return "Code: %s, message: %s" % (self.code, self.message)


def wrap_exception(notifier=None, publisher_id=None, event_type=None,
                   level=None):
    """This decorator wraps a method to catch any exceptions that may
    get thrown. It logs the exception as well as optionally sending
    it to the notification system.
    """
    # TODO(sandy): Find a way to import nova.notifier.api so we don't have
    # to pass it in as a parameter. Otherwise we get a cyclic import of
    # nova.notifier.api -> nova.utils -> nova.exception :(
    # TODO(johannes): Also, it would be nice to use
    # utils.save_and_reraise_exception() without an import loop
    def inner(f):
        def wrapped(*args, **kw):
            try:
                return f(*args, **kw)
            except Exception as e:
                # Save exception since it can be clobbered during processing
                # below before we can re-raise
                exc_info = sys.exc_info()

                if notifier:
                    payload = dict(args=args, exception=e)
                    payload.update(kw)

                    # Use a temp vars so we don't shadow
                    # our outer definitions.
                    temp_vel = level
                    if not temp_vel:
                        temp_vel = notifier.ERROR

                    temp_type = event_type
                    if not temp_type:
                        # If f has multiple decorators, they must use
                        # functools.wraps to ensure the name is
                        # propagated.
                        temp_type = f.__name__

                    notifier.notify(publisher_id, temp_type, temp_vel,
                                    payload)

                # re-raise original exception since it may have been clobbered
                raise exc_info[0], exc_info[1], exc_info[2]

        return functools.wraps(f)(wrapped)
    return inner


class RoboticeException(Exception):
    """Base Robotice Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = _("An unknown exception occurred.")

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        try:
            self.message = self.msg_fmt % kwargs
        except KeyError:
            exc_info = sys.exc_info()
            # kwargs doesn't match a variable in the message
            # log the issue and the kwargs
            LOG.exception(_('Exception in string format operation'))
            for name, value in six.iteritems(kwargs):
                LOG.error("%s: %s" % (name, value))  # noqa

            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise exc_info[0], exc_info[1], exc_info[2]

    def __str__(self):
        return unicode(self.message).encode('UTF-8')

    def __unicode__(self):
        return unicode(self.message)

    def __deepcopy__(self, memo):
        return self.__class__(**self.kwargs)


class MissingCredentialError(RoboticeException):
    msg_fmt = _("Missing required credential: %(required)s")


class BadAuthStrategy(RoboticeException):
    msg_fmt = _("Incorrect auth strategy, expected \"%(expected)s\" but "
                "received \"%(received)s\"")


class AuthBadRequest(RoboticeException):
    msg_fmt = _("Connect error/bad request to Auth service at URL %(url)s.")


class AuthUrlNotFound(RoboticeException):
    msg_fmt = _("Auth service at URL %(url)s not found.")


class AuthorizationFailure(RoboticeException):
    msg_fmt = _("Authorization failed.")


class NotAuthenticated(RoboticeException):
    msg_fmt = _("You are not authenticated.")


class Forbidden(RoboticeException):
    msg_fmt = _("You are not authorized to complete this action.")


# NOTE(bcwaldon): here for backwards-compatibility, need to deprecate.
class NotAuthorized(Forbidden):
    msg_fmt = _("You are not authorized to complete this action.")


class Invalid(RoboticeException):
    msg_fmt = _("Data supplied was not valid: %(reason)s")


class AuthorizationRedirect(RoboticeException):
    msg_fmt = _("Redirecting to %(uri)s for authorization.")


class RequestUriTooLong(RoboticeException):
    msg_fmt = _("The URI was too long.")


class MaxRedirectsExceeded(RoboticeException):
    msg_fmt = _("Maximum redirects (%(redirects)s) was exceeded.")


class InvalidRedirect(RoboticeException):
    msg_fmt = _("Received invalid HTTP redirect.")


class RegionAmbiguity(RoboticeException):
    msg_fmt = _("Multiple 'image' service matches for region %(region)s. This "
                "generally means that a region is required and you have not "
                "supplied one.")


class UserParameterMissing(RoboticeException):
    msg_fmt = _("The Parameter (%(key)s) was not provided.")


class UnknownUserParameter(RoboticeException):
    msg_fmt = _("The Parameter (%(key)s) was not defined in template.")


class PhysicalResourceNameAmbiguity(RoboticeException):
    msg_fmt = _(
        "Multiple physical resources were found with name (%(name)s).")



class ResourceFailure(RoboticeException):
    msg_fmt = _("%(exc_type)s: %(message)s")

    def __init__(self, exception, resource, action=None):
        if isinstance(exception, ResourceFailure):
            exception = getattr(exception, 'exc', exception)
        self.exc = exception
        self.resource = resource
        self.action = action
        exc_type = type(exception).__name__
        super(ResourceFailure, self).__init__(exc_type=exc_type,
                                              message=six.text_type(exception))


class NotSupported(RoboticeException):
    msg_fmt = _("%(feature)s is not supported.")


class ResourceActionNotSupported(RoboticeException):
    msg_fmt = _("%(action)s is not supported for resource.")


class ResourcePropertyConflict(RoboticeException):
    msg_fmt = _('Cannot define the following properties '
                'at the same time: %(props)s.')

    def __init__(self, *args, **kwargs):
        if args:
            kwargs.update({'props': ", ".join(args)})
        super(ResourcePropertyConflict, self).__init__(**kwargs)


class PropertyUnspecifiedError(RoboticeException):
    msg_fmt = _('At least one of the following properties '
                'must be specified: %(props)s')

    def __init__(self, *args, **kwargs):
        if args:
            kwargs.update({'props': ", ".join(args)})
        super(PropertyUnspecifiedError, self).__init__(**kwargs)


class HTTPExceptionDisguise(Exception):
    """Disguises HTTP exceptions so they can be handled by the webob fault
    application in the wsgi pipeline.
    """

    def __init__(self, exception):
        super(HTTPExceptionDisguise, self).__init__(exception)
        self.exc = exception
        self.tb = sys.exc_info()[2]


class EgressRuleNotAllowed(RoboticeException):
    msg_fmt = _("Egress rules are only allowed when "
                "Neutron is used and the 'VpcId' property is set.")


class Error(RoboticeException):
    msg_fmt = "%(message)s"

    def __init__(self, msg):
        super(Error, self).__init__(message=msg)


class NotFound(RoboticeException):
    def __init__(self, msg_fmt=_('Not found')):
        self.msg_fmt = msg_fmt
        super(NotFound, self).__init__()


class InvalidContentType(RoboticeException):
    msg_fmt = _("Invalid content type %(content_type)s")


class RequestLimitExceeded(RoboticeException):
    msg_fmt = _('Request limit exceeded: %(message)s')


class StackResourceLimitExceeded(RoboticeException):
    msg_fmt = _('Maximum resources per stack exceeded.')


class ActionInProgress(RoboticeException):
    msg_fmt = _("Stack %(stack_name)s already has an action (%(action)s) "
                "in progress.")


class StopActionFailed(RoboticeException):
    msg_fmt = _("Failed to stop stack (%(stack_name)s) on other engine "
                "(%(engine_id)s)")


class EventSendFailed(RoboticeException):
    msg_fmt = _("Failed to send message to stack (%(stack_name)s) "
                "on other engine (%(engine_id)s)")