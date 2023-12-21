"""
  scenariogeneration
  https://github.com/pyoscx/scenariogeneration

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright (c) 2022 The scenariogeneration Authors.

"""

""" This is a collection of ready to use functions, to generate standard road snipets, like:
    - Simple straight road
    - Spiral-Arc-Spiral type of turns
    - Simple roads with different geometries and lanes
    - Simple junction roads
        limited to 3/4-way crossings with 90degree turns (3-way can be 120 deg aswell)
    - Creation of the junction based on the connecting roads and incomming/outgoing roads
"""
import numpy as np
import pyclothoids as pcloth
import copy
from .lane import Lane, RoadMark, LaneSection, Lanes, RoadLine
from .enumerations import (
    JunctionType,
    RoadMarkType,
    MarkRule,
    ContactPoint,
    ElementType,
    ObjectType,
)

from .geometry import Line, Arc, Spiral, PlanView
from .opendrive import Road
from .links import Junction, Connection, _get_related_lanesection, LaneLinker
from .exceptions import (
    GeneralIssueInputArguments,
    NotSameAmountOfLanesError,
    RemovedFunctionality,
)

from warnings import warn


def std_roadmark_solid():
    return RoadMark(RoadMarkType.solid, 0.2)


def std_roadmark_broken():
    roadmark = RoadMark(RoadMarkType.broken, 0.2)
    roadmark.add_specific_road_line(RoadLine(0.15, 3, 9, 0, 0))
    return roadmark


def std_roadmark_broken_long_line():
    roadmark = RoadMark(RoadMarkType.broken, 0.2)
    roadmark.add_specific_road_line(RoadLine(0.15, 9, 3, 0, 0))
    return roadmark


def std_roadmark_broken_tight():
    roadmark = RoadMark(RoadMarkType.broken, 0.2)
    roadmark.add_specific_road_line(RoadLine(0.15, 3, 3, 0, 0))
    return roadmark


def std_roadmark_broken_broken():
    roadmark = RoadMark(RoadMarkType.broken_broken)
    roadmark.add_specific_road_line(RoadLine(0.2, 3, 3, 0.2, 0))
    roadmark.add_specific_road_line(RoadLine(0.2, 3, 3, -0.2, 0))
    return roadmark


def std_roadmark_solid_solid():
    roadmark = RoadMark(RoadMarkType.solid_solid)
    roadmark.add_specific_road_line(RoadLine(0.2, 0, 0, 0.2, 0))
    roadmark.add_specific_road_line(RoadLine(0.2, 0, 0, -0.2, 0))
    return roadmark


def std_roadmark_solid_broken():
    roadmark = RoadMark(RoadMarkType.solid_broken)
    roadmark.add_specific_road_line(RoadLine(0.2, 0, 0, 0.2, 0))
    roadmark.add_specific_road_line(RoadLine(0.2, 3, 3, -0.2, 0))
    return roadmark


def std_roadmark_broken_solid():
    roadmark = RoadMark(RoadMarkType.broken_solid)
    roadmark.add_specific_road_line(RoadLine(0.2, 0, 0, -0.2, 0))
    roadmark.add_specific_road_line(RoadLine(0.2, 3, 3, 0.2, 0))
    return roadmark


STD_ROADMARK_SOLID = std_roadmark_broken()
STD_ROADMARK_BROKEN = std_roadmark_broken()
STD_ROADMARK_BROKEN_TIGHT = std_roadmark_broken_tight()
STD_ROADMARK_BROKEN_BROKEN = std_roadmark_broken_broken()
STD_ROADMARK_SOLID_SOLID = std_roadmark_solid_solid()
STD_ROADMARK_SOLID_BROKEN = std_roadmark_solid_broken()
STD_ROADMARK_BROKEN_SOLID = std_roadmark_broken_solid()


STD_START_CLOTH = 1 / 1000000000


def standard_lane(offset=3, rm=std_roadmark_broken()):
    """standard_lane creates a simple lane with an offset an a roadmark

    Parameters
    ----------
        offset (int): width of the lane
            default: 3

        rm (RoadMark): road mark used for the standard lane
            default:  RoadMark(STD_ROADMARK_BROKEN)
    Returns
    -------
        lane (Lane): the lane

    """
    lc = Lane(a=offset)
    lc.add_roadmark(rm)
    return lc


