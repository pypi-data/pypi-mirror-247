import datetime
import logging
from typing import Any

from django.core.cache import DEFAULT_CACHE_ALIAS
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.timezone import now

from update_cache.brokers import Broker, default_broker, get_broker, get_view_broker, ViewBroker
from update_cache.cache.cache import CacheResult, missing
from update_cache.cache.registry import CachedFunction
from update_cache.cache.views import should_cache_view


logger = logging.getLogger(__name__)


class CacheUpdateHandler:

    backend: str

    cached_function: CachedFunction

    timeout: int

    cache_args: bool

    def get_result(self, key: str, *args, **kwargs) -> Any:
        logger.info(f'Retrieving active cache for {key}')
        result = self.cached_function.get_active(key, missing)
        if result != missing:
            # See if the result has expired
            if result.has_expired:
                logger.info(f'Active cache for {key} has expired')
                # Make it the expired version
                self.cached_function.set_expired(key, result)
            return result.result

        # Next, see if there is an expired version
        logger.info(f'Retrieving expired cache for {key}')
        result = self.cached_function.get_expired(key, missing)
        if result != missing:
            # Delegate the function call, delete and then return the expired version
            logger.info(f'Delegating function call for {key}')
            self.delegate(*args, **kwargs)
            return result.result

        # No version found in cache, get live result and cache it
        logger.info(f'Getting live result for {key}')
        live_result = self.execute(*args, **kwargs)
        self.save_result(key, live_result, *args, **kwargs)
        return live_result

    def execute(self, *args, **kwargs):
        live_result = self.cached_function.f(*args, **kwargs)
        return live_result

    def delegate(self, *args, **kwargs):
        self.get_broker()(self.cached_function.f, self.timeout, (args, kwargs), self.backend)

    def save_result(self, key: str, result: Any, *args, **kwargs):
        result = CacheResult(
            result=result,
            expires=now() + datetime.timedelta(seconds=self.timeout),
            calling_args=(args, kwargs) if self.cache_args else None
        )
        self.cached_function.set_active(key, result)

    def get_broker(self) -> Any:
        raise NotImplementedError()


class DefaultUpdateHandler(CacheUpdateHandler):

    broker: Broker

    cache_args = True

    def __init__(self, cached_function: CachedFunction, timeout: int = DEFAULT_TIMEOUT,
                 backend: str = DEFAULT_CACHE_ALIAS, broker: Broker = default_broker):
        self.cached_function = cached_function
        self.timeout = 300 if timeout == DEFAULT_TIMEOUT else timeout
        self.backend = backend
        self.broker = broker

    def get_broker(self) -> Any:
        return get_broker(self.broker)


class ViewUpdateHandler(CacheUpdateHandler):

    broker: ViewBroker

    cache_args = False

    def __init__(self, cached_function: CachedFunction, timeout: int = DEFAULT_TIMEOUT,
                 backend: str = DEFAULT_CACHE_ALIAS, broker: ViewBroker = default_broker):
        self.cached_function = cached_function
        self.timeout = 300 if timeout == DEFAULT_TIMEOUT else timeout
        self.backend = backend
        self.broker = broker

    def delegate(self, *args, **kwargs):
        # First arg should be request
        args = list(args)
        request = args.pop(0)
        self.get_broker()(self.cached_function.f, self.timeout, request, (tuple(args), kwargs), self.backend)

    def save_result(self, key: str, result: Any, *args, **kwargs):
        # First arg should be request
        request = list(args).pop(0)
        if not should_cache_view(request, result):
            return

        _save_result = lambda r: super(ViewUpdateHandler, self).save_result(key, r, *args, **kwargs)

        if hasattr(result, "render") and callable(result.render):
            result.add_post_render_callback(_save_result)
        else:
            super().save_result(key, result,  *args, **kwargs)

    def get_broker(self) -> Any:
        return get_view_broker(self.broker)
