from __future__ import annotations
import numpy as np
from geometry import Transformation, PX, PY, PZ, P0
from flightdata import State, Time
from .element import Element
from flightanalysis.scoring.criteria.f3a_criteria import F3A
from flightanalysis.scoring import Measurement, DownGrade, DownGrades


class StallTurn(Element):
    parameters = Element.parameters + ["yaw_rate"]
    def __init__(self, speed:float, yaw_rate:float=3.0, uid: str=None):
        super().__init__(uid, speed)
        self.yaw_rate = yaw_rate

    @property
    def intra_scoring(self) -> DownGrades:
        return DownGrades([
            DownGrade(Measurement.roll_angle, F3A.intra.roll),
            #DownGrade(Measurement.track_y, F3A.single.track)  # track_y doesn't work as template velocity is zero
        ])

    def describe(self):
        return f"stallturn, yaw rate = {self.yaw_rate}"

    def create_template(self, istate: State, time: Time=None) -> State:
        return self._add_rolls(
            istate.copy(rvel=P0() ,vel=P0()).fill( 
                Element.create_time(np.pi / abs(self.yaw_rate), time)
            ).superimpose_rotation(
                PZ(), 
                np.sign(self.yaw_rate) * np.pi
            ), 
            0.0
        )

    def match_axis_rate(self, yaw_rate: float) -> StallTurn:
        return self.set_parms(yaw_rate=yaw_rate)

    def match_intention(self, transform: Transformation, flown: State) -> StallTurn:
        return self.set_parms(
            yaw_rate=flown.data.r[flown.data.r.abs().idxmax()]
        )

    def copy_direction(self, other) -> StallTurn:
        return self.set_parms(
            yaw_rate=abs(self.yaw_rate) * np.sign(other.yaw_rate)
        )
    
    def yaw_rate_visibility(self, st: State):
        return Measurement._vector_vis(
            st.att.transform_point(PZ(1)).mean(), 
            st.pos.mean()
        )