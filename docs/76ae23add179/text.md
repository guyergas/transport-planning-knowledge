=== PAGE 1 === [ocr; layer=garbled; image; conf=93]
מינהל תכנון IS‏
ופיתוח תשתיות
אגף בכיר תכנון תחבורתי משרדהתחבורה
והבטיחות בדרכים
General Specifications for the
Placement and Maintenance of
Traffic Signal Lights in Israel
Section 6: Traffic Signal Controller
Appendix H: TSC Cyber Protection
Edition 3.0
February 2026
Inter-Ministerial Committee
for Approval of Traffic and Safety Devices
x

=== PAGE 2 === [ocr; layer=garbled; conf=95]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
General Specifications for the Placement and Maintenance of
Traffic Signal Lights in Israel
Section 6: Traffic Signal Controller
Appendix H: TSC Cyber Protection
Edition 3.0
Prepared by: Shiran Aharoni (Head of ITS Cyber Protection
Department, MOT) and Shmuel Tzirkel
Coordinated and Edited by: Yuval Blum
Version Control for Appendix H - TSC Cyber Protection
Edition Publication Date |Updates
1 July 2022
2 November 2023 General Update
3 February 2026 General Update

=== PAGE 3 === [ocr; layer=garbled; conf=95]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
1. General
Traffic control systems constitute a critical component of transportation infrastructure, ensuring
safe, reliable, and efficient flow of vehicular and pedestrian traffic in urban and inter-urban
spaces. As cities adopt advanced connectivity-based solutions, the risk of exposing these
systems to cyber-attacks that could cause significant disruptions increases, ranging from
interference with traffic signal timing or unavailability, potentially leading to traffic chaos. Traffic
Signal Controllers (TSC) may be exposed to various threats and vulnerabilities that could
constitute an attack surface and target for attacks, such as:
. TSC blackout/ flashing.
+ Malicious code injection into the TSC and remote takeover via software updates.
+ Changes affecting the safety TSC.
. Accessing via the traffic TSC to the Control Center.
Therefore, Traffic Signal Controllers (TSCs) must meet the cyber security protection
requirements detailed in this document, to achieve protection objectives for maintaining the
safety, reliability, and availability of traffic control systems.
2. Document Purpose
To define best practice guidelines for TSC protection, addressing unique requirements in this
domain.
3. Terms and Definitions
Term/Definition Description
A system is considered remotely-operated if access,
Remote management, administrative functions, or operations can be
|IAccess/Operation performed from any location outside the internal network,
including access via the Internet/external network.
A professional entity that has received approval from the Sectoral
Cyber Unit at the Ministry of Transportation and/or the Inter-
Ministerial Committee for Traffic and Safety Devices (“the
Committee”) to perform penetration testing and risk assessment.
Testing Entity
The local signage authority that owns the Traffic Signal, and is
responsible for its design, installation, operation, and
maintenance. Abbreviated: LSA.
Local Signage
|Authority
A digital device, such as a touch screen, configured to operate in
'Kiosk' Mode a dedicated mode that restricts its use to a specific application or
process, while blocking access to other device functions.
The entirety of digital system components, each of which
|Attack Surface individually, as well as their combination, contains certain
vulnerabilities that an attacker can exploit.

=== PAGE 4 === [ocr; layer=garbled; conf=95]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
Term/Definition Description
The applicant requesting approval for a TSC from the Inter-
Supplier Ministerial Committee for Traffic Devices and Safety.
Critical/ High/ Medium/ ||Cyber Security updates for vulnerabilities classified according to
Low Security Updates | CVSS Score.
CIS Center for Internet Security.
DFD Data Flow Diagram
EOL / EOS End of Life / End of Support.
MFA/2FA Multi Factor Authentication / Two Factor Authentication.
SBOM Software Bill of Materials.
SSDLC Secure Software Development Life Cycle.
VPN Virtual Private Network.
4. Application Submission Process (see Appendix A to this annex)
4.1 A supplier requesting approval for a TSC model, as of the date of publication of this
document, must demonstrate the compliance of the TSC with cyber security protection
aspects, as detailed in this document.
4.2 As defined in Section 6.2 of the main TSC specification, regarding the TSC testing and
approval process, the supplier is required to conduct a test of the TSC in a cyber laboratory
recognized by the State. The supplier may apply for State recognition to certify any other
laboratory or independent expert.
4.3 Any deviation or request for exemption from the requirements appearing in this document
is contingent upon a submission of a professional opinion, for the approval of the Cyber
Unit at the Ministry of Transportation.
4.4 As part of the TSC approval process, the following information and documentation must
be provided:
4.4.1 Architecture Documents
Documents required for submission to the committee and cyber security laboratory:
4.4.1.1 Engineering design documents for computing equipment, communications,
and electronic equipment for all components.
4.4.1.2 TSC architecture, including access to various modules, and DFD.
4.4.1.3 Interfaces and communication modules.
4.4.1.4 Testing equipment (for maintenance and updates).
4.4.1.5 Operating system, software, and access framework.