def create_lanes_merge_split(
    right_lane_def,
    left_lane_def,
    road_length,
    center_road_mark,
    lane_width,
    lane_width_end,
):
    """create_lanes_merge_split is a generator that will create the Lanes of a road road that can contain one or more lane merges/splits
    This is a simple implementation and has some constraints:
     - left and right merges has to be at the same place (or one per lane), TODO: will be fixed with the singleSide attribute later on.
     - the change will be a 3 degree polynomial with the derivative 0 on both start and end.

    Please note that the merges/splits are defined in the road direction, NOT the driving direction.

    Parameters
    ----------
        right_lane_def (list of LaneDef, or an int): a list of the splits/merges that are wanted on the right side of the road, if int constant number of lanes

        left_lane_def (list of LaneDef, or an int): a list of the splits/merges that are wanted on the left side of the road, if int constant number of lanes.

        road_length (float): the full length of the road

        center_road_mark (RoadMark): roadmark for the center line

        lane_width (float): the width of the lanes

        lane_width_end (float): the end width of the lanes

    Return
    ------
        road (Lanes): the lanes of a road
    """

    lanesections = []
    # expand the lane list

    right_lane, left_lane = _create_lane_lists(
        right_lane_def, left_lane_def, road_length, lane_width
    )

    # create the lanesections needed
    for ls in range(len(left_lane)):
        lc = Lane(a=0)
        lc.add_roadmark(copy.deepcopy(center_road_mark))
        lsec = LaneSection(left_lane[ls].s_start, lc)
        # do the right lanes
        for i in range(max(right_lane[ls].n_lanes_start, right_lane[ls].n_lanes_end)):
            # add broken roadmarks for all lanes, except for the outer lane where a solid line is added
            if i == max(right_lane[ls].n_lanes_start, right_lane[ls].n_lanes_end) - 1:
                rm = std_roadmark_solid()
            else:
                rm = std_roadmark_broken()

            # check if the number of lanes should change or not
            if (
                right_lane[ls].n_lanes_start > right_lane[ls].n_lanes_end
                and i == np.abs(right_lane[ls].sub_lane) - 1
            ):
                # lane merge
                coeff = get_coeffs_for_poly3(
                    right_lane[ls].s_end - right_lane[ls].s_start,
                    right_lane[ls].lane_start_widths[i],
                    False,
                    right_lane[ls].lane_end_widths[i],
                )
                rightlane = Lane(a=coeff[0], b=coeff[1], c=coeff[2], d=coeff[3])
                rightlane.add_roadmark(rm)
            elif (
                right_lane[ls].n_lanes_start < right_lane[ls].n_lanes_end
                and i == np.abs(right_lane[ls].sub_lane) - 1
            ):
                # lane split
                coeff = get_coeffs_for_poly3(
                    right_lane[ls].s_end - right_lane[ls].s_start,
                    right_lane[ls].lane_start_widths[i],
                    True,
                    right_lane[ls].lane_end_widths[i],
                )
                rightlane = Lane(a=coeff[0], b=coeff[1], c=coeff[2], d=coeff[3])
                rightlane.add_roadmark(rm)
            elif (lane_width_end is not None) and (lane_width != lane_width_end):
                coeff = get_coeffs_for_poly3(
                    right_lane[ls].s_end - right_lane[ls].s_start,
                    lane_width,
                    False,
                    lane_width_end=lane_width_end,
                )
                rightlane = Lane(a=coeff[0], b=coeff[1], c=coeff[2], d=coeff[3])
                rightlane.add_roadmark(rm)
            elif right_lane[ls].lane_start_widths:
                coeff = get_coeffs_for_poly3(
                    right_lane[ls].s_end - right_lane[ls].s_start,
                    right_lane[ls].lane_start_widths[i],
                    False,
                    lane_width_end=right_lane[ls].lane_end_widths[i],
                )
                rightlane = Lane(a=coeff[0], b=coeff[1], c=coeff[2], d=coeff[3])
                rightlane.add_roadmark(rm)
            else:
                rightlane = standard_lane(lane_width, rm)

            lsec.add_right_lane(rightlane)

        # do the left lanes
        for i in range(max(left_lane[ls].n_lanes_start, left_lane[ls].n_lanes_end)):
            # add broken roadmarks for all lanes, except for the outer lane where a solid line is added
            if i == max(left_lane[ls].n_lanes_start, left_lane[ls].n_lanes_end) - 1:
                rm = std_roadmark_solid()
            else:
                rm = std_roadmark_broken()

            # check if the number of lanes should change or not
            if (
                left_lane[ls].n_lanes_start < left_lane[ls].n_lanes_end
                and i == left_lane[ls].sub_lane - 1
            ):
                # lane split
                coeff = get_coeffs_for_poly3(
                    left_lane[ls].s_end - left_lane[ls].s_start,
                    left_lane[ls].lane_start_widths[i],
                    True,
                    left_lane[ls].lane_end_widths[i],
                )
                leftlane = Lane(a=coeff[0], b=coeff[1], c=coeff[2], d=coeff[3])
                leftlane.add_roadmark(rm)
            elif (
                left_lane[ls].n_lanes_start > left_lane[ls].n_lanes_end
                and i == left_lane[ls].sub_lane - 1
            ):
                # lane merge
                coeff = get_coeffs_for_poly3(
                    left_lane[ls].s_end - left_lane[ls].s_start,
                    left_lane[ls].lane_start_widths[i],
                    False,
                    left_lane[ls].lane_end_widths[i],
                )
                leftlane = Lane(a=coeff[0], b=coeff[1], c=coeff[2], d=coeff[3])
                leftlane.add_roadmark(rm)
            elif (lane_width_end is not None) and (lane_width != lane_width_end):
                coeff = get_coeffs_for_poly3(
                    left_lane[ls].s_end - left_lane[ls].s_start,
                    lane_width,
                    False,
                    lane_width_end=lane_width_end,
                )
                leftlane = Lane(a=coeff[0], b=coeff[1], c=coeff[2], d=coeff[3])
                leftlane.add_roadmark(rm)
            elif left_lane[ls].lane_start_widths:
                coeff = get_coeffs_for_poly3(
                    left_lane[ls].s_end - left_lane[ls].s_start,
                    left_lane[ls].lane_start_widths[i],
                    False,
                    lane_width_end=left_lane[ls].lane_end_widths[i],
                )
                leftlane = Lane(a=coeff[0], b=coeff[1], c=coeff[2], d=coeff[3])
                leftlane.add_roadmark(rm)
            else:
                leftlane = standard_lane(lane_width, rm)

            lsec.add_left_lane(leftlane)

        lanesections.append(lsec)

    # create the lane linker to link the lanes correctly
    lanelinker = LaneLinker()
    for i in range(1, len(right_lane)):
        if right_lane[i].n_lanes_end > right_lane[i].n_lanes_start:
            # lane split
            for j in range(0, right_lane[i - 1].n_lanes_end + 1):
                # adjust for the new lane
                if right_lane[i].sub_lane < -(j + 1):
                    lanelinker.add_link(
                        lanesections[i - 1].rightlanes[j], lanesections[i].rightlanes[j]
                    )
                elif right_lane[i].sub_lane > -(j + 1):
                    lanelinker.add_link(
                        lanesections[i - 1].rightlanes[j - 1],
                        lanesections[i].rightlanes[j],
                    )
        elif right_lane[i - 1].n_lanes_end < right_lane[i - 1].n_lanes_start:
            # lane merge
            for j in range(0, right_lane[i - 1].n_lanes_end + 1):
                # adjust for the lost lane
                if right_lane[i - 1].sub_lane < -(j + 1):
                    lanelinker.add_link(
                        lanesections[i - 1].rightlanes[j], lanesections[i].rightlanes[j]
                    )
                elif right_lane[i - 1].sub_lane > -(j + 1):
                    lanelinker.add_link(
                        lanesections[i - 1].rightlanes[j],
                        lanesections[i].rightlanes[j - 1],
                    )

        else:
            # same number of lanes, just add the links
            for j in range(right_lane[i - 1].n_lanes_end):
                lanelinker.add_link(
                    lanesections[i - 1].rightlanes[j], lanesections[i].rightlanes[j]
                )

    for i in range(1, len(left_lane)):
        if left_lane[i].n_lanes_end > left_lane[i].n_lanes_start:
            # lane split
            for j in range(0, left_lane[i - 1].n_lanes_end + 1):
                # adjust for the new lane
                if left_lane[i].sub_lane < (j + 1):
                    lanelinker.add_link(
                        lanesections[i - 1].leftlanes[j - 1],
                        lanesections[i].leftlanes[j],
                    )
                elif left_lane[i].sub_lane > (j + 1):
                    lanelinker.add_link(
                        lanesections[i - 1].leftlanes[j], lanesections[i].leftlanes[j]
                    )
        elif left_lane[i - 1].n_lanes_end < left_lane[i - 1].n_lanes_start:
            # lane merge
            for j in range(0, left_lane[i - 1].n_lanes_end + 1):
                # adjust for the lost lane
                if left_lane[i - 1].sub_lane < (j + 1):
                    lanelinker.add_link(
                        lanesections[i - 1].leftlanes[j],
                        lanesections[i].leftlanes[j - 1],
                    )
                elif left_lane[i - 1].sub_lane > (j + 1):
                    lanelinker.add_link(
                        lanesections[i - 1].leftlanes[j], lanesections[i].leftlanes[j]
                    )

        else:
            # same number of lanes, just add the links
            for j in range(left_lane[i - 1].n_lanes_end):
                lanelinker.add_link(
                    lanesections[i - 1].leftlanes[j], lanesections[i].leftlanes[j]
                )

    # Add the lanesections to the lanes struct together the lanelinker
    lanes = Lanes()
    for ls in lanesections:
        lanes.add_lanesection(ls, lanelinker)
    return lanes


