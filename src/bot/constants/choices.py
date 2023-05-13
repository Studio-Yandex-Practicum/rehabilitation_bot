from bot.constants import key
from bot.constants.models import SpecialtyFormModel


SPECIALTY = {
    f"{key.SPECIALTY}_frm": {
        key.NAME: "Врач ФРМ",
        key.BUTTON: "Врач ФРМ",
    },
    f"{key.SPECIALTY}_ftd": {
        key.NAME: "Врач ФТД",
        key.BUTTON: "Врач ФТД",
    },
    f"{key.SPECIALTY}_logoped": {
        key.NAME: "Логопед",
        key.BUTTON: "Логопед",
    },
    f"{key.SPECIALTY}_psy": {
        key.NAME: "Психолог",
        key.BUTTON: "Психолог",
    },
    f"{key.NAME}_npsy": {
        key.NAME: "Нейропсихолог",
        key.BUTTON: "Нейропсихолог",
    },
    f"{key.SPECIALTY}_custom": {
        key.BUTTON: "Другая специальность",
        key.MODEL: SpecialtyFormModel,
    },
}
