# Keys
# SRC: https://doc.qt.io/archives/qtjambi-4.5.2_01/com/trolltech/qt/core/Qt.Key.html
class SPBC:
    def __init__(self, min_, max_, step_):
        self.min = float(min_)
        self.max = float(max_)
        self.step = float(step_)


class UiSpinboxConstraints:
    # Quadplane tuning parameter constraints.
    # Source: https://ardupilot.org/plane/docs/parameters.html#q-parameters

    ROLL_STAB_P = SPBC(3, 12, 0.001)
    PITCH_STAB_P = SPBC(3, 12, 0.001)
    YAW_STAB_P = SPBC(3, 12, 0.001)

    ROLL_RATE_P = SPBC(0.01, 0.5, 0.005)
    ROLL_RATE_I = SPBC(0.01, 2.0, 0.01)
    ROLL_RATE_D = SPBC(0, 0.05, 0.001)

    PITCH_RATE_P = SPBC(0.01, 0.5, 0.005)
    PITCH_RATE_I = SPBC(0.01, 2.0, 0.01)
    PITCH_RATE_D = SPBC(0, 0.05, 0.001)

    YAW_RATE_P = SPBC(0.1, 2.5, 0.005)
    YAW_RATE_I = SPBC(0.01, 1.0, 0.01)
    YAW_RATE_D = SPBC(0, 0.02, 0.001)

    # FIXME: Boilerplate

    def get_constraint_list_by_axis(self, axis):
        if axis == 0:
            return [self.ROLL_RATE_P, self.ROLL_RATE_I, self.ROLL_RATE_D, self.ROLL_STAB_P]
        elif axis == 1:
            return [self.PITCH_RATE_P, self.PITCH_RATE_I, self.PITCH_RATE_D, self.PITCH_STAB_P]
        elif axis == 2:
            return [self.YAW_RATE_P, self.YAW_RATE_I, self.YAW_RATE_D, self.YAW_STAB_P]