def create_road(
    geometry,
    id,
    left_lanes=1,
    right_lanes=1,
    road_type=-1,
    center_road_mark=std_roadmark_solid(),
    lane_width=3,
    lane_width_end=None,
):
    """create_road creates a road with one lanesection with different number of lanes, lane marks will be of type broken,
    except the outer lane, that will be solid.
    The lane_width_end parameter can only be used when inputs for left_lanes and right_lanes are int

    Parameters
    ----------
        geometry (Line, Spiral, ParamPoly3, or Arc, or list with these): geometries to build the road

        id (int): id of the new road

        left_lanes (list of LaneDef, or an int): a list of the splits/merges that are wanted on the left side of the road, if int constant number of lanes.
            Default: 1

        right_lanes (list of LaneDef, or an int): a list of the splits/merges that are wanted on the right side of the road, if int constant number of lanes
            Default: 1

        road_type (int): type of road, -1 normal road, otherwise connecting road

        center_road_mark (RoadMark): roadmark for the center line

        lane_width (float): the width of all lanes

        lane_width_end (float): the end width of all lanes

    Returns
    -------
        road (Road): a straight road
    """
    pv = PlanView()
    raw_length = 0
    if isinstance(geometry, list):
        for g in geometry:
            pv.add_geometry(g)
            raw_length += g.length
    else:
        pv.add_geometry(geometry)
        raw_length += geometry.length

    if isinstance(left_lanes, LaneDef):
        left_lanes = [left_lanes]
    if isinstance(right_lanes, LaneDef):
        right_lanes = [right_lanes]

    if (lane_width_end is not None) and (
        (type(left_lanes) != int) or (type(right_lanes) != int)
    ):
        raise RuntimeError(
            "lane_width_end can only be used when left_lanes and right_lanes are int"
        )

    lanes = create_lanes_merge_split(
        right_lanes,
        left_lanes,
        raw_length,
        center_road_mark,
        lane_width,
        lane_width_end=lane_width_end,
    )

    road = Road(id, pv, lanes, road_type=road_type)

    return road


def create_straight_road(road_id, length=100, junction=-1, n_lanes=1, lane_offset=3):
    """creates a standard straight road with two lanes
    STD_ROADMARK_SOLID
        Parameters
        ----------
            road_id (int): id of the road to create

            length (float): length of the road
                default: 100

            junction (int): if the road belongs to a junction or not
                default: -1

            n_lanes (int): number of lanes
                default: 1

            lane_offset (int): width of the road
                default: 3

        Returns
        -------
            road (Road): a straight road
    """
    warn(
        "create_straight_road should not be used anymore, please use the create_road function instead",
        DeprecationWarning,
        2,
    )
    # create geometry
    line1 = Line(length)

    # create planviews
    planview1 = PlanView()
    planview1.add_geometry(line1)

    # create lanesections
    lanesec1 = LaneSection(0, standard_lane())
    for i in range(1, n_lanes + 1, 1):
        lanesec1.add_right_lane(standard_lane(lane_offset))
        lanesec1.add_left_lane(standard_lane(lane_offset))

    # create lanes
    lanes1 = Lanes()
    lanes1.add_lanesection(lanesec1)

    # finally create the roads
    return Road(road_id, planview1, lanes1, road_type=junction)


def create_cloth_arc_cloth(
    arc_curv,
    arc_angle,
    cloth_angle,
    r_id,
    junction=1,
    cloth_start=STD_START_CLOTH,
    n_lanes=1,
    lane_offset=3,
):
    """creates a curved Road  with a Spiral - Arc - Spiral, and two lanes

    Parameters
    ----------
        arc_curv (float): curvature of the arc (and max clothoid of clothoids)

        arc_angle (float): how much of the curv should be the arc

        cloth_angle (float): how much of the curv should be the clothoid (will be doubled since there are two clothoids)

        r_id (int): the id of the road

        junction (int): if the Road belongs to a junction
            default: 1

        cloth_start (float): staring curvature of clothoids

        n_lanes (int): number of lanes
            default: 1

        lane_offset (int): width of the road
            default: 3

    Returns
    -------
        road (Road): a road built up of a Spiral-Arc-Spiral
    """
    warn(
        "create_cloth_arc_cloth should not be used anymore, please use the create_road (see exampels/xodr/clothoid_generation.py) function instead",
        DeprecationWarning,
        2,
    )
    pv = PlanView()
    # adjust sign if angle is negative
    if cloth_angle < 0 and arc_curv > 0:
        cloth_angle = -cloth_angle
        arc_curv = -arc_curv
        cloth_start = -cloth_start
        arc_angle = -arc_angle

    # create geometries
    spiral1 = Spiral(cloth_start, arc_curv, angle=cloth_angle)
    arc = Arc(arc_curv, angle=arc_angle)
    spiral2 = Spiral(arc_curv, cloth_start, angle=cloth_angle)

    pv.add_geometry(spiral1)
    pv.add_geometry(arc)
    pv.add_geometry(spiral2)

    # create lanes
    lsec = LaneSection(0, standard_lane())
    for i in range(1, n_lanes + 1, 1):
        lsec.add_right_lane(standard_lane(lane_offset))
        lsec.add_left_lane(standard_lane(lane_offset))
    lanes = Lanes()
    lanes.add_lanesection(lsec)

    # create road
    return Road(r_id, pv, lanes, road_type=junction)


