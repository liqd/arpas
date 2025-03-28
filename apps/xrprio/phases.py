from django.utils.translation import gettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class PrioritizePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = "prioritize"
    view = views.XRPrioView

    name = _("Prioritize phase")
    description = _("Prioritize and comment topics.")
    module_name = _("topic prioritization")

    features = {
        # "comment": (models.XRPrio,),
        # "rate": (models.XRPrio,),
    }


phases.content.register(PrioritizePhase())
