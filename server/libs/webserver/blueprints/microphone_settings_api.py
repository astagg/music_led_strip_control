from libs.webserver.executer import Executer

from flask import Blueprint, request, jsonify, send_file, flash
from flask_login import login_required
import copy
import json

microphone_settings_api = Blueprint('microphone_settings_api', __name__)


@microphone_settings_api.route('/api/settings/microphone/volume', methods=['GET'])
@login_required
def microphone_get_volume():  # pylint: disable=E0211

    data_out = dict()

    settings = Executer.instance.microphone_settings_executer.microphone_get_volume()
    data_out = settings

    if settings is None:
        return "Could not find settings value", 403
    else:
        return jsonify(data_out)


@microphone_settings_api.route('/api/settings/microphone/volume', methods=['POST'])
@login_required
def microphone_set_volume():  # pylint: disable=E0211

    data_in = request.get_json()
    data_out = dict()

    if not Executer.instance.effect_executer.validate_data_in(data_in, ("level",)):
        return "Input data are wrong.", 403

    settings = Executer.instance.microphone_settings_executer.microphone_set_volume(
        data_in["level"])
    data_out = settings

    if settings is None:
        return "Could not find settings value", 403
    else:
        return jsonify(data_out)
