from flask import current_app
from app import dba
from app.dbmodels.query_installation import QueryInstallation
from .base import BaseModel
# ===========================


class Installation(BaseModel):
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    display_name = db.Column(db.String(64), unique=True)
    """

    def __repr__(self):
        return '<InstallationStep %r>' % self.name
    # ____________________________

    def __init__(self):
        self.query = QueryInstallation(dba)
    # ____________________________

    def insert_steps(self):
        steps = [
            dict(step='hw_config', step_name='HW Config'),
            dict(step='installation', step_name='Installation'),
            dict(step='post_script', step_name='Post Installation Script'),
            dict(step='hw_wizard', step_name='HW Wizard'),
            dict(step='check_all', step_name='Check All'),
            dict(step='direct_io', step_name='Direct IO'),
            dict(step='fc_loopback', step_name='FC Loopback Test'),
            dict(
                step='internal_network',
                step_name='Internal Network Test'
            ),
            dict(step='disable_fc_port', step_name='Disable FC Port'),
            dict(step='mfg_suite', step_name='MFG Test Suite'),
            dict(step='enable_fc_port', step_name='Enable FC Port'),
            dict(step='check_all', step_name='Check All Test'),
            dict(step='cleanup', step_name='Clean Up'),
        ]

        for ind, step in enumerate(steps):
            step['priority'] = ind + 1
            self.query.create(step)
    # ____________________________

    def get_all(self):
        steps = self.query.read()

        # read() returns a list of DictRow objects
        # Casting to a list of dicts
        steps_to_return = [dict(step) for step in steps]
        current_app.logger.debug("Installation steps: %r", steps_to_return)
        return steps_to_return

# ===========================