def create_3cloths(
    cloth1_start,
    cloth1_end,
    cloth1_length,
    cloth2_start,
    cloth2_end,
    cloth2_length,
    cloth3_start,
    cloth3_end,
    cloth3_length,
    r_id,
    junction=1,
    n_lanes=1,
    lane_offset=3,
    road_marks=std_roadmark_broken(),
):
    """creates a curved Road  with a Spiral - Arc - Spiral, and two lanes

    Parameters
    ----------
        cloth1_start (float): initial curvature of spiral 1

        cloth1_end (float): ending curvature of spiral 1

        cloth1_length (float): total length of spiral 1

        cloth2_start (float): initial curvature of spiral 2

        cloth2_end (float): ending curvature of spiral 2

        cloth2_length (float): total length of spiral 2

        cloth3_start (float): initial curvature of spiral 3

        cloth3_end (float): ending curvature of spiral 3

        cloth3_length (float): total length of spiral 3

        r_id (int): the id of the road

        junction (int): if the Road belongs to a junction
            default: 1

        cloth_start (float): staring curvature of clothoids

        n_lanes (int): number of lanes
            default: 1

        lane_offset (int): width of the road
            default: 3

    Returns
    -------
        road (Road): a road built up of a Spiral-Spiral-Spiral
    """
    warn(
        "create_cloth_arc_cloth should not be used anymore, please use the create_road (see exampels/xodr/clothoid_generation.py) function instead",
        DeprecationWarning,
        2,
    )
    pv = PlanView()

    # create geometries
    spiral1 = Spiral(cloth1_start, cloth1_end, length=cloth1_length)
    spiral2 = Spiral(cloth2_start, cloth2_end, length=cloth2_length)
    spiral3 = Spiral(cloth3_start, cloth3_end, length=cloth3_length)

    pv.add_geometry(spiral1)
    pv.add_geometry(spiral2)
    pv.add_geometry(spiral3)

    # create lanes
    center_lane = Lane()
    if road_marks:
        center_lane.add_roadmark(road_marks)
    lsec = LaneSection(0, center_lane)

    for i in range(1, n_lanes + 1, 1):
        rl = Lane(a=lane_offset)
        ll = Lane(a=lane_offset)
        if road_marks:
            rl.add_roadmark(road_marks)
            ll.add_roadmark(road_marks)
        lsec.add_right_lane(rl)
        lsec.add_left_lane(ll)
    lanes = Lanes()
    lanes.add_lanesection(lsec)

    # create road
    return Road(r_id, pv, lanes, road_type=junction)


def get_lanes_offset(road1, road2, contactpoint):
    """returns number of lanes (hp #left lanes = # right lanes) and their offset (hp offset is constant)


    Parameters
    ----------
        road1 (Road): first road

        road2 (Road): second road

    Returns
    -------
        n_lanes (int):

        lane_offset (int):
    """

    # now we always look at lanesection[0] to take the number of lanes
    # TO DO - understand if the roads are connect through end or start and then take the relative lane section
    if contactpoint == ContactPoint.end:
        n_lanesection = 0
    else:
        n_lanesection = -1
    if len(road1.lanes.lanesections[n_lanesection].leftlanes) == len(
        road2.lanes.lanesections[0].leftlanes
    ) and len(road1.lanes.lanesections[n_lanesection].rightlanes) == len(
        road2.lanes.lanesections[0].rightlanes
    ):
        n_lanes = len(road1.lanes.lanesections[n_lanesection].leftlanes)
        lane_offset = road1.lanes.lanesections[n_lanesection].leftlanes[0].widths[0].a
    else:
        raise NotSameAmountOfLanesError(
            "Incoming road ",
            road1.id,
            " and outcoming road ",
            road2.id,
            "do not have the same number of left lanes.",
        )

    return n_lanes, lane_offset


def create_junction_roads_standalone(
    angles,
    r,
    junction=1,
    spiral_part=1 / 3,
    arc_part=1 / 3,
    startnum=100,
    n_lanes=1,
    lane_width=3,
):
    """creates all needed roads for some simple junctions, the curved parts of the junction are created as a spiral-arc-spiral combo
    - 3way crossings (either a T junction, or 120 deg junction)
    - 4way crossing (all 90 degree turns)
    NOTE: this will not generate any links or add any successor/predecessors to the roads, and has to be added manually,
    if you have the connecting roads please use create_junction_roads

    Parameters
    ----------

        angles (list of float): the angles from where the roads should be coming in (see description for what is supported),
                                to be defined in mathimatically positive order, beginning with the first incoming road

        r (float): the radius of the arcs in the junction (will determine the size of the junction)

        junction (int): the id of the junction
            default: 1

        spiral_part (float): the part of the curve that should be spirals (two of these) spiral_part*2 + arcpart = angle of the turn
            default: (1/3)

        arc_part (float): the part of the curve that should be an arc:  spiral_part*2 + arcpart = angle of the turn
            default: (1/3)

        startnum (int): start number of the roads in the junctions (will increase with 1 for each road)

        n_lanes (int): the number of lanes in the junction

        lane_width (float): the lane width of the lanes in the junction
    Returns
    -------
        junction_roads (list of Road): a list of all roads in a junction without connections added

    """
    warn(
        "create_junction_roads_standalone should not be used anymore, please use the CommonJunctionCreator function instead",
        DeprecationWarning,
        2,
    )
    angle = np.pi / 2
    angle_cloth = angle * spiral_part
    spiral_length = 2 * abs(angle_cloth * r)

    cloth = pcloth.Clothoid.StandardParams(
        0,
        0,
        0,
        STD_START_CLOTH,
        (1 / r - STD_START_CLOTH) / spiral_length,
        spiral_length,
    )

    X0 = cloth.XEnd - r * np.sin(angle_cloth)
    Y0 = cloth.YEnd - r * (1 - np.cos(angle_cloth))
    linelength = 2 * (X0 + r + Y0)

    junction_roads = []

    for i in range(len(angles) - 1):
        for j in range(1 + i, len(angles)):
            # check angle needed for junction
            an = np.sign(angles[j] - angles[i] - np.pi)
            an1 = angles[j] - angles[i] - np.pi
            angle_arc = an1 * arc_part

            angle_cloth = an1 * spiral_part

            # adjust angle if multiple of pi
            if an1 > np.pi:
                an1 = -(2 * np.pi - an1)

            # create road, either straight or curved
            if an == 0:
                tmp_junc = create_straight_road(
                    startnum,
                    length=linelength,
                    junction=junction,
                    n_lanes=n_lanes,
                    lane_offset=lane_width,
                )
            else:
                tmp_junc = create_cloth_arc_cloth(
                    1 / r,
                    angle_arc,
                    angle_cloth,
                    startnum,
                    junction,
                    n_lanes=n_lanes,
                    lane_offset=lane_width,
                )

            # add predecessor and successor
            startnum += 1
            junction_roads.append(tmp_junc)

    return junction_roads


