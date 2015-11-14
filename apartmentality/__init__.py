import datetime
import json

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.set_root_factory("apartmentality.views:RootResource")

    config.add_renderer("api", "apartmentality:APIRendererFactory")

    config.scan()
    return config.make_wsgi_app()


class APIRendererFactory(object):
    _flat_types = [
        type(None),
        int,
        float,
        bool,
        str,
    ]

    @classmethod
    def flatten_obj(cls, obj):
        """Turn an object into a JSON-serializiable value.

        Args:
            obj: The object to flatten

        Returns:
            A JSON-serializable value.
        """
        if isinstance(obj, cls._flat_types):
            val = obj
        elif isinstance(obj, (list, tuple, set)):
            val = []
            for sub_obj in obj:
                try:
                    sub_val = cls.flatten_obj(sub_obj)
                    val.append(sub_val)
                except TypeError:
                    pass
        elif isinstance(obj, dict):
            val = {}
            for sub_key, sub_obj in obj.items():
                try:
                    val[sub_key] = cls.flatten_obj(sub_obj)
                except TypeError:
                    pass
        elif isinstance(obj, datetime.datetime):
            val = str(datetime.datetime)
        elif isinstance(obj, object):
            val = {}
            for sub_key, sub_obj in obj.__dict__.items():
                if not isinstance(sub_obj, cls._flat_types):
                    continue
                if sub_key[0] == "_":
                    continue
                val[sub_key] = sub_obj
        else:
            raise TypeError(obj)

        return val

    def __init__(self, info):
        self.info = info

    def __call__(self, value, system):
        request = system["request"]
        request.response.content_type = "application/json"

        val = self.flatten_obj(value)
        val_str = json.dumps(val, indent=4, sort_keys=True)
        return val_str
