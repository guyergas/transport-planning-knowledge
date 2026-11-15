=== PAGE 1 === [ocr; layer=garbled; image; conf=86]
מינהל תכנון >
ופי (0)‏ יתוח תשת ופיתוח תשתיות.
אגף בכיר תכנון תחבורתי an un‏
Appendix 1
To the Procedure for Approval of Traffic
Signal Planning Software (TSPS)
The Ministry of Transport's
Requirements for
Traffic Signal Planning Software
Fourth Edition
January 2026
TUR 3
המינהלת לתכנון תחבורתי
של כושרד התחבורה

=== PAGE 2 === [ocr; layer=garbled; conf=81]
Table of contents
Chapter page
1.General 111117 1 ה‎ 3
2. The Purpose of the DOCUMENL ייייייייייייייייייייייייייייייייייייייייייייייייייי בשש‎ 4
3. Definitions es 4
4. Accompanying DOCUMENTS יייייייייוייייייייייייוייייייייייייייייויייייייייייייייייייייי ששב‎ 4
5. Compliance with the Requirement for Maturity of the Software and the Software
Supplier.
6. Compliance with Support and Maintenance Requirements...
7. Compliance with the Software Approval Process, Maintaining the Validity of the
Approval and Backward Compatibility................c.c..... 5
8. Threshold requirements of the planning software יייייייייייייייייייייי שעג‎ 6
9. Supportive requirements
10. List of Files and Documents for submission
Supplement A to Appendix 1: List of Cases for Inter-Green Calculation Verification. 15
Supplement B to Appendix 1: Intersection 1 (for Submission for Inspection) —
Intersection Properties.
Supplement C to Appendix 1: List of tests for the software (TSPS) Supplier and
ה א או ה‎ 8
Supplement D to Appendix 1: Unified Format Requirements בשש‎ 44
Supplement E to Appendix 1:  Inter-Green Times and Vehicle Two Optical Units......48
49 ייייייויוייייייייייייויויויויויויויויויויייליליטידידידידידידיויויויי ה הכה ה ה ה | Versions Control‏
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 3 === [ocr; layer=garbled; conf=96]
1. General
This document was updated in accordance with the requirements of the Guidelines
of Traffic Signal Design (Ministry of Transport, 2025), hereinafter: “MOT Guidelines of
Traffic Signal Design” or “MOT Guidelines”.
This document constitutes Appendix 1 to the Procedure for Approval of Traffic Signal
Planning Software (TSPS) in Israel. The document defines the Threshold Requirements and
Supportive Requirements for the Traffic Signal Planning Software (hereinafter "Software" /
"Planning Software" / "TSPS") which complies with the Ministry of Transport's requirements
detailed in this document.
The threshold requirements which are defined in this document constitute minimum
requirements. Customers who execute a process of planning software acquisition and/or
authorities which instruct on the use of planning software are entitled to add requirements.
The needs of the Ministry of Transport and the traffic authorities in Israel vary and are
updated from time to time. These changes also necessitate consistently updating planning
software capabilities. The ability to guarantee stability, availability and commitment in order
to enable reliance on traffic signal programs and their maintenance over time is required
from the planning software supplier. Therefore, in addition to the requirements for planning
software, threshold requirements of the suppliers of the software will be defined as will
requirements for commitment to support and provide version updates.
The Ministry of Transport will carry out processes for the initial approval and the ongoing
approval of the Traffic Signal Planning Software.
Two types of requirements will be defined for the software.
* A mandatory requirement (threshold requirement) — noncompliance with the
requirement will disqualify the planning software from use as planning software in
Israel.
« A supportive requirement — A requirement that supports the ability of software users
to comply with the Ministry of Transport instructions for planning traffic signal
programs. As part of the planning software approval process, the compliance of the
planning software with the supportive requirements will be examined and
documented. Documentation of the level of compliance with the requirements will
help the interested parties in the acquisition process and the use of the planning
software.
It is the responsibility of the software purchasers to ensure that they have the ability
to furnish the Ministry of Transport with traffic signal programs that comply with the
Ministry of Transport's guidelines for traffic signal planning and the manner of
submitting traffic signal programs, all of which should be produced through the
planning software that they have acquired.
The responsibility to ensure that the traffic signal program complies with the MOT
Guidelines of Traffic Signal Design (in addition to the safety guidelines specified as
a mandatory requirement) rests upon the designer only.
The variations of this version compared to previous versions are detailed in the
Versions Control Table, at the end of this Appendix.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 4 === [ocr; layer=garbled; conf=95]
Note: The terms Software / Planning Software / 1505 are used interchangeably in
this document, and have the same meaning.
2. The Purpose of the Document
a. To define the Requirements from the Software Supplier, and the Threshold
Requirements for approval of the Traffic Signal Planning Software (TSPS), as
authorized for planning traffic signal programs in the State of Israel.
b. To define the supportive optional requirements demanded of the planning software
for support in the process of planning and testing of the traffic signal programs in
Israel.
6. To define the examination processes of approval for traffic signal planning software
for use in traffic signal planning in Israel.
3. Definitions
a. The traffic signal planning software (TSPS)- software through which it is possible
to plan traffic signal programs.
b. Unified format —An XML (XSD) template, defined and distributed by the Ministry of
Transport, which defines the structure of the traffic signal program on the basis of
which, it is possible to export a traffic signal program.
6. Aunified file - a traffic signal program, which is presented in accordance with the
unified format.
d. Adjacent Signal Groups— Two (or more) Signal Groups for vehicles coming from
the same approach, each controlling different movements (vehicles traveling in
different directions).
e. Skeleton - All possible combinations of Stage / Signal groups’ sequences, having
minimum green, starting and ending with the main stage, according to the flow
chart possibilities.
f. Vehicle 3 Optical Units (Vehicle 3 OU) - Vehicle Signal Group, based on 3 optical
units, that display the signal: red, red-yellow, green (flashing green), yellow.
g. Vehicle 2 Optical Units (Vehicle 2 OU) - Vehicle Signal Group, based on 2 optical
units, that display the signal: red, flashing yellow, yellow. This Signal Group is
currently not approved by the Ministray of Transport (MOT). This Signal Group will
be incorporated in the TSPS, however it will become valid only after it is approved
as part of the MOT Guidelines of Traffic Signal Design.
4. Accompanying Documents
a. Unified Format Definition Document (XSD File).
b. MOT Guidelines of Traffic Signal Design, Ministry of Transport, June 2025.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 5 === [ocr; layer=garbled; conf=96]
5. Compliance with the Requirement for Maturity of the
Software and the Software Supplier
a) The software supplier must have at least 3 years of experience as a software
house in developing the software examined at the time of the examination, which
will be calculated from the date of issue of the first commercial version of the
software.
b) The examined software has been used as software for the planning of traffic signal
programs for at least 50 junctions in which these programs were implemented on
active traffic signals, among them at least 10 junctions with transit priority.
c) The software has been used for planning traffic signal programs for at least 2
customers / authorities during the two years prior to the examination.
6. Compliance with Support and Maintenance
Requirements
a. The software supplier will commit to support the Israeli version continuously and
must allocate the necessary resources for updating the versions as part of the
conditions for maintaining the validity of the approval.
b. The software supplier's declaration of suspending support for the Israeli software
version could result in the immediate suspension of the approval.
7. Compliance with the Software Approval Process,
Maintaining the Validity of the Approval and Backward
Compatibility
a. The software approval process and maintaining the validity of the approval is
described in the "Traffic-Signal Planning Software approval procedure”
b. The supplier of planning software must submit the files and documents as described
in Section 10 of this document.
c. The version of the software to be submitted for examination by the Ministry of
Transport must not have any limitations of operation or licensing limitations. All the
necessary security measures enabling the operation of the software must be
provided in full to the Ministry of Transport without any time or operating limitations.
d. Should the software require any additional software components, said components
shall be supplied in full in the suitable version for use in the planning software version
that was submitted for examination.
e. Planning software must be submitted for examination in the most advanced
operating system version supported by the software.
f. New versions of the software are required to be backwards compatible with the
capabilities of previous versions and shall support plans made using previous
versions, unless the MOT has given its approval for the cessation of compatibility.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 6 === [ocr; layer=garbled; conf=95]
8. Threshold requirements of the planning software
a. Unified Format File:
In order to enable the Ministry of Transport to independently examine the traffic
signal planning, and in order to assist in the import of the traffic signal plans to
Traffic Control Centers, the unified format was defined according to which the
traffic signal programming software is required to export the traffic signal programs
using this format.
The minimum requirements for the Unified Format are defined in Supplement D to
Appendix 1, and supersede any previous requirements of this matter.
Export to a Unified Format:
I. The software must have the ability to export the traffic signal program
plans to the unified format file (hereinafter the "file") as defined in the
unified protocol definition document.
Export to the file must be executed by the software version authorized‏ .ו
by the Ministry of Transport. The software version number must appear‏
in the file.‏
lll. Every mandatory data element required to appear according to the
definitions of the unified format must be exported in the file.
IV. The software must export the Hebrew strings to the file in a manner that
enables their normal presentation and in common/standard fonts.
b. The Calculation of Inter-Green Times:
The calculation of Inter-Green times for Vehicle 3 Optical Units, Pedestrians and
Public Transport must be executed pursuant to the calculation method determined
by the Ministry of Transport as described in Section 5 of the Guidelines for Traffic
Signal Design (MOT, 2025), including all the definitions, values and relevant
calculation formulas. These Inter-Green times shall be embedded in the Inter-
Green Matrix.
The calculation of the Inter-Green times for Vehicle 2 Optical Units shall be
performed as described in the Guidelines for Traffic Signal Design (MOT, 2025),
Section 5 and Appendix N.6. The calculation of these Inter-Green times shall be
included in the Inter-Green times calculation table. However, these times shall not
be embedded in the Inter-Green Matrix. The implementation of these inter-green
times in the Transition Periods shall be ensured.
The translation to English of Section 5 and Appendix N.6 of the Guidelines for
Traffic Signal Design (MOT, 2025) is provided in Supplement E of Appendix 1 (in a
sepratae file).
e The TSPS will prevent Signal Timing-Plan printout or marks the printout, in a very
clear and prominent way, when changes were made to parameters pertaining to
Inter-Green durations, but not all relevant changes to the Traffic-signal plan were
made.
The TSPS prevents Signal Timing-Plan export to Unified-Format and\or download
to controller when changes were made to parameters pertaining to Inter-green
durations but not all relevant changes to the Traffic-signal plan were implemented.
c. Printing:
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 7 === [ocr; layer=garbled; conf=94]
1) The TSPS shall allow printing of the following components:
a. A cover page that includes at least — The name of the junction, the local
authority, the planner, the plan number, allocated space for the local
authority signature, allocated space for the central authority signature (at
least 9 cm wide by 5 cm height), a list of the accompanying documents,
versions and related geometry plans.
b. List of Contents (including page numbers).
c. The Traffic Arrangements Plan of the intersection in a scale of 1:500.
d. A schematic diagram of the intersection produced by the software including
all the traffic signal components entered for the intersection and at the least
the names of the streets, movements and signal groups, lanes, detectors
and pedestrian push buttons.
e. Table of the minimum durations of green for all signal groups.
f. סוסב ה‎ of Inter-Green times calaculation, including entrance and clearance
distances, and parameters for the calculation for all movements, as well as
the resulting mininum inter-green calculation, and the detrerming durations
after rounding off).
gd. An inter-green duration matrix.
h. Description of all the incoming/outgoing signals / pulses (detectors, pulses,
communication with the control center etc.). *
i. Specific functions for the intersection should there be any.
j. Written description of the principles of the traffic signal program *
k. Charts of signal stages.
I. Charts of the transition sequence between stages (optional for printing).
m. A flow chart and logic of the design.
n. Charts of all skeleton sequences.
o. Signal Group Maximum Timing Plan for operation programs, including
programs for police officer to locally control the intersection, other
emergency programs, and statrt-up program.
p. Alist of programs, and time schedule for activation (weekly/annual
schedule).
q. A parameter table pursuant to the list of programs.
r. Scenarios (optional for printing).
« It shall be possible to carry out the requirements described in the clauses
marked with * using an external Software. The TSPS shall allow the addition
of a file (for example in pdf format), which includes the required information,
as part of the signal timing plan that the Software exports / prints.
2) The graphics of the printouts is clear, understandable, and meets standard
industry requirements.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 8 === [ocr; layer=garbled; conf=93]
0. Signals for Traffic Signals in Israel -
1) The software shall guarantee the required sequence and duration of signals, as
defined in the Guidelines for Traffic Signal Design, specifically for each type of
Signal Group.
2) The software shall consider the sequence (order) of the signals while
determining the transitions between stages/signal groups.
3) For every signal, the start time and finish time shall be saved.
Vehicle 3 Optical Units Signal Group
Signal Sequence: red -> red-yellow -> green -> [flashing green] -> yellow
Signal Duration:
«Minimal red signal: 3 seconds.
* Red-yellow signal: 2 seconds.
« Flashing green (for speeds 60 kph and above): 3 seconds.
* Yellow signal: 3 seconds.
Pedestrian without / with Bicycle in Crosswalk Signal Group
Signal Sequence: red -> green
Signal Duration:
«Minimal red signal: 3 seconds.
The signal sequence and duration for bicycles (if exists) shall be identical to those
of pedestrians.
Bicycle 3 Optical Units Signal Group
Bicycle Signal Group, in a lane or a path, that crosses the intersection not in a
Crosswalk.
Signal Sequence: red -> green -> yellow
Signal Duration:
«Minimal red signal: 3 seconds.
* Yellow signal: 3 seconds.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 9 === [ocr; layer=garbled; conf=93]
Public Transport (LRT, BRT) Signal Group
Signal Sequence:
= Stop
. 0
Prepare for moving
צ‎
[J . .. ... Move forward
. . .. ..
000 6480 60 06] 0 0
.
Stop if you can‏ ס
Signal Duration:
«Minimal red signal: 3 seconds.
* Prepare for Moving: 2 seconds.
« Stop if you can: 3 seconds.
Driving Assistance Signal for LRT (DAS) Signal Group
The TSPS shall enable the design of a priority related signal for a LRT with two
different options:
Option 1: A triangle signal displayed in one signal head
« Triangle signal - a flashing signal and a 4 second constant signal. The
flashing signal will begin when one of the priority detectors is activated
(usually the remote detector). This signal will change to a constant signal 4
seconds before the “move forward” signal. The constant signal will end (no
signal) when the “move forward” signal begins.
Option 2: Two different signals (two signal groups) displaed in two signal
heads
* Flashing Rhombus signal — showing the LRT has been identified by the
signal controller. This signal will begin when one of the priority detectors is
activated (usually the remote detector) and shall end 4 seconds before the
“move forward” signal.
* Exclamation Mark signal — showing the LRT is about to receive “move
forward” signal. This signal will begin 4 seconds before the “move forward”
signal (together with the closure of the rhombus signal) and shall end (no
signal) when the “move forward” signal begins.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 10 === [ocr; layer=garbled; conf=95]
Vehicle 2 Optical Units Signal Group
Signal Sequence: red -> flashing yellow -> yellow
Signal Duration:
«Minimal red signal: 3 seconds.
* Yellow signal: 3 seconds.
Note: Vehicle 2 Optical Units Signal Group is not approved at this stage in the
MOT Guidelines for Traffic Signal Design. This Signal Group shall be incorporated
in the TSPS, however, it shall become valid only after its approval as part of the
MOT Guidelines.
Constant flashing yellow signal
Signal Sequence: flashing yellow (during the entire cycle)
Conditional Flashing Yellow
Signal Sequence: dark -> flashing yellow
Remark: The rules for the beginning and ending of the conditional flashing yellow
are detailed in the MOT guidelines.
Start-Up Sequence
The transition from an operation mode where the Traffic Signal is turned-off
(blacked-out), or from a Flashing Yellow mode of all vehicle signals, to a regular
mode of operation of the Traffic Signal, shall be performed in a controlled manner,
and in accordance with the Start-Up plan, as defined in Section 6 of the Guidelines
for Traffic Signal Design.
This plan shall be planned by the Traffic Signal designer, and shall be programmed
in the TSPS, for the particualr planned intersection.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 11 === [ocr; layer=garbled; conf=93]
9. Supportive requirements
In order to enable compliance of the traffic signal program planning with the MOT Guidelines
of Traffic Signal Design, the following capabilities are required. These requirements are not
mandatory as aforementioned, but the Ministry of Transport will examine the software's
compatibility to the requirements and will document the findings in order to enable the
interested parties to consider the suitability of the software to their needs. The required
capabilities are:
a. The names of elements - the ability to define the names of planning elements,
which shall be in accordance with MOT Guidelines for Traffic Signal Design.
« Vehicle signal groups — Numbering staring from 1 (1, 2, 3, 4...)
« Pedestrian signal groups — lowercase letters in English, starting from a, and
optionally adding numbers (a, b, 6, d1...)
* Bicycle signal group - Numbering staring from 50, in addition to the number of
the parallel Vehicle signal group.
«Public Transport signal group, LRT type - Numbering staring from 20.
* Public Transport signal group, other type - Numbering staring from 30, in
addition to the number of the parallel Vehicle signal group.
« Flashing yellow signal group:
o In case of combined green for turning vehicles and pedestrains — Bi, where i
represents the marking of the relevant crosswalk signal group.
o Free right turn — BL for all flashing yellow signal groups, or Bj, where j
represents an English letter in ascending order.
« Driving Assistance Signal for LRT (DAS) Signal Group - P1 for the “rhobus”
and P2 for the “exclamation mark”.
* The names of stages - Alphanumeric uppercase letters in English (A, BA, C1...)
« Vehicle and Public Transport detectors - Alphanumeric uppercase letters and
other characters in English (D1, E3, Q5, DPT12, DPT_1_5, DP1, DL1, etc.)
* Pedestrian and Bicycle pushbuttons - Alphanumeric uppercase and lower case
etters in English (Pa, Pba, Pc1 etc.).
* A simultaneous inspection of all the detectors and pedestrian push buttons -
Dx.
*. Green wave pulses - the letters SY with the addition of numerals (SY, SY1...)
«Pulses — Alphanumeric uppercase and lowercase (fo1, fo2, X1, Y2...).
b. The ability to define the minimum green duration - pursuant to the Ministry of
Transport guidelines which will be used by the software as default minimum values
for a signal group. The software will prevent/alert in case the designer specified
shorter minimum intervals or such interval is obtained during the signal planning
(displays, scenarios, etc.). The minimum green (the default value determined
minimum value per signal group) will be:
« 1 second for a Vehicle 3 Optical Units signal group.
* 6 seconds for Pedestrian signal groups.
* 6 seconds for Bicycle signal groups.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 12 === [ocr; layer=garbled; conf=94]
* 5 seconds for Public Transport (LRT) signal group.
* 6 seconds for Public Transport (not LRT) signal group.
* 6 seconds for Vehicle 2 Optical Units signal group (flashing yellow).
6. The ability of the designer to define the minimum green duration for a signal group/
stage and an alert and/or prevention in the event of deviations. For example:
* 10 seconds for a vehicle on a main road at an intersection located on an
interurban road.
* 2/3 of the required time for a pedestrian to cross the pedestrian crossing.
d. The ability to define the duration of the maximum cycle, in accordancs with the
MOT Guidelines, and an alert and/or prevention in the event of deviations, for
example:
* 120 seconds.
e. Presentation and emphasis of exceptions in Inter-Green times which are longer than
required, when implementing transition sequences.
Conditional Flashing Yellow — ability to define the actication and deactivation rules
of the conditional flashing yellow signal, in accordance with the MOT Guidelines of
Traffic Signal Design, and alert / prevention in case of deviation from these rules.
g. Adjacent signal groups - An alert and/or prevention in an event in which the time
interval between the start of the green, of two adjacent vehicle signal groups is one
second.
h. Presenting a chart of the working flow of the traffic signal - The planning will include
a flowchart that presents the traffic signal's operation. The flowchart will include all
the stages, the possible transitions between the stages and shall enable the
presentation of the conditions for the transitions.
Prevention of skipping a signal group - The software must alert and/or prevent
skipping (unplanned) a signal group in a cycle while there is demand for that signal
group. The signal group may not appear in a cycle, only if the demand for the signal
group has been examined (in all relevant detectors/push-buttons) and found to be
negative, or the planning includes skipping this signal group intentionally.
Printing, with regard to Section 86 of this document:
* The software must enable users to select whether to print the optional sections.
« If a user chooses to print the optional sections and there is no relevant
information that can be printed, the software must print that there is no suitable
information.
« Inthe printing process of the traffic signal plan booklet the possibility shall exist
to select and arrange the sections to be printed. Printing will be executed with
one click, with the possibility of printing each page separately.
« It shall be possible to direct the printout to a PDF file and/or produce a file in
PDF format and print the file.
k. Writing Hebrew Strings:
* The TSPS allows assignment and saving of Hebrew Strings in all text field in
the Software, including intersection names, file names, comments, etc.
* String feeding is carried out in a manner suitable for editing Hebrew text.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 13 === [ocr; layer=garbled; conf=93]
10. List of Files and Documents for submission
The software Supplier shall submit the following files and documents for inspection:
« Form A: Details of the Supplier applying for the Approval of the TSPS (from
Appendix 2).
* Form 8: Declaration of Conformity to the Threshold Requirements, and
Requirement for Maturity of the Software (TSPS) and the Supplier (from
Appendix 2).
* Form C: Declaration of TSPS Compliance with Support and Maintenance
Requirements (from Appendix 2).
« Form D: Declaration of Compliance with the Software Approval Process,
Maintaining the Validity of the Approval and the Backward Compatibility (from
Appendix 2).
* Form 5: List of Documents and Files to be Submitted (from Appendix 2).
* List of tests for the Supplier and Software (TSPS) Examiner signed by the
supplier (in accordance with Supplement C to Appendix 1).
« Traffic signal planning booklet, containing a Traffic Signal design that was
perfomed and produced by the proposed software, for a traffic-actuated
intersection, that includes parallel transition states between stages, as defined
in Supplement B of Appendix 1.
« Traffic signal planning booklet, containing a Traffic Signal design that was
perfomed by the proposed software, for an intersection with priority to public
transport, that includes at least the following components:
o 4 Vehicle 3 Optical Units signal groups (of which at least 2 Vehicle 3 Optical
Units signal groups with flashing green).
o 2 Pedestrain signal groups.
o 2 Bicycle signal groups (not in a crosswalk combined with pedestrains).
o 2 extension detectors.
o 1demand detector.
o Conditional flashing yellow.
o 2 Public Transport signal groups.
o Actuation of public transport detector (at least: preliminary, close, stop-line,
cancelation).
o Priority methods: green extension and early green, stage insertion.
o Cycle length limit (120 seconds).
* Detailed calculation of the inter-green duration for the two planned
intersections.
o For each pair of movements in conflict, which does not include a clearing
(=evacuating) public transport vehicle, the supplier will submit for
examination the following:
| Name of entering movement
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 14 === [ocr; layer=garbled; conf=92]
| Name of signal group to which this movement belongs
v' Entrance distance
v' Entrance speed
v' Entrance duration
| Name of clearing movement
| Name of signal group to which this movement belongs
v' Clearance distance
| Fast-Clearance speed
v Clearance duration for fast-clearance speed
| Low-Clearance speed
v Clearance duration for Low-clearance speed
"| Exact Inter-green duration (3 digits after point)
v' Inter-green duration rounded for conflicting movements
v Final Inter-green duration for signal groups (considering movement
allocation to signal groups).
o For each pair of conflicting movements, which includes a clearing public
transport vehicle, the Supplier shall submit for inspection, for the clearing
movement, the results of calculation of case | (LRT moving in a steady
speed), case lla (clearance from standing position when the clearance is
completed within the acceleration distance), and case IIb (clearance from
standing position when the clearance is completed after the acceleration is
completed).
« Design files of designed intersections.
« Unified format files of designed intersections.
« Inter-green calculations according to the list of typical cases, as presented in
Supplement A to Appendix 1, as calculated by the TSPS, and the detailed
calculation and its compliance with the MOT Guidelines of Traffic Signal
Design. For each one of the cases the Supplier shall submit for inspection the
details and results of the calculation as described above, for the Traffic Signal
plans (without allocation to a signal group).
* Inter-green calculation files (preferably in Excel format).
As far as possible, the Supplier shall make use of Hebrew strings in all text fields
(excluding names of elements which are acceptable in Traffic Signal plans as defined in
clause 9a above), for example: intersection names, name of designer, name of Local
Authority, comments, etc.).
The TSPS Supplier shall provide training and support for the TSPS operation, in order to
allow the examiner to use the software and inspect it.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 15 === [ocr; layer=garbled; conf=95]
Supplement A to Appendix 1:
List of Cases for Inter-Green Calculation Verification
Cases for Inter-green calculation verification (2 examples for each case):
a. Vehicle 3 Optical Units Signal Group
a.1. Clearance Duration Calculation
a.1.a. Clearance speed under 50 Km/h — clearance duration calculation formula
includes acceleration.
a.1.b. Clearance speed over 50 Km/h — clearance duration calculation formula
does not include acceleration.
a.1.c. Clearance duration set by fast-clearing vehicle.
a.1.d. Clearance duration set by slow-clearing vehicle.
a.2. Entrance Duration Calculation
Entrance duration is calculated according to the appropriate formula.
b. Pedestrian Signal Group
b.1. Clearance Duration Calculation
The Clearance duration is calculated according to the appropriate formula.
b.2. Entrance Duration Calculation
The Entrance duration is calculated according to the appropriate formula.
c. Bicycle Signal Group
c.1. Clearance Duration Calculation
6.1.8. Clearance speed under 50 Km/h — clearance duration calculation formula
does not include acceleration (unlike Vehicle).
c.1.b. Clearance speed over 50 Km/h — clearance duration calculation formula
does not include acceleration.
c.1.c. Clearance duration set by fast-clearing bicycle.
6.1.0. Clearance duration set by slow-clearing bicycle.
6.2. Entrance Duration Calculation
Entrance duration is calculated according to the appropriate formula.
d. LRT Signal Group
d.1. Clearance Duration Calculation — Case I: LRT is moving in a steady
speed
d.1.a. Clearance speed under 50 Km/h — clearance duration calculation formula
does not include acceleration (unlike vehicle).
d.1.b. Clearance speed over 50 Km/h — clearance duration calculation formula
does not include acceleration.
d.1.c. Clearance duration set by fast-clearing LRT.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 16 === [ocr; layer=garbled; conf=94]
0.1.0. Clearance duration set by slow-clearing LRT.
d.2. Clearance Duration Calculation — Case lla: LRT clearing from standing
position and clearance is completed within the acceleration distance
The Clearance duration is calculated according to the appropriate formula.
0.3. Clearance Duration Calculation - case llb — LRT clearing from standing
position and clearance is completed after acceleration completion
The Clearance duration is calculated according to the appropriate formula.
d.4. Final Clearance Duration
* Case where the maximum value is obtained when calculating case |.
* Case where the maximum value is received when calculating case lla.
* Case where the maximum value is received when calculating case IIb.
d.5. Entrance Duration Calculation
The Entrance duration is calculated according to the appropriate formula.
. Vehicle 2 Optical Units Signal Group
e.1. Clearance Duration Calculation
e.1.a. Clearance speed under 50 Km/h — clearance duration calculation formula
includes acceleration.
e.1.b. Clearance speed over 50 Km/h — clearance duration calculation formula
does not include acceleration.
e.1.c. Clearance duration set by fast-clearing vehicle.
e.1.d. Clearance duration set by slow-clearing vehicle.
e.2. Entrance Duration Calculation
Entrance duration is calculated according to the appropriate formula.
Final Inter-Green Times Calculation
1.1. Final Inter Green Time Clearing vehicle — Entering Vehicle
1.2. Final Inter Green Time Clearing vehicle — Entering Pedestrain
1.3. Final Inter Green Time Clearing vehicle — Entering Bicycle
f.4. Final Inter Green Time Clearing vehicle — Entering LRT
1.5. Final Inter Green Time Clearing Pedestrain — Entering Vehicle
1.6. Final Inter Green Time Clearing Pedestrain — Entering Bicycle
1.7. Final Inter Green Time Clearing Pedestrain — Entering LRT
1.8. Final Inter Green Time Clearing Bicycle — Entering Vehicle
1.9. Final Inter Green Time Clearing Bicycle — Entering Pedestrain
1.10. Final Inter Green Time Clearing Bicycle — Entering Bicycle
1.11. Final Inter Green Time Clearing Bicycle — Entering LRT
1.12. Final Inter Green Time Clearing LRT - Entering Vehicle
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
16