def create_junction_roads_from_arc(
    roads, angles, r=0, junction=1, arc_part=1 / 3, startnum=100
):
    """creates all needed roads for some simple junctions, the curved parts of the junction are created as a spiral-arc-spiral combo
    Supported junctions:
    - 3way crossings (either a T junction, or 120 deg junction)
    - 4way crossing (all 90 degree turns)

    Parameters
    ----------
        roads (list of Road): all roads that should go into the junction

        angles (list of float): the angles from where the roads should be coming in (see description for what is supported),
                                to be defined in mathimatically positive order, beginning with the first incoming road [0, +2pi]

        r (float): the radius of the arcs in the junction (will determine the size of the junction)

        junction (int): the id of the junction
            default: 1

        spiral_part (float): the part of the curve that should be spirals (two of these) spiral_part*2 + arcpart = angle of the turn
            default: (1/3)

        arc_part (float): the part of the curve that should be an arc:  spiral_part*2 + arcpart = angle of the turn
            default: (1/3)

        startnum (int): start number of the roads in the junctions (will increase with 1 for each road)

    Returns
    -------
        junction_roads (list of Road): a list of all roads needed for all traffic connecting the roads
    """
    warn(
        "create_junction_roads_from_arc should not be used anymore, please use the CommonJunctionCreator function instead",
        DeprecationWarning,
        2,
    )
    # arc_part = 1 - 2*spiral_part
    spiral_part = (1 - arc_part) / 2

    angle = np.pi / 2
    angle_cloth = angle * spiral_part
    spiral_length = 2 * abs(angle_cloth * r)

    cloth = pcloth.Clothoid.StandardParams(
        0,
        0,
        0,
        STD_START_CLOTH,
        (1 / r - STD_START_CLOTH) / spiral_length,
        spiral_length,
    )

    X0 = cloth.XEnd - r * np.sin(angle_cloth)
    Y0 = cloth.YEnd - r * (1 - np.cos(angle_cloth))

    linelength = 2 * (X0 + r + Y0)

    junction_roads = []

    # loop over the roads to get all possible combinations of connecting roads
    for i in range(len(roads) - 1):
        # for now the first road is place as base,
        if i == 0:
            cp = ContactPoint.end
            roads[i].add_successor(ElementType.junction, junction)
        else:
            cp = ContactPoint.start
            roads[i].add_predecessor(ElementType.junction, junction)

        for j in range(1 + i, len(roads)):
            # check angle needed for junction [-pi, +pi]
            an1 = angles[j] - angles[i] - np.pi
            # adjust angle if multiple of pi
            if an1 > np.pi:
                an1 = -(2 * np.pi - an1)

            angle_arc = an1 * arc_part
            angle_cloth = an1 * spiral_part

            sig = np.sign(an1)

            # create road, either straight or curved
            n_lanes, lanes_offset = get_lanes_offset(roads[i], roads[j], cp)
            if sig == 0:
                # create straight road
                tmp_junc = create_straight_road(
                    startnum,
                    length=linelength,
                    junction=junction,
                    n_lanes=n_lanes,
                    lane_offset=lanes_offset,
                )
            else:
                # create the cloth-arc-cloth road given the radius fo the arc
                tmp_junc = create_cloth_arc_cloth(
                    1 / r,
                    angle_arc,
                    angle_cloth,
                    startnum,
                    junction,
                    n_lanes=n_lanes,
                    lane_offset=lanes_offset,
                )

            # add predecessor and successor
            tmp_junc.add_predecessor(ElementType.road, roads[i].id, cp)
            tmp_junc.add_successor(ElementType.road, roads[j].id, ContactPoint.start)
            startnum += 1
            junction_roads.append(tmp_junc)

    # add junction to the last road aswell since it's not part of the loop
    roads[-1].add_predecessor(ElementType.junction, junction)

    return junction_roads