=== PAGE 5 === [ocr; layer=garbled; conf=96]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
4.4.1.6 Detailed description of existing protection mechanisms, and their
implementation.
4.4.1.7 Documentation of SSDLC process implementation across all TSC systems,
including:
4.4.1.7.1 Current scan reports (static and dynamic) from source code
security products (code review), e.g., SonarQube, Checkmarks,
etc.
4.4.1.7.2 SBOM presentation for all software components.
4.4.2 As part of the testing process, the supplier is required to perform a simulation of the
interface between the TSC and a central traffic management system, using protocols
that the TSC supports.
4.4.3 Declaration of Conformity and Penetration Testing and Risk Management
Conformity Document: The supplier shall submit a document confirming the compliance
of the proposed TSC with the requirements of this Appendix. The document shall include
a Table containing a reference to all clauses of this Appendix, and the Supplier's
declaration of compliance with them. Documents evidencing compliance with this
appendix's requirements must be submitted to the Inter-Ministerial Committee for Traffic
and Safety Devices, together with other application materials for approval of a new TSC.
4.4.3.1 As a preliminary stage and prior to requesting approval for a new TSC, the
supplier/ manufacturer of the proposed TSC shall conduct penetration testing
and risk management assessment. Prior to conducting the testing and risk
assessment, the testing framework and scope must be submitted for
approval to the Sectoral Cyber Unit at the Ministry of Transportation and/or
the Inter-Ministerial Committee for Traffic and Safety Devices.
The testing framework shall include:
4.4.3.1.1 Name of the professional entity (the company and the cyber
inspector) who actually performs the tests — experience/
certifications.
4.4.3.1.2 Testing scenarios according to device type.
4.4.3.1.3 Contact person name from each party of the agreement (the
supplier submitting the request and the entity performing the
testing).
4.4.3.2 Penetration testing shall be enclosed to the application, and shall include at
least:
4.43.21 Detailed test plan for compliance with cyber protection
requirements, as required in this directive according to threat
analysis specific to the device and system components.
4.4.3.2.2 Testing methodology.
4.4.3.2.3 Method of performing the test (accepted methods, technological
tools, equipment and test setup, method of calculating the severity
classification of the findings, etc.).

=== PAGE 6 === [ocr; layer=garbled; conf=96]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
4.4.3.2.4 Test results that include the TSC model under test, versions
(hardware, firmware and software), and conclusions. The results
shall be submitted using a table containing a reference to all
clauses of this Appendix, and the laboratory's reference to them
(pass / fail / comments and recommendations).
4.4.3.2.5 The supplier undertakes to submit the detailed testing report to the
Ministry of Transportation / Sectoral Cyber Unit, and to present it.
4.4.3.2.6 If no technical solution is found for test findings or compliance with
handling recommendations, risk analysis must be performed and
implementation of compensating controls presented.
4.5 The process for submitting an application and testing for approval of TSC cyber security
protection aspects is described in Supplement A at the end of the appendix.
5. Protection Requirements
5.1 Communications
5.1.1 External communication to the TSC shall be performed using reliable and secure
communication:
5.1.1.1 Use of communication protocols defined in the TSC specification, Section 6,
in encrypted form.
5.1.1.2 Use of strong encryption mechanisms according to current best practices. For
example: external communication to the Control Center shall use TLS -
implementation in a version without known vulnerabilities at the time of TSC
approval.
5.1.2 The TSC must implement communication segmentation between different environments
(e.g., connection to Control Center, local technician connection, sensor connection) and
the safety environment (SafeNet):
5.1.2.1 Access from management/ operational networks to the SafeNet network shall
not be permitted.
5.1.2.2 If access between networks/ environments is required, it must be performed
by defining rules in the operating system's internal firewall (IPTABLE/ HFW)
for specific Ips, using a dedicated Allow List mechanism.
5.1.3 Implementation of protection mechanism against denial-of-service attacks on the
SafeNet network / safety component.
5.1.4 Definition of static IP addresses for each component installed in the TSC, and disabling
of dynamic address allocation mechanism (DHCP).

