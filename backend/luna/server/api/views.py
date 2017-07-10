from flask import Blueprint, json
from flask.views import MethodView
from luna.server.repositories import CityRepository, FederativeUnitRepository, ModuleRepository


api_blueprint = Blueprint('api', __name__)


class FederativeUnitAPI(MethodView):

    def get(self, id):
        if id is not None:
            return json.jsonify(dict(status=True, data=dict(FederativeUnitRepository().find(id)), message='Federative Unit returned.'))
        return json.jsonify(dict(status=True, data=[dict(x) for x in FederativeUnitRepository().all()], message='Federative Units returned.'))


class CityAPI(MethodView):

    def get(self, federative_unit_id, id):
        if id is not None:
            return json.jsonify(dict(status=True, data=dict(CityRepository().find(id)), message='City returned.'))
        return json.jsonify(dict(status=True, data=[dict(x) for x in CityRepository().allByFederativeUnit(federative_unit_id)], message='Cities returned.'))


class ModuleAPI(MethodView):
    
    def get(self, identifier):
        if identifier is not None:
            return json.jsonify(dict(
                status=True,
                data=dict(ModuleRepository().findByIdentifier(identifier)),
                message='Module returned.'
            ))
        return json.jsonify(dict(status=True, data=[dict(x) for x in ModuleRepository().all()], message='Modules returned.'))


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    api_blueprint.add_url_rule(url, defaults={pk: None},
                               view_func=view_func, methods=['GET', ])
    api_blueprint.add_url_rule('%s<%s:%s>/' % (url, pk_type, pk), view_func=view_func,
                               methods=['GET'])
    # api_blueprint.add_url_rule(url, view_func=view_func, methods=['POST',])
    # api_blueprint.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
    #                  methods=['GET', 'PUT', 'DELETE'])


register_api(FederativeUnitAPI, 'uf_api', '/federative_units/')
register_api(CityAPI, 'city_api', '/federative_units/<int:federative_unit_id>/cities/')
register_api(ModuleAPI, 'module_api', '/modules/', pk='identifier', pk_type='string')