def create_junction_roads(
    roads,
    angles,
    R,
    junction=1,
    arc_part=1 / 3,
    startnum=100,
    inner_road_marks=None,
    outer_road_marks=std_roadmark_solid(),
):
    """creates all needed roads for some simple junctions, the curved parts of the junction are created as a spiral-arc-spiral combo
    R is value to the the radius of the whole junction (meaning R = distance between the center of the junction and any external road attached to the junction)
    Supportes all angles and number of roads.

    Parameters
    ----------
        roads (list of Road): all roads that should go into the junction

        angles (list of float): the angles from where the roads should be coming in (see description for what is supported),
                                to be defined in mathimatically positive order, beginning with the first incoming road [0, +2pi]

        R (list of float): the radius of the whole junction, meaning the distance between roads and the center of the junction. If only one value is specified, then all roads will have the same distance.

        junction (int): the id of the junction
            default: 1

        spiral_part (float): the part of the curve that should be spirals (two of these) spiral_part*2 + arcpart = angle of the turn
            default: (1/3)

        startnum (int): start number of the roads in the junctions (will increase with 1 for each road)
            default: 100

        inner_road_marks (RoadMark): the RoadMark that all lanes inside the junction will have (outer will be solid)
            Default: None

        outer_road_marks (RoadMark): the roadmark that will be on the edge of the connecting roads (limit the junction)
            Default: STD_ROADMARK_SOLID
    Returns
    -------
        junction_roads (list of Road): a list of all roads needed for all traffic connecting the roads
    """
    warn(
        "create_junction_roads_from_arc should not be used anymore, please use the CommonJunctionCreator function instead",
        DeprecationWarning,
        2,
    )
    if len(roads) is not len(angles):
        raise GeneralIssueInputArguments("roads and angles do not have the same size.")

    if len(R) == 1:
        R = R * np.ones(len(roads))
    elif len(R) > 1 and len(R) is not len(roads):
        raise GeneralIssueInputArguments("roads and R do not have the same size.")

    # linelength = 2*R
    junction_roads = []

    # loop over the roads to get all possible combinations of connecting roads
    for i in range(len(roads) - 1):
        # for now the first road is place as base,
        if i == 0:
            cp = ContactPoint.end
            roads[i].add_successor(ElementType.junction, junction)
        else:
            cp = ContactPoint.start
            roads[i].add_predecessor(ElementType.junction, junction)

        for j in range(1 + i, len(roads)):
            # check angle needed for junction [-pi, +pi]
            an1 = angles[j] - angles[i] - np.pi
            # adjust angle if multiple of pi
            if an1 > np.pi:
                an1 = -(2 * np.pi - an1)

            sig = np.sign(an1)

            # create road, either straight or curved
            n_lanes, lanes_offset = get_lanes_offset(roads[i], roads[j], cp)
            if sig == 0:
                # create straight road
                linelength = R[i] + R[j]
                tmp_junc = create_straight_road(
                    startnum,
                    length=linelength,
                    junction=junction,
                    n_lanes=n_lanes,
                    lane_offset=lanes_offset,
                )
                if inner_road_marks:
                    for l in tmp_junc.lanes.lanesections[0].leftlanes:
                        l.roadmark[0] = inner_road_marks
                    for r in tmp_junc.lanes.lanesections[0].rightlanes:
                        r.roadmark[0] = inner_road_marks
                    tmp_junc.lanes.lanesections[0].centerlane.roadmark[
                        0
                    ] = inner_road_marks
                if len(roads) == 3:
                    # not sure all will be needed since angles have to be in increasing order, but it "should work"
                    k = [x for x in [0, 1, 2] if x != j and x != i][0]
                    if (angles[i] > angles[j]) and (
                        (angles[k] > angles[j]) or (angles[k] < angles[i])
                    ):
                        tmp_junc.lanes.lanesections[0].rightlanes[-1].roadmark[
                            0
                        ] = outer_road_marks
                    elif (angles[i] < angles[j]) and (
                        (angles[k] > angles[j]) or (angles[k] < angles[i])
                    ):
                        tmp_junc.lanes.lanesections[0].rightlanes[-1].roadmark[
                            0
                        ] = outer_road_marks
                    elif (angles[i] < angles[j]) and (
                        (angles[k] < angles[j]) or (angles[k] > angles[i])
                    ):
                        tmp_junc.lanes.lanesections[0].leftlanes[-1].roadmark[
                            0
                        ] = outer_road_marks
                    else:
                        tmp_junc.lanes.lanesections[0].rightlanes[-1].roadmark[
                            0
                        ] = outer_road_marks
            else:
                clothoids = pcloth.SolveG2(
                    -R[i],
                    0,
                    0,
                    STD_START_CLOTH,
                    R[j] * np.cos(an1),
                    R[j] * np.sin(an1),
                    an1,
                    STD_START_CLOTH,
                )
                tmp_junc = create_3cloths(
                    clothoids[0].KappaStart,
                    clothoids[0].KappaEnd,
                    clothoids[0].length,
                    clothoids[1].KappaStart,
                    clothoids[1].KappaEnd,
                    clothoids[1].length,
                    clothoids[2].KappaStart,
                    clothoids[2].KappaEnd,
                    clothoids[2].length,
                    startnum,
                    junction,
                    n_lanes=n_lanes,
                    lane_offset=lanes_offset,
                    road_marks=inner_road_marks,
                )

                if tmp_junc.planview._raw_geometries[1].curvstart > 0:
                    tmp_junc.lanes.lanesections[0].leftlanes[-1].add_roadmark(
                        outer_road_marks
                    )
                if tmp_junc.planview._raw_geometries[1].curvstart < 0:
                    tmp_junc.lanes.lanesections[0].rightlanes[-1].add_roadmark(
                        outer_road_marks
                    )
            # add predecessor and successor
            tmp_junc.add_predecessor(ElementType.road, roads[i].id, cp)
            tmp_junc.add_successor(ElementType.road, roads[j].id, ContactPoint.start)
            startnum += 1
            junction_roads.append(tmp_junc)

    # add junction to the last road aswell since it's not part of the loop
    roads[-1].add_predecessor(ElementType.junction, junction)

    return junction_roads


def _create_junction_links(
    connection, nlanes, r_or_l, sign, from_offset=0, to_offset=0
):
    """helper function to create junction links

    Parameters
    ----------
        connection (Connection): the connection to fill

        nlanes (int): number of lanes

        r_or_l (1 or -1): if the lane should start from -1 or 1

        sign (1 or -1): if the sign should change

        from_offset (int): if there is an offset in the beginning
            Default: 0

        to_offset (int): if there is an offset in the end of the road
            Default: 0
    """
    for i in range(1, nlanes + 1, 1):
        connection.add_lanelink(r_or_l * i + from_offset, r_or_l * sign * i + to_offset)