=== PAGE 17 === [ocr; layer=garbled; conf=95]
1.13. Final Inter Green Time Clearing LRT - Entering Pedestrain
1.14. Final Inter Green Time Clearing LRT - Entering Bicycle
1.15. Final Inter Green Time Clearing LRT - Entering LRT
. Additional Cases
g.1. When there are a number of vehicle movements in conflict, the Inter-
Green Time is set as the highest of all times, obtained by calculation for all
movement pairs that are in conflict in these signal groups.
9.2. When there are a number of bicycle movements in conflict, the Inter-
Green Time is set as the highest of all times obtained by calculation for all
movement pairs that are in conflict in these signal groups.
9.3 A case where the rounded value is lower than the minimal time of 3
seconds, and therefore the result shall be the minimum Inter-Green Time.
g.4 A case where the result of the Inter-Green Time calculation is a little
above an integer number, and therefore the final Inter-Green Time is rounded
to an integer value upwards.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 18 === [ocr; layer=garbled; conf=94]
Supplement B to Appendix 1:
Intersection 1 (for Submission for Inspection) — Intersection
Properties
Introduction
The Supplier shall plan, using the software, a Traffic Signal at an intersection with the
properties detailed in this Supplement. The intersection properties were chosen for the
purpose of testing the software and do not always match the typical properties to be
found in a standard intersection. The Vehicle signal groups in this example are
Vehicle 3 Optical Units.
This Supplement does not include a scaled plan of the intersection; instead, the
properties and distances required for planning are specified. In order to insert into the
booklet a scaled plan of 1:500, the Supplier may use a plan from a different
intersection (preferably similar) marked "example from different intersection".
General Details (partial, to be completed by the Supplier):
* Intersection name: street A — street B
« Name of Local Authority: City A
« Number of intersections at the local authority: 100
* Plan number: YS-999-999-R
« Number of intersection layout plan (geometry 1:250): YS- 999-999-HH
« Name of designer: Designer A
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
1.