=== PAGE 7 === [ocr; layer=garbled; conf=96]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
5.2 Hardening
5.2.1 The TSC shall implement inherent security (hardening) according to hardening
standards accepted in European Union or US countries, such as CIS, to enable minimal
access only as needed for system services.
5.2.2 Disabling / removal of radiating hardware / software component capabilities - the TSC
shall not include communications such as WIFI, GSM, BT, NFC, if they are not required
for the operation / function of the TSC. If use of such communications is required, they
must be hardened according to current best practices.
5.2.3 Prevention of external device connection capability (removable media) to the TSC, for
example: USB, SD, CD, RJ45, except those required for basic and essential TSC
operation, and for secure access control purposes, for example: dongle (security token),
testing equipment, etc.
5.2.4 Hardening of all ports, except those required for basic and essential TSC operation:
5.2.4.1 Closure of unused ports.
5.2.4.2 Closure of diagnostic ports in the TSC: JTAG, UART, SPI, etc. If required for
future use, they must be blocked using physical access control.
5.2.5 Hardening of system services and processes:
5.2.5.1 Removal of unused libraries.
5.2.5.2 Running services with lowest possible privileges, except management
services (such as SSH).
5.2.6 Changing default users and passwords.
5.2.7 Implementing an internal mechanism to prevent unwanted access to the TSC, by
managing devices and supporting the following hardening:
5.2.7.1 Prevention of MAC address spoofing
5.2.7.2 Prevention of IP spoofing
5.2.7.3 Support for 802.1x protocol authentication is recommended.
5.2.8 Implementation of secure boot process to prevent execution of malicious software during
TSC restart.
5.2.9 If 'kiosk' mode (lean operating system) is implemented in the TSC display screen,
hardening must be performed according to best practices, to prevent breakout to the
operating system.
5.2.10 Removal of all access capabilities and code segments from development and testing
phases. For example, closure of management interfaces in testing environments.

=== PAGE 8 === [ocr; layer=garbled; conf=96]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
5.3 User Control and Segregation
5.3.1 Local TSC Management System
5.3.1.1 The management system shall support multiple authorization levels, for
example: guest, technician, administrator users. These users shall have
different viewing permissions, and only specific users shall be able to make
system changes.
5.3.1.2 User authentication shall be performed according to a policy including
passwords of at least 8 characters, including letters, numbers and special
characters.
5.3.1.3 For users with high privileges, user authentication shall be performed using
two-factor authentication (2FA) mechanism.
5.3.1.4 Sensitive details about IP addresses, MAC addresses, and TSC network data
shall not be displayed or exposed on the TSC display screen, before
authentication by an authorized user.
5.3.1.5 Implementation of protection mechanism to limit the number of system
authentication requests (brute force / user enumeration attacks).
5.3.2 Operating System
5.3.2.1 Authentication to operating system management services (ssh, sftp) shall be
performed using dedicated certificates and not using passwords.
5.3.2.2 Changes at BIOS level shall be performed using strong passwords only,
including passwords of at least 8 characters, including letters, numbers and
special characters.
5.3.2.3 Passwords shall be stored securely and encrypted. Additionally, the ability to
read passwords stored in the system shall not be permitted, and passwords
shall not be stored within system code (hard-coded credentials).
5.4 Physical Control
5.4.1 TSC storage in a locked cabinet, incorporating an Anti-Tamper component, with alerting
capability upon unauthorized cabinet access, and reporting to a central monitoring
system with cabinet intrusion detection (if central system exists).
5.5 Change and Update Management
5.5.1 Software and firmware to be used shall have undergone an orderly and documented
SSDLC process, and are not based on open-source code, that has not undergone a
testing and inspection process.
5.5.2 As defined in Section 6.2 of the main TSC specification, it must be verified with the
manufacturer that there is support for TSC versions for a period of at least ten (10) years
from the date of initial approval, and that the manufacturer undertakes to provide security
updates continuously without reservations of End of Life (EOL) / End of Support (EOS).
The update shall include the software components in the latest versions.