def create_junction(junction_roads, id, roads, name="my junction"):
    """create_junction creates the junction struct for a set of roads


    Parameters
    ----------
        junction_roads (list of Road): all connecting roads in the junction

        id (int): the id of the junction

        roads (list of Road): all incomming roads to the junction

        name(str): name of the junction
        default: 'my junction'

    Returns
    -------
        junction (Junction): the junction struct ready to use

    """

    junc = Junction(name, id)

    for jr in junction_roads:
        # handle succesor lanes
        conne1 = Connection(jr.successor.element_id, jr.id, ContactPoint.end)
        _, sign, _ = _get_related_lanesection(
            jr, get_road_by_id(roads, jr.successor.element_id)
        )

        _create_junction_links(
            conne1,
            len(jr.lanes.lanesections[-1].rightlanes),
            -1,
            sign,
            to_offset=jr.lane_offset_suc[str(jr.successor.element_id)],
        )
        _create_junction_links(
            conne1,
            len(jr.lanes.lanesections[-1].leftlanes),
            1,
            sign,
            to_offset=jr.lane_offset_suc[str(jr.successor.element_id)],
        )
        junc.add_connection(conne1)

        # handle predecessor lanes
        conne2 = Connection(jr.predecessor.element_id, jr.id, ContactPoint.start)
        _, sign, _ = _get_related_lanesection(
            jr, get_road_by_id(roads, jr.predecessor.element_id)
        )
        _create_junction_links(
            conne2,
            len(jr.lanes.lanesections[0].rightlanes),
            -1,
            sign,
            from_offset=jr.lane_offset_pred[str(jr.predecessor.element_id)],
        )
        _create_junction_links(
            conne2,
            len(jr.lanes.lanesections[0].leftlanes),
            1,
            sign,
            from_offset=jr.lane_offset_pred[str(jr.predecessor.element_id)],
        )
        junc.add_connection(conne2)
    return junc


def create_direct_junction(roads, id, name="my direct junction"):
    """create_direct_junction creates the junction struct for a set of roads, for a direct junction

    Parameters
    ----------
        roads (list of Road): all roads that are building up the direct junction

        id (int): the id of the junction

        name(str): name of the junction
        default: 'my direct junction'

    Returns
    -------
        junction (Junction): the junction struct ready to use

    """
    raise RemovedFunctionality(
        "The create_direct_junction has been removed, due to its very limited functionality, please try the xodr.DirectJunctionCreator instead."
    )


def get_road_by_id(roads, id):
    """get_road_by_id returns a road based on the road id

    Parameters
    ----------
        roads (list of Roads): a list of roads to seach through

        id (int): the id of the road wanted

    Returns
    -------
        Road
    """
    for r in roads:
        if r.id == id:
            return r


class LaneDef:
    """LaneDef is used to help create a lane merge or split. Can handle one lane merging or spliting.

    NOTE: This is not part of the OpenDRIVE standard, but a helper for the xodr module.

    Parameters
    ----------
        s_start (float): s coordinate of the start of the change

        s_end (float): s coordinate of the end of the change

        n_lanes_start (int): number of lanes at s_start

        n_lanes_end (int): number of lanes at s_end

        sub_lane (int): the lane that should be created (split) or removed (merge)

        lane_start_widths (list of float): widths of lanes at start, must be [] or same length as n_lanes_start
            Default: []

        lane_end_widths (list of float): widths of lanes at end, must be [] or same length as n_lanes_end
            Default: same as lane_start_widths

    Attributes
    ----------
        s_start (float): s coordinate of the start of the change

        s_end (float): s coordinate of the end of the change

        n_lanes_start (int): number of lanes at s_start

        n_lanes_end (int): number of lanes at s_end

        sub_lane (int): the lane that should be created (split) or removed (merge)

        lane_start_widths (list of float): widths of lanes at start, must be [] or same length as n_lanes_start

        lane_end_widths (list of float): widths of lanes at end, must be [] or same length as n_lanes_end
    """

    def __init__(
        self,
        s_start,
        s_end,
        n_lanes_start,
        n_lanes_end,
        sub_lane=None,
        lane_start_widths=[],
        lane_end_widths=[],
    ):
        self.s_start = s_start
        self.s_end = s_end
        self.n_lanes_start = n_lanes_start
        self.n_lanes_end = n_lanes_end
        self.sub_lane = sub_lane
        self.lane_start_widths = lane_start_widths
        if lane_end_widths == []:
            self.lane_end_widths = self.lane_start_widths.copy()
        else:
            self.lane_end_widths = lane_end_widths

    def _adjust_lane_widths(self):
        if self.sub_lane:
            if self.lane_end_widths and len(self.lane_end_widths) < self.n_lanes_start:
                # mergeo
                self.lane_end_widths.insert(abs(self.sub_lane) - 1, 0)
            elif (
                self.lane_start_widths
                and len(self.lane_start_widths) < self.n_lanes_end
            ):
                # split
                self.lane_start_widths.insert(abs(self.sub_lane) - 1, 0)
        # TODO: add some checks here?