=== PAGE 19 === [ocr; layer=garbled; conf=90]
General Layout of Intersection
Intersection: Road A \ Road B
General Diagram
ATE,
5 0( =
General parameters of the intersection
The intersection has four approaches. The traffic-signal is traffic activated.
3.1 Detectors/pedestrian push buttons
* Demand detectors in signal groups: 3,6,8.
e Pedestrian Demand push buttons:
"| Pd- demand for crossing pedestrian-crossing d from the median
v' Pd_c- demand for crossing pedestrian-crossing d from the south
curb
« Extension detectors for all vehicle signal groups.
3.2 Flashing Green for vehicle signal groups
« Flashing green activated for signal groups: 2,4,6,8. For the other signal
groups flashing green will not be activated.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
2.
3.

=== PAGE 20 === [ocr; layer=garbled; table; conf=93]
3.3 Flashing Yellow / combined right-turn for Vehicles and Crossing
Pedestrians
*. Turning right from the south (signal group 3) will be activated in parallel with
the green at pedestrian-crossing d (conditional flashing Bd)
*. Turning right from the west (signal group 4) will be activated in parallel with
the green at pedestrian-crossing f (conditional flashing Bf)
* For the right turn from the east, flashing-amber will be constantly active
(Constant flashing Bi)
Data for Inter-green calculation
4.1 General
* Reaction time: 1 second
« Clearing vehicle deceleration: 3.5 m/sec(2)
*. Vehicle length: 12 m.
4.2 Traveling/crossing speeds
4.2.1 Vehicle:
Fast-clearing Slow-clearing Fast-entering Movement
vehicle speed vehicle speed vehicle speed direction
(Km/h) (Km/h) (Km/h)
50 25 50 E-L
50 25 50 E-R
90 35 90 E-T
50 25 50 N-L
50 30 50 N-R
80 35 80 N-T
50 25 50 S-L
50 30 50 S-R
80 35 80 ST
50 25 50 W-L
50 25 50 W-R
90 35 90 W-T
(read table columns from right to left)
4.2.2 Pedestrians:
Pedestrian | Crossing
Crossing | Speed (m/s)
a 1.2
b 1.2
6 1.0
d 1.0
e 1.2
f 1.2
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
4.
--- table-ocr psm6 (row order; verify values on page image) ---
3.3 Flashing Yellow / combined right-turn for Vehicles and Crossing
Pedestrians
*. Turning right from the south (signal group 3) will be activated in parallel with
the green at pedestrian-crossing d (conditional flashing Bd)
*. Turning right from the west (signal group 4) will be activated in parallel with
the green at pedestrian-crossing f (conditional flashing Bf)
* For the right turn from the east, flashing-amber will be constantly active
(Constant flashing Bi)
4. Data for Inter-green calculation
4.1 General
* Reaction time: 1 second
« Clearing vehicle deceleration: 3.5 m/sec(2)
*. Vehicle length: 12 m.
4.2 Traveling/crossing speeds
4.2.1 Vehicle:
Fast-clearing Slow-clearing Fast-entering Movement
vehicle speed vehicle speed vehicle speed direction
Km/h Km/h Km/h
[50 | 25 | 5 | ER |
9 | 3% | 9 | ET |
[50 | 3 | 5 | NR |
8 | 3% | 8 | NT |
[8 | 3 | 8 | ST |
Le [| 3 | 90 | WT |
(read table columns from right to left)
4.2.2 Pedestrians:
Pedestrian | Crossing
Crossing | Speed (m/s)
[a [ 12 |
|b | 12 |
[ d | 10 |
| 6 | 12 |
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
20

=== PAGE 21 === [ocr; layer=garbled; conf=94]
4.3 Inter-Green distances:
4.3.1 Pedestrian-crossing Lengths
Pedestrian | Crossing
Crossing | Length (m)
a 6.5
b 6.0
c 9.0
d 6.5
e 8.0
f 5.5
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 22 === [ocr; layer=garbled; table; conf=82]
4.3.2 Entry distances and Clearance distances for movements: Entering Vehicle -
Clearing Vehicle
4 / Distance for Distance for
Clearing Entering 8 / 4 4
clearing vehicle | Entering vehicle
Movement Movement
(m) (m)
1 E-T N_-L 41.5 8.5
2 ET ה-א‎ 17.5 85
3 ET דא‎ 20 85
4 54 N_-L 39 10
5 S_R N_-L 18.5 28
6 5 ד‎ N_-L 22 14
7 54 N_R 35 11
8 5 -L ז- א‎ 27.5 12
9 ז- או‎ N_-L 8 19
10 W_R דא‎ 18 275
11 ד א ז- או‎ 3 25
12 E -L N_-L 20 18
13 E_-L דא‎ 7 20
14 או‎ + N_-L 23 95
15 W_-L ז- א‎ 7 4
6 N_-L ד ם‎ 19 41
17 N_R ד ם‎ 15 185
18 ד ם דא‎ 16 16.5
19 S -L E-T 35 20
20 5 ד ם ד‎ 25 6.5
21 ד ם + או‎ 8 7
2 א‎ -L 5 - 5 8.5
23 N_R 54 4 24
24 דא‎ 5-4 4 155
25 -א‎ SR 42 8
26 א‎ -L 5 ז-‎ 4 75
27 ET 54 29 24
28 ET 5 ד‎ 15 20
29 ז- או‎ 54 18 75
30 ד- או‎ 5-8 5 8
41 ד 5 ד- או‎ 25 7
22 EL 54 25 105
33 E -L 5 ז-‎ 6 4
34 או‎ 54 17 15.5
35 ד 5 4-ו‎ 28 195
36 8-ו דא‎ 355 85
37 א‎ -L Ww _-T 33 14
38 ד- או דא‎ 25 8
39 54 ד או‎ 18 125
40 5 -R Ww _-T 18 20
41 5 ד- או ד‎ 15.5 175
42 EL או‎ ₪ 44 85
43 EL ד אי‎ 25 8
4 א‎ -L ם‎ -L 6 75
45 דא‎ E_-L 28 16
46 54 EL 18 13
47 5 ם ז-‎ -L 25 8
8 W_R E_-L 18 22
49 ז- או‎ EL 19 115
50 N_-L או‎ + 25 95
51 N_-T W_-L 215 8.5
52 ET W_-L 0 100
53 54 WL 25 75
54 5 ד‎ WL 28 16
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
--- table-ocr psm6 (row order; verify values on page image) ---
4.3.2 Entry distances and Clearance distances for movements: Entering Vehicle -
Clearing Vehicle
/ / Distance for Distance for
Clearing Entering 8 / 4 4
| hm | moe ene
(m) (m)
[2 [ET [NR [175 [85 |
[6 [~~ soT [NL [22 [1a]
[7 [sit [NR [3 [11]
[8 [si [NaI | 2275 [12 |
[eo [wo [NL [28 [19 |
| ‏חר‎ [NR [ET [15 [185 |
[2 | NR ‏ה | ה‎ 54 [21 [24 |
[26 [NAL [SR | 42 [8 |
[8 [wT [ SR [205 | & |
[8 [NT [WT [285 ‏ה | ה‎ & |
[40 [sR [wo [18 [2 |
[4 [EL [wa [225 [8 |
[4 [NAL [EL [26 [75 |
[4 [si [EL [18 18 |
[4 [sax [EL [25 [8 |
[4 | wR [ EL [18 [22 |
[49 [wo [EL [19 [M5 |
[6s [ET [| ‏א‎ [0 [10 |
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
22

=== PAGE 23 === [ocr; layer=garbled; table; conf=89]
3
4.4 Entry distances and Clearing distances for movements: Pedestrian
clearing — vehicle entering
Clearing Entering Crossing Entry
signal group | Movement Distance (m) | Distance(m)
a N_-L 6.5 0
d N_-L 6.5 25.0
a N_-R 6.5 0
a א‎ - 6.5 0
f א‎ - 5.5 32.0
0 E-T 9.0 0
c S + 8.0 0
0 S_-R 8.0 0
b 5 -T 6.0 28.5
c 5 -T 8.0 0
d W_-T 6.5 26.0
c E -L 9.0 0
f E -L 5.5 24.0
b W_-L 6.0 23.0
4.5 Entry distances and Clearing distances for movements: vehicle
clearing —Pedestrian entering
Clearing Movement Entering Signal Distance for clearing
Group vehicle (m)
N_-L a 6.0
N_-R a 6.0
N_-T a 6.0
5 ז-‎ b 34.0
W_-L b 34.0
E-T 6 4.0
ם‎ -L 6 4.0
N_-L d 43.0
W_-T d 30.0
54 6 4.0
S R e 4.0
5 ז-‎ e 4.0
N_-T f 34.0
ם‎ -L f 34.0
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
--- table-ocr psm6 (row order; verify values on page image) ---
4.4 Entry distances and Clearing distances for movements: Pedestrian
clearing - vehicle entering
signal group Movement Distance (m Distance(m

| a [| NAL [ 65 | 0 |
| d | NL [ 65 [ 250 |
| a | NR | 65 | 0 |
[a [ NT [ 65 [ 0 |
| ec [ET | 80 | 0 |
[ ec [ ‏כ‎ 5 [ 80 [ 0 |
| ec | sR | 80 | 0 |
[bb [ sT [ 60 | 285 |
[ ec [ sT1 [ 80 [ 0 |
| ‏ה 6 ה‎ | w.oT [| 65 | 260 |
[oc [ ELL [ 90 [0 |
Lb [ wi [ 60 | 230 |

4.5 Entry distances and Clearing distances for movements: vehicle

clearing —Pedestrian entering

Clearing Movement Entering Signal Distance for clearing
Group vehicle (m)
[NL [a | 60 |
[NR [a | 60 |
NT a [60 |
[ sT1 [bb | 340 |
ow. Fb [80 |
NAL Fd 430 |
[wT [dd | 300 |
ls. Fe [40 |
[ sR [ee | 40 |
[ sT1 [  e | 40 |
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
23

=== PAGE 24 === [ocr; layer=garbled; conf=85]
4
5. Stages
The Traffic Signal stages are described in the following diagram:
aN
(A)
ZY ZRY
|B) A ® | C)
\2 Ye Na
חפה
7
5
7
TX 05
Comments:
Stage C is identical in its components to stage C1, stage C is meant to allow un-
interrupted consecutive crossing of pedestrian-crossings d and then c.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 25 === [ocr; layer=garbled; conf=96]
25
6. Flow Chart/ Operating Logic
The operating logic of the traffic signal is detailed in the following diagram:
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 26 === [ocr; layer=garbled; conf=94]
6.1 Comments on Operating Logic
6.1.1 The transition from stage D to stage A is a parallel transition’ to be
implemented according to data from the extension detectors E6 and 58.
Stages E and F will not necessarily fully run their course in such a
transition.
6.1.2 Signal group pair '2 and 6' and pair '4 and 8' are adjacent signal groups
and one cannot open/close the green in these pairs 1 second apart.
7. Traffic Volume and Green Times
7.1 Minimum Green Durations
Signal Minimum Green
Group Duration (sec)
1 6
2 10
3 6
4 10
Additionally, the green duration from the beginning of green for crossing d in stage C until
the closure of green in crossing C shall not be less than 15 seconds.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 27 === [ocr; layer=garbled; table; conf=87]
7.2 Traffic Volume and Maximum green durations required for vehicle
signal groups
Signal Plan 1 Plan 2
Group | Hourly Volume | Max Green Hourly Volume Max
(Etu/hour/lane) Duration (Etu/hour/lane) Green
(sec) Duration
Etu=Equivalent (sec)
traffic units
1 150 12 40 6
2 500 31 350 19
3 350 22 150 10
4 400 28 150 10
5 200 15 80 6
6 140 10 150 10
Comments:
a. Max green durations shown in the table define the duration required for vehicles.
These durations will be extended as necessary to meet minimum green duration in
vehicle signal groups, pedestrian signal groups or for continuous crossing of
pedestrian-crossings d and then c.
b. The required Max green durations do not necessarily match the traffic volumes.
However, traffic volumes should be integrated, as detailed above, into the planning
presentation (Durations and Volumes Table).
8. Operation Time-Table
00:00 09:00 Sunday - Wednesday
] ]27[ ך )1( )27( /
06:00
00:00 12:00 Thursday
[ [27] I (1) I (2) ]
06:00
0:00 10:00 Friday + Holiday eve.
[ 12] 1 (17) I | 2 [ /
05:00
00:00 Satureday + Holiday
/ 11[ ]
ה ו ה ה ו 0" 0 = ₪ ו מ | | חן ו f‏
24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
27
--- table-ocr psm6 (row order; verify values on page image) ---
7.2 Traffic Volume and Maximum green durations required for vehicle
signal groups
Signal Plant |  Plan2 |
Group | Hourly Volume | Max Green Hourly Volume Max
(Etu/hour/lane) Duration (Etu/hour/lane) Green
(sec) Duration
Etu=Equivalent (sec)
traffic units
[1+ [150 | 12 | 4 [| 6 |
| 6 [| 200 | 15 | 8 [| 6 |
L 6 [ 140 | 10 | 150 [| 10 |
Comments:

a. Max green durations shown in the table define the duration required for vehicles.
These durations will be extended as necessary to meet minimum green duration in
vehicle signal groups, pedestrian signal groups or for continuous crossing of
pedestrian-crossings d and then c.

b. The required Max green durations do not necessarily match the traffic volumes.
However, traffic volumes should be integrated, as detailed above, into the planning
presentation (Durations and Volumes Table).

8. Operation Time-Table
00:00 09:00 Sunday - Wednesday
0 06:00 0 0
00:00 12:00 Thursday
0 06:00 0 0
00:00 10:00 Friday + Holiday eve.
05:00
00:00 0 Satureday + Holiday
ttt
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
27

=== PAGE 28 === [ocr; layer=garbled; conf=95]
Supplement 6 to Appendix 1:
List of tests for the software (TSPS) Supplier and Examiner
. The TSPS Examiner/Consultant will test the sample Traffic Signal plans submitted by the Supplier (Printed and Files) and the submitted
Inter-green duration calculations (in-addition to the ones included in the plans). Additionally, The Examiner/Consultant will verify the
requirements by using the software and at least as detailed below.
. The Examiner/Consultant will detail (where required) the gaps in TSPS capabilities vs. requirements.
. General Threshold Requirements —
Requirement Detail of Requirement The Test and its implementation Consultant (on Examiner
section behalf of Supplier) | Signature
Signature
5 Compliance with Requirements | Verification of Supplier statement
for TSPS Maturity and Supplier | (Form Bin Annex 2).
Experience, and written
Declaration for compliance with
the conditions on Form B in
Appendix 2.
6 Compliance with TSPS Support | Verification of Supplier statement
and Maintenance (Form C in Annex 2).
Requirements, and written
Declaration for compliance with
the conditions on Form C in
Appendix 2.
7 Compliance with the Software Verification of Supplier statement
Approval Process, Maintaining | (Form D in Annex 2).
the Validity and Backward
Compatibility, and written
Declaration for compliance with
the conditions on Form D in
Appendix 2.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
28

=== PAGE 29 === [ocr; layer=garbled; conf=95]
Examiner
Signature
29
4. General Threshold Technical Requirements —
Detail of Requirement The Test and its implementation Consultant (on behalf
of Supplier) Signature
Compliance with Threshold Verification of Supplier statement (Form
Requirements of the TSPS, and written B in Appendix 2).
Declaration for compliance with the
conditions on Form B in Appendix 2.
Plan and Execute the two submitted a. Plans submitted by the Supplier
Sample Intersections using the Software,
and Export of Plan to Unified-Format File
e Testing submitted files"
compliance to Unified-Format
requirements while meeting
Requirements of the clause.
b. TSPS usage
Randomly implementing general
changes in the TSPS and exporting
to the Unified-Format file while using
the TSPS and analyzing the relevant
changes in the resulting file.
The examiner/consultant will
introduce changes in Hebrew
strings, will export to the file and
check the relevant result in the
unified file.
e The TSPS properly exports the
changes into the exported file,
while meeting the requirement of
the clause.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
Requirement
section
8
8a

=== PAGE 30 === [ocr; layer=garbled; conf=94]
30
Inter-Green Duration Calculation for the | a. Plans submitted by the Supplier
two submitted Sample Intersections, and
for the cases described in Supplement A
to Appendix 1.
* Comparing TSPS generated
Inter-Green Durations,
presented in the Inter-Green
Duration Matrix, with the Inter-
Green Durations submitted by
the Supplier in the Inter-Green
Duration calculation document,
specifying the calculations for
each conflict.
* Comparing TSPS generated
Inter-Green Durations with MOT
requirements.
e All parameters used for Inter-
Green Duration calculations are
printed as part of the Signal
Timing-Plan.
b. Supplier calculations
exemplifying Requirement
compliance (Supplement A to
Appendix 1)
e The Supplier has submitted
examples for all typical cases
according to Supplement A to
Appendix 1, as produced by the
TSPS.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
8b

=== PAGE 31 === [ocr; layer=garbled; conf=94]
31
e The Supplier has submitted the
calculation details for all typical
cases as required.
* The resulting calculated values
comply with MOT requirements.
6. TSPS usage - Changes to
Parameters
*. Where changes were made to
parameters related to Inter-
green duration calculation, the
TSPS consequently makes all
the required changes in the
traffic-signal plan or notifies of
the need for changes required
(the notification will appear as
long as the required changes
were not implemented).
For TSPS
examiner’s/consultant's 6
please mark: Implements
Changes / Alerts.
e The TSPS prevents Signal
Timing-Plan printout or marks
the printout, in a very clear and
prominent way, when changes
were made to parameters
pertaining to Inter-Green
durations, but not all relevant
changes to the Traffic-signal
plan were made.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 32 === [ocr; layer=garbled; conf=94]
2
e The TSPS prevents the
generation of Unified-Format file
and\or download to the Traffic
Signal Control (TSC), when
changes were made to
parameters pertaining to Inter-
green durations, but not all
relevant changes to the Traffic-
signal plan were made.
Printout of the booklet with the two a. Plans submitted by the Supplier
submitted Sample Intersections.
e The printed booklet shall be
clear, understandable, and
complies with industry
standards.
Signals in accordance with traffic signal | a. Plans submitted by the Supplier
practice in Israel, for all signal types. The
signal sequence and duration shall be in
accordance with the MOT Guidelines.
e The signal sequence complies
with MOT guidelines.
e The TSPS has considered the
signal sequnce when setting the
transition between stages.
b. TSPS usage
* The TSPS does not enable
usage of sequence or signal-
lengths that are not in
compliance with the MOT
Guidelines (red-yellow, yellow,
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
8c
8d

=== PAGE 33 === [ocr; layer=garbled; conf=94]
3
flashing green, yellow triangle or
rhombus and exclamation mark
for LRT).
* The TSPS does not enable
Signal timing plan printout
and\or generation of Unified-
Format file and\or download to
Traffic Signal Conntroller (TSC),
when the sequence and the
signal lengths are not in
compliance with the MOT
Guidelines.
Start-Up program in accordance with a. Plans submitted by the Supplier
MOT Guidelines
e The Start-Up program is in
accordance with MOT
Guidelines.
b. Plans submitted by the Supplier
* In case that changes associated
with the Inter-Green times
calculation have been
implemented, the TSPS perfoms
all the required derived changes
in the Start-Up program, or
alerts about the need to perform
these changes (the alert shall
appear as long as the required
changes have not been
implemented).
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
8e

=== PAGE 34 === [ocr; layer=garbled; conf=94]
4
Examiner
Signature
For TSPS examiner's
/consultant's use, please mark:
Implements Changes / Alerts.
e The TSPS prevents Signal
Timing-Plan printout or marks
the printout, in a very clear and
prominent way, when changes
were made to parameters
pertaining to Inter-Green
durations, but not all relevant
changes to the Traffic-signal
plan were made.
The TSPS prevents the
generation of Unified-Format file
and\or download to the Traffic
Signal Control (TSC), when
changes were made to
parameters pertaining to Inter-
green durations, but not all
relevant changes to the Traffic-
signal plan were made.
5. Supportive Requirements —
Requirement | Detail of Requirement | The Test and its implementation Consultant (on behalf
section of Supplier)
9a Definitions of Element a. Plans submitted by the Supplier
Names, in accordance
with MOT Guidelines.
* Names of elements comply with MOT
requirements.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 35 === [ocr; layer=garbled; conf=94]
5
Examiner
Signature
Requirement | Detail of Requirement | The Test and its implementation Consultant (on behalf
section of Supplier)
b. TSPS usage
The Examiner/consultant will attempt to
enter element names as required for the
different elements, and will verify that the
TSPS enables their usage.
e The TSPS enables entering names of
elements that comply with MOT
requirements.
e The TSPS does not enable entering
names of elements that do not comply
with MOT requirements.
9b Definition of Minimum a. Plans submitted by the Supplier
Inter-green duration for
the various signal
groups, in accordance
with MOT Guidelines
*. Green durations for signal groups
Vehicle 3 Optical Units, Pedestrian,
and Bicycle, and Flashing Yellow
duration for Vehicle 2 Optical Units, do
not fall short of the minimum value
according to the MOT guidelines
(including in skeletons).
b. TSPS Usage
e The TSPS enables defining minimum
green durations per signal group that
comply with MOT requirements
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 36 === [ocr; layer=garbled; conf=94]
6
Examiner
Signature
Requirement | Detail of Requirement | The Test and its implementation Consultant (on behalf
section of Supplier)
e The minimum green duration
according to MOT guidelines is
integrated in the TSPS as the default
value for signal group minimum
duration.
e The TSPS does not enable, or alerts,
when attempting to enter Minimum
duration values for Vehicle signal
groups (with and without flashing
green), Pedestrian signal group, Public
Transport signal group, that are below
the minimum value according to the
MOT guidelines.
For TSPS examiner’s/consultant's use
please mark: prohibits /alerts
e The TSPS does not enable, or alerts,
when Green duration values received
are lower than the minimum values (for
example, when producing skeletons or
scenarios).
For TSPS examiner’s/consultant's use
please mark: prohibits /alerts
9c Definition of Minimum a. Plans submitted by the Supplier
Inter-green duration for
signal group/stage The Green durations for Vehicle 3
Optical Units, Pedestrain, Bicycle,
Public Transport signal group, and
Flashing Yellow duration for Vehicle 2
Optical Units signal group, do not fall
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 37 === [ocr; layer=garbled; conf=93]
7
Examiner
Signature
Requirement | Detail of Requirement | The Test and its implementation Consultant (on behalf
section of Supplier)
short of the minimum value defined in
the plan.
e The Green durations for stages do not
fall short of the minimum value defined
in the plan.
b. TSPS Usage
The Examonator’s/Consultant will enter
different Minimum green values for
Vehicle, Pedestrian, Bicycle, and Public
Transport signal groups and will verify the
Green duration values produced by the
TSPS (for example when producing
skeletons or scenarios).
* The TSPS does not enable, or notifies
when stages that are created with
green duration values that are shorter
than defined.
For TSPS examiner’s/consultant's use
please mark: prohibits /alerts
e The TSPS does not enable, or alerts,
when signal groups are created with
green duration values that are shorter
than defined.
For TSPS examiner’'s/consultant's use
please mark: prohibits /alerts
9d Definition of maximum a. Plans submitted by the Supplier
cycle length
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 38 === [ocr; layer=garbled; conf=93]
8
Examiner
Signature
Requirement | Detail of Requirement | The Test and its implementation Consultant (on behalf
section of Supplier)
e Maximum cycle length in plans
submitted does not exceed 120
seconds (including in various
scenarios with LRT priority).
b. TSPS usage
The TSPS examinato’s/consultant will insert
a maximum value cycle and will check the
cycle times created by the software.
e tis possible to define a maximum
cycle time.
*. The software prevents or alerts in the
case of situations where the cycle time
exceeds the maximum cycle time.
For TSPS examiner’s/consultant's use,
please mark: prohibits /alerts
6 Display/Highlighting of a. Plans submitted by the Supplier
deviation in Inter-green
duration (higher than * Deviations in Inter-green duration
required) while (longer than required) are noted in the
implementing transition plan.
between stages b. TSPS Usage
The Examiner/consultant will increase the
inter-green durations between signal
groups in transition between stages
* tis possible to increase the inter-
green duration between signal groups
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 39 === [ocr; layer=garbled; conf=94]
39
Examiner
Signature
Detail of Requirement | The Test and its implementation Consultant (on behalf
of Supplier)
when updating the transition between
stages.
e The TSPS displays/highlights Inter-
green duration longer than required
according to the inter-green matrix.
Conditional Flashing a. Plans submitted by the Supplier
Yellow
* Activating and dis-activating the
conditional flashing is in accordance
with MOT Guidelines.
b. TSPS Usage
e The TSPS does not enable, or alerts in
case that activating and dis-activating
the conditional flashing is not in
accordance with MOT Guidelines.
Activating and a. Plans submitted by the Supplier
deactivating of adjacent
vehicle signal groups
* Under no circumstances is the interval
duration between the start of green of
two adjacent vehicle signal groups one
second.
b. TSPS Usage
The examiner/consultant will define two
vehicle signal groups as" adjacent signal
groups" and create a scenario wherein, in
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
Requirement
section
of
99

=== PAGE 40 === [ocr; layer=garbled; conf=92]
40
Examiner
Signature
Requirement | Detail of Requirement | The Test and its implementation Consultant (on behalf
section of Supplier)
terms of Inter-green duration, these groups
‘may’ open within a one second difference.
e tis possible to define vehicle signal
groups as "adjacent signal groups"
e The TSPS prevents or notifies in case
of the activating interval for adjacent
signal groups is one second.
For TSPS examiner’s/consultant's use
please mark: prohibits /alerts
Traffic-signal operation a. Plans submitted by the Supplier‏ חפ
flow-chart Display, for - :‏
the submitted examples *. The Traffic-signal operation flow-chart‏
includes all stages and the possible
transitions between them.
*. The Traffic-signal operation flow-chart
includes all the conditions for transition
between the stages.
* The conditions for transition between
the stages are displayed separately
from the signal operation flow-chart
(In-case it is not included in the flow-
chart).
e The display format is clear and
understandable.
9i Prevention of skipping a | a. Plans submitted by the Supplier
demanded signal group,
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 41 === [ocr; layer=garbled; conf=93]
41
Examiner
Signature
Requirement | Detail of Requirement | The Test and its implementation Consultant (on behalf
section of Supplier)
based on signal group * In all branches/scenarios where a
Branch Timing Plan vehicle/pedestrian/bicycle signal group
does not receive green, the demand
for this signal group has been checked
and found negative.
b. TSPS Usage
The examiner’s/Consultant will attempt to
create a branch/scenario where a
vehicle/pedestrian/bicycle signal group
does not receive green despite being
demanded.
e The TSPS prevents or notifies when 8
vehicle/pedestrian/bicycle signal group
does not appear despite being
demanded.
For TSPS examiner’s/consultant's use
please mark: prohibits /alerts
9j Printouts a. TSPS Usage
The examiner/Consultant will test the
control options during printing, including:
e The TSPS enables choosing to print
the optional parts.
* In case the user chooses to print the
optional parts, but no relevant printable
data exists, the printout will note there
is no appropriate data available.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 42 === [ocr; layer=garbled; conf=93]
42
Examiner
Signature
Requirement | Detail of Requirement | The Test and its implementation Consultant (on behalf
section of Supplier)
e The booklet printout procedure
enables choosing and managing of the
printable sections to be done using
one keystroke and the option to print
each page separately.
e The TSPS enables creation of the
printout in a PDF file and/or creation of
a file in PDF format and printing of that
file.
9k Usage of Hebrew strings | a. Plans submitted by the Supplier
in all text fields
(excluding element
names that are b. TSPS Usage
acceptable for signal
planning in Israel)
*. Hebrew Strings appear in the booklets
Checking the usage of strings, during
TSPS usage, in all possible fashions,
including:
e The TSPS enables feeding Hebrew in
all text fields.
e The TSPS enables feeding Hebrew in
selected fields.
*. Hebrew text feeding from right to left.
* Appropriate pushing during text
feeding.
* Including quotation marks and other
special signs in the text.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 43 === [ocr; layer=garbled; conf=93]
43
Examiner
Signature
Detail of Requirement | The Test and its implementation Consultant (on behalf
of Supplier)
* Correct combination of English and
Hebrew.
«Correct combination of numbers in the
text.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
Requirement
section

=== PAGE 44 === [ocr; layer=garbled; conf=95]
Supplement ם‎ to Appendix 1:
Unified Format Requirements
The unified format shall include at least the following elements:
1. general
General junction information
junction number, junction name, project name, design version, designer details,
customer details, authority details, junction location (at least one field with junction
number).
2. base-move-list
Base signal group types allowed and their signal representation
2.1. name - signal type (closed list).
2.2. active-signal - signal type representing the active period.
2.3. inactive-signal - signal type representing the inactive period.
24. activation-sequence - the sequence to switch the signal from inactive to
active.
2.4.1. duration - activation sequence duration (second).
2.4.2. signal-type - type of signal during activation.
2.4.3. considered-active - Boolean field, 1 if activation is included in the active
time of the signal type, 0 otherwise. (For example, red/yellow is 0 - not
included in the green time).
2.5. deactivation-sequence- the sequence to switch the signal from active to
inactive.
2.5.1. duration - deactivation sequence duration (second).
2.5.2. signal-type - type of signal during deactivation.
2.5.3. considered-active- Boolean field, 1 if deactivation is included in the active
time of the signal type, 0 otherwise.
3. move-list
Junction specific signal group list including types and properties
3.1. name - signal group name.
3.2. base-move-type-name - signal group type (selected from defined signal
group types).
3.3. min-duration - minimum signal group duration.
4. evacuation-information
Evacuation information for calculating inter-green times
4.1. calculation-formula - inter-green calculation method (Israel-MOT-2025).
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 45 === [ocr; layer=garbled; conf=93]
4.2. pedestrian-information list.
Specific properties required for inter-green calculation regarding pedestrian
signal groups
4.2.1. move - pedestrian signal group name.
4.2.2. speed - pedestrian evacuation speed.
4.3. vehicle-information list.
Specific properties required for inter-green calculation regarding vehicle signal
groups
4.3.1. move - vehicle signal group name.
4.3.2. turn - vehicle move (closed list).
4.3.3. fast-vehicle-entry-speed - fast vehicle entry speed.
4.3.4. slow-vehicle-exit-speed - slow vehicle exit speed.
4.3.5. fast-vehicle-exit-speed - fast vehicle exit speed.
4.3.6. vehicle-deceleration - vehicle deceleration (meter/second”2)
4.3.7. vehicle-length - vehicle length (meter).
44. pt-information list
Specific properties required for inter-green calculation regarding public
transportation signal groups
4.4.1. move - public transportation signal group name.
4.4.2. turn- public transportation move.
4.4.3. service-accl - service acceleration (meter/second”*2).
4.4.4. service-decl - service deceleration (meter/second”2).
4.4.5. vehicle-length -vehicle length (meter).
4.5. calculation data list
Calculation Data of inter-green times (values must be included for each conflict)
4.5.1. move-in - entering signal group name.
4.5.2. turn-in - entering move (closed list).
4.5.3. move-out - exiting signal group name.
4.5.4. turn-out - exiting move.
4.5.5. exit-distance - exiting move distance to conflict point.
4.5.6. entry-distance - entering move distance to conflict point.
4.5.7. calculated-inter-green-time - raw calculation results.
4.5.8. result-inter-green-time - rounded calculation results.
matrix
Inter-green matrix
5.1. move-in - entering signal group.
5.2. move-out - exiting signal group.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
45

=== PAGE 46 === [ocr; layer=garbled; conf=94]
5.3. value - inter-green time (seconds).
. stage-list
List of junction stages
6.1. name - stage name.
6.2. stage-move-list - list of active signal groups during stage
inter-stage-list
List of Inter-stages
7.1. stage-in - the name of the stage that going in.
72. stage-out - the name of the stage that going out.
7.3. duration - inter-stage duration in seconds.
7.4. move-name - signal group name.
7.5. move-type - signal group action in inter-stage (in/out/in-out/continuous)
(closed list).
7.6. move-second - signal group action second within the inter-stage - starting
from second zero up to the length of the inter-stage.
program-list
List of operating programs
8.1. number - program number.
8.2. description - program description.
program-schedule
Programs operating schedule
9.1. name- program name.
9.2. start - program start time in minutes from midnight.
9.3. duration - program duration in minutes.
94. program - program number to activate during this time.
parameter-list
List of parameters
10.1. name - parameter name.
10.2. description - parameter description.
10.3. tcs-name - name of the parameter at the traffic control center.
10.4. tcs-number - number of the parameter at the traffic control center.
10.5. alias - alias to other parameter (optional).
10.6. program-number - program number.
10.7 - parameter-value - parameter value in program.
in-out-element-list
List of pulses and detectors outgoing/incoming from/to junction
11.1. name - name of input/output element.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
46
10.
1".

=== PAGE 47 === [ocr; layer=garbled; conf=95]
11.2. type - element type from selection list (closed list).
11.3. description - optional description.
11.4. related moves - a list of signal groups related to this detector or pulse (optional)
12. junction-schema-version
XSD version.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 48 === [ocr; layer=garbled; conf=95]
Supplement E to Appendix 1:
Intergreen Times and Vehicle Two Optical Units
Based on Guidelines of Traffic Signal Deign (Ministry of
Transport, 2025)
Enclosed in a Separate File
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026

=== PAGE 49 === [ocr; layer=garbled; table; conf=93]
Versions Control
Publication Updates
Date
October 2017
May 2019 e Correction of Clause 8, Addition of Clause 9-k, and
Revision of Supplements D and G, accordingly:
Variation of "Writing Hebrew Strings" from Threshold
Requirement to Supportive Requirement, and
therefore: Revision of Clause 1-f in Supplement A and
Clause a.3.b in Supplement E: Variation of the
Rounding Method of the value of the intergreen times
calculation, when the result in exactly 0.1 second.
*. Variation of Clause 8-b and Clause 4 in Supplement G:
Addition the option of an alert while printing, in case
that parameters relevant to intergreen calculation have
been changed, and no corresponding changes have
been implemented in the signal timing plan.
* Addition of a Comment in Supplement C: Allowing the
option to implement the printing requirements
described in the clauses above with means external to
the Software.
August 2022 * Update of Clauses 2, 5, 6, 7, 8-a, 9-k.
* Update of Supplement D to Appendix 1, Clauses 2, 3-
a, 3-b, 4.
* Update of Supplement G to Appendix 1, Clauses 3, 4.
« Addition of Supplement H.
* Language and General updates and editing throughout
the document.
January 2026 * Update of the Appendis as a whole, in accordance with
the MOT Guidelines for Traffoc Signal Design (2025).
The main changes are described in the bullets below.
* Supplements A-D from Version 3 were deleted, and
accordingly, Supplements E-H from Version 3 were re-
numbered A-D.
* Supplement E was added, in the English Version (as a
separate file), that includes translation to English of
Section 5 and Appendix N.6 of the MOT Guidelines to
Traffic Signal Design — Calculation of Inter-Green
Times.
* The method and list of cases for the calculation of
Inter-Green Times were updated.
« A requirement for Start-Up Plan for the particular
intersection was added.
*. A “Vehicle 2 Optical Units signal group” was added,
and additionally a “Pedestrain without / with Bicycle in
Crosswalk signal group” was added, and also “Bicycle
3 Optical Units signal group”.
Number
4
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 6
--- table-ocr psm6 (row order; verify values on page image) ---
Versions Control

Publication Updates

Date

si ‏ביא‎
‎2 May 2019 e Correction of Clause 8, Addition of Clause 9-k, and

Revision of Supplements D and G, accordingly:
Variation of "Writing Hebrew Strings" from Threshold
Requirement to Supportive Requirement, and
therefore: Revision of Clause 1-f in Supplement A and
Clause a.3.b in Supplement E: Variation of the
Rounding Method of the value of the intergreen times
calculation, when the result in exactly 0.1 second.

*. Variation of Clause 8-b and Clause 4 in Supplement G:
Addition the option of an alert while printing, in case
that parameters relevant to intergreen calculation have
been changed, and no corresponding changes have
been implemented in the signal timing plan.

* Addition of a Comment in Supplement C: Allowing the
option to implement the printing requirements
described in the clauses above with means external to
the Software.

3 August 2022 * Update of Clauses 2, 5, 6, 7, 8-a, 9-k.

* Update of Supplement D to Appendix 1, Clauses 2, 3-
a, 3-b, 4.

* Update of Supplement G to Appendix 1, Clauses 3, 4.

« Addition of Supplement H.

* Language and General updates and editing throughout
the document.

4 January 2026 * Update of the Appendis as a whole, in accordance with
the MOT Guidelines for Traffoc Signal Design (2025).
The main changes are described in the bullets below.

* Supplements A-D from Version 3 were deleted, and
accordingly, Supplements E-H from Version 3 were re-
numbered A-D.

* Supplement E was added, in the English Version (as a
separate file), that includes translation to English of
Section 5 and Appendix N.6 of the MOT Guidelines to
Traffic Signal Design — Calculation of Inter-Green
Times.

* The method and list of cases for the calculation of
Inter-Green Times were updated.

« A requirement for Start-Up Plan for the particular
intersection was added.

*. A “Vehicle 2 Optical Units signal group” was added,
and additionally a “Pedestrain without / with Bicycle in
Crosswalk signal group” was added, and also “Bicycle
3 Optical Units signal group”.

Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
49

=== PAGE 50 === [ocr; layer=garbled; conf=92]
* A requirement was added for the possible use of
“rhobus” and the “exclamation mark” type signals, in
the design of LRT signal plans.
* Printing Requirements were moved and updated from
Supplement C from Version 3 that was deleted, to
Section 8-c.
* List of Files and Documents for submission was moved
and updated from Supplement D from Version 3 that
was deleted, to Section 10.
Procedure for Approval of Traffic Signal Planning Software, Appendix 1, Fourth Edition, January 2026