=== PAGE 9 === [ocr; layer=garbled; conf=96]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
5.5.3 It is required to download the update files from the manufacturer's official website, and
verify the originality/ authenticity of the software components before installation.
5.5.4 If software updates are performed remotely, directly by the manufacturer, this must be
done in coordination with the LSA and the Supplier, only after verifying that the update
meets cyber security requirements.
5.5.5 Firmware updates shall be performed at the supplier's laboratory only.
5.5.6 Routine software updates: The TSC manufacturer/ supplier commits at the time of
requesting approval for a new TSC device to perform routine firmware and cyber security
updates, with update frequency not less than once every 12 months. The applicant also
commits to install these updates on every TSC unit of the approved model actually
installed in the field. The update shall be performed and documented no later than three
(3) months from the date of update distribution by the manufacturer.
5.5.7 Cyber Security Updates
5.5.7.1 The TSC manufacturer/ supplier commits at the time of requesting approval
for a new TSC device to perform cyber security updates to most recent status.
The applicant also commits to install and document cyber security updates for
every TSC unit of the approved model actually installed in the field, as detailed
below:
5.5.7.1.1 Critical cyber security updates: shall be performed and
documented on every installed TSC of the approved model, as soon
as possible, and no later than two weeks after update distribution
by the manufacturer.
5.5.7.1.2 High-priority cyber security updates: shall be performed and
documented on every installed TSC of the approved model, no later
than one month after the update release date. If the vulnerability
allows remote exploitation and impact on the TSC, the update
should be treated as critical cyber security update, and updated
accordingly.
5.5.7.1.3 Medium and low-priority cyber security updates: shall be
performed and documented on every installed TSC of the approved
model as part of routine manufacturer updates process.
5.5.7.2 The TSC supplier commits to receive on-going updates from the
manufacturer, regarding critical and high vulnerabilities found in the TSC, and
to report to the LSA within 24 hours a plan for fixing the vulnerability and
reducing the risk.
5.5.8 Update implementation method
Update implementation method: Routine manufacturer updates or critical cyber
security updates or patches, for an approved TSC model, shall be performed securely
and encrypted, and their implementation documented by the applicant throughout the
entire approval validity period, with reference to every TSC unit of the approved model
actually installed in the field. Documentation of execution and implementation of all
required updates shall be submitted for review and approval by the Sectoral Cyber Unit
of the Ministry of Transportation, at the time of application for the three-year validity
extension for the TSC by the Inter-Ministerial Committee for Traffic and Safety Devices.
9

=== PAGE 10 === [ocr; layer=garbled; conf=96]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
Presentation of approval from the Sectoral Cyber Unit that the submitted report is
satisfactory, shall constitute a condition for approval of the validity extension.
5.5.9 The “update table” shall include at least the following details: TSC model, location of
installation intersection, update date, nature of the update, severity of the vulnerability
(if any), description of the vulnerability that was fixed (if any), version number of the
hardware/ firmware/ software that was updated.
5.6 Monitoring - Logging and Documentation
5.6.1 Logs (security and behavioural) collected in the TSC, shall be stored locally in the TSC
for a period of 3 months, in a non-volatile and non-removable memory storage
component.
5.6.2 A log recording procedure is required within the TSC, that enables as a minimum:
5.6.2.1 Identification or neutralization or failure of registration.
5.6.2.2 Monitoring of processing power and alerting about extreme system events. A
set of passive/ active actions by the TSC must be defined upon detection of
such anomalies.
5.6.2.3 Operating system logging.
5.6.2.4 Identifying attacks on TSC management interfaces (e.g., web attacks on
management interface, brute force on authentication process, etc.).
5.6.2.5 Logging remote access and connection operations (if exists).
5.6.3 The ability to transfer logs to a central server and monitor them in the Control Center is
required.
10

=== PAGE 11 === [ocr; layer=garbled; conf=88]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
Supplement A: Application Submission and Testing Process for TSC Cyber
Security Protection Aspects Approval
Process /
Stage Nature Performer Required Output
Submission of application for
1 approval / validity extension of TSC supplier
approval of a TSC to the Committee
Supplier contacts to a laboratory
certified by the Ministry of Application/Request
2 Transportation - for receiving a TSC supplier Initiation Document
proposal
Submission of testing framework Scope document for
3 land scope - for approval by Sectoral [TSC supplier (performing the penetration
Cyber Unit/ Committee test
Activity initiation and testing TSC supplier
0 + Testing
execution Ny
entity
Sending TSC documents as TSC supplier "TSC documents as per
required in this document pp clause 4.4.1
4
Setting activity framework and . ,
schedule for TSC testing Testing entity ||Complete SOW
Presenting SOW for approval by TSC supplier
Sectoral Cyber Unit/Standards and ||+ Testing
The Committee entity
A full PT test on the TSC, including
conducting research and risk Testing entit Testing and complete initial
assessment on the manufacturer's 9 דם| ל‎ report after TCS testing
5 documents
Writing the report and validating it ,
with the supplier + the Ministry of Testing entity Presenting draft report for
. 56 supplier comments
Transportation
6 Handling report findings TSC supplier
14

=== PAGE 12 === [ocr; layer=garbled; conf=89]
General Specifications for the Placement and Maintenance of Traffic Signal Lights in Israel, Section 6: Traffic
Signal Controller, Appendix H: TSC Cyber Protection, Edition 3.0, February 2026
Re-testing after correcting the report Final report to TSC
Testing entity
findings supplier
7 Testing entity +
Compliance check with the TSC supplier + Compliance document
requirements Ministry of
Transportation
|Approval of Sectoral
Final approval of Sectoral Cyber Unit at ||, ,. . Cyber Unit at the
- : Ministry of -
8 the Ministry of Transportation for the Transportation Ministry of
TSC according to the findings 2 Transportation for the
TSC device.
12