def _create_lane_lists(right, left, tot_length, default_lane_width):
    """_create_lane_lists is a function used by create_lanes_merge_split to expand the list of LaneDefs to be used to create stuffs

    Parameters
    ----------
        right (list of LaneDef, or int): the list of LaneDef for the right lane

        left (list of LaneDef, or int): the list of LaneDef for the left lane

        tot_length (float): the total length of the road

        default_lane_width (float): lane_width to be used if not defined in LaneDef
    """

    # TODO: implement for left and right lanesection...
    def _check_lane_widths(lane):
        if lane.lane_start_widths == []:
            lane.lane_start_widths = [
                default_lane_width for x in range(lane.n_lanes_start)
            ]
        if lane.lane_end_widths == []:
            lane.lane_end_widths = [default_lane_width for x in range(lane.n_lanes_end)]

    const_right_lanes = None
    const_left_lanes = None

    retlanes_right = []
    retlanes_left = []
    present_s = 0

    r_it = 0
    l_it = 0
    # some primariy checks to handle int instead of LaneDef

    if not isinstance(right, list):
        const_right_lanes = right
        right = []

    if not isinstance(left, list):
        const_left_lanes = left
        left = []

    while present_s < tot_length:
        if r_it < len(right):
            # check if there is still a right LaneDef to be used, and is the next one to add
            if right[r_it].s_start == present_s:
                add_right = True
            else:
                next_right = right[r_it].s_start
                add_right = False
                n_r_lanes = right[r_it].n_lanes_start
        else:
            # no more LaneDefs, just add new right lanes with the const/or last number of lanes
            add_right = False
            next_right = tot_length
            if const_right_lanes or const_right_lanes == 0:
                n_r_lanes = const_right_lanes
            else:
                n_r_lanes = right[-1].n_lanes_end

        if l_it < len(left):
            # check if there is still a left LaneDef to be used, and is the next one to add
            if left[l_it].s_start == present_s:
                add_left = True
            else:
                next_left = left[l_it].s_start
                add_left = False
                n_l_lanes = left[l_it].n_lanes_start
        else:
            # no more LaneDefs, just add new left lanes with the const/or last number of lanes
            add_left = False
            next_left = tot_length
            if const_left_lanes or const_left_lanes == 0:
                n_l_lanes = const_left_lanes
            else:
                n_l_lanes = left[-1].n_lanes_end

        # create and add the requiered LaneDefs
        if not add_left and not add_right:
            # no LaneDefs, just add same amout of lanes
            s_end = min(next_left, next_right)
            if const_right_lanes is not None:
                retlanes_right.append(
                    LaneDef(
                        present_s,
                        s_end,
                        n_r_lanes,
                        n_r_lanes,
                        lane_start_widths=[
                            default_lane_width for x in range(n_r_lanes)
                        ],
                        lane_end_widths=[default_lane_width for x in range(n_r_lanes)],
                    )
                )
            else:
                lane_start_widths = [default_lane_width for x in range(n_r_lanes)]
                lane_end_widths = [default_lane_width for x in range(n_r_lanes)]
                if r_it == len(right):
                    if right[r_it - 1].lane_end_widths:
                        lane_start_widths = right[r_it - 1].lane_end_widths.copy()
                        lane_end_widths = right[r_it - 1].lane_end_widths.copy()
                elif right[r_it].lane_start_widths:
                    lane_start_widths = right[r_it].lane_start_widths.copy()
                    lane_end_widths = right[r_it].lane_start_widths.copy()
                retlanes_right.append(
                    LaneDef(
                        present_s,
                        s_end,
                        n_r_lanes,
                        n_r_lanes,
                        lane_start_widths=lane_start_widths,
                        lane_end_widths=lane_end_widths,
                    )
                )
            if const_left_lanes is not None:
                retlanes_left.append(
                    LaneDef(
                        present_s,
                        s_end,
                        n_l_lanes,
                        n_l_lanes,
                        lane_start_widths=[
                            default_lane_width for x in range(n_l_lanes)
                        ],
                        lane_end_widths=[default_lane_width for x in range(n_l_lanes)],
                    )
                )
            else:
                lane_start_widths = [default_lane_width for x in range(n_l_lanes)]
                lane_end_widths = [default_lane_width for x in range(n_l_lanes)]
                if l_it == len(left):
                    if left[l_it - 1].lane_end_widths:
                        lane_start_widths = left[l_it - 1].lane_end_widths.copy()
                        lane_end_widths = left[l_it - 1].lane_end_widths.copy()
                elif left[l_it].lane_start_widths:
                    lane_start_widths = left[l_it].lane_start_widths.copy()
                    lane_end_widths = left[l_it].lane_start_widths.copy()

                retlanes_left.append(
                    LaneDef(
                        present_s,
                        s_end,
                        n_l_lanes,
                        n_l_lanes,
                        lane_start_widths=lane_start_widths,
                        lane_end_widths=lane_end_widths,
                    )
                )

            present_s = s_end
        elif add_left and add_right:
            # Both have changes in the amount of lanes,
            _check_lane_widths(left[l_it])
            _check_lane_widths(right[r_it])
            retlanes_left.append(left[l_it])
            retlanes_right.append(right[r_it])
            present_s = left[l_it].s_end
            r_it += 1
            l_it += 1
        elif add_right:
            # only the right lane changes the amount of lanes, and add a LaneDef with the same amount of lanes to the left
            _check_lane_widths(right[r_it])
            retlanes_right.append(right[r_it])
            retlanes_left.append(
                LaneDef(
                    present_s,
                    right[r_it].s_end,
                    n_l_lanes,
                    n_l_lanes,
                    lane_start_widths=[default_lane_width for x in range(n_l_lanes)],
                    lane_end_widths=[default_lane_width for x in range(n_l_lanes)],
                )
            )
            present_s = right[r_it].s_end
            r_it += 1
        elif add_left:
            # only the left lane changes the amount of lanes, and add a LaneDef with the same amount of lanes to the right
            _check_lane_widths(left[l_it])
            retlanes_left.append(left[l_it])
            retlanes_right.append(
                LaneDef(
                    present_s,
                    left[l_it].s_end,
                    n_r_lanes,
                    n_r_lanes,
                    lane_start_widths=[default_lane_width for x in range(n_r_lanes)],
                    lane_end_widths=[default_lane_width for x in range(n_r_lanes)],
                )
            )
            present_s = left[l_it].s_end
            l_it += 1
    [x._adjust_lane_widths() for x in retlanes_right]
    [x._adjust_lane_widths() for x in retlanes_left]
    return retlanes_right, retlanes_left


def get_coeffs_for_poly3(length, lane_offset, zero_start, lane_width_end=None):
    """get_coeffs_for_poly3 creates the coefficients for a third degree polynomial, can be used for all kinds of descriptions in xodr.

    Assuming that the derivative is 0 at the start and end of the segment.

    Parameters
    ----------
        length (float): length of the segment in the s direction

        lane_offset (float): the lane offset (width) of the lane

        zero_start (bool): True; start with zero and ends with lane_offset width,
                           False; start with lane_offset and ends with zero width

        lane_width_end (float): specify the ending lane width for lanes that may start
                                and end with different widths

    Return
    ------
        coefficients (float,float,float,float): polynomial coefficients corresponding to "a, b, c, d" in the OpenDrive polynomials
    """
    # might be expanded for other cases, not now if needed yet though
    start_heading = 0
    end_heading = 0
    s0 = 0
    s1 = length

    # create the linear system
    A = np.array(
        [
            [0, 1, 2 * s0, 3 * s0**2],
            [0, 1, 2 * s1, 3 * s1**2],
            [1, s0, s0**2, s0**3],
            [1, s1, s1**2, s1**3],
        ]
    )
    if zero_start:
        B = [start_heading, end_heading, 0, lane_offset]
    else:
        B = [start_heading, end_heading, lane_offset, 0]

    if lane_width_end is not None:
        B = [start_heading, end_heading, lane_offset, lane_width_end]

    # calculate and return the coefficients
    return np.linalg.solve(A, B)
