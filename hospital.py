"""
Assignment 0 solution
CSC148, Winter 2020
Michael Liut, Bogdan Simion, and Paul Vrbik.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Bogdan Simion, Michael Liut, Paul Vrbik, Dan Zingaro
"""

from __future__ import annotations
from typing import List, Tuple, Dict
from collections import defaultdict
import datetime
import loaddata

MONTH_ABBREV = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                'Oct', 'Nov', 'Dec']

ABBREV_TO_NUMBER = {month: k + 1 for k, month in enumerate(MONTH_ABBREV)}


class HospitalVisit:
    """An object for storing the medical history for a single visit of a
    patient to a hospital.

    Public Attributes
    =================
    date: The date of the visit.
    doctor_id: The identification number of the doctor who delivered care
        during this visit.
    patient_id: The identification number for the patient associated with this
        visit.
    diagnosis: A human-readable string of the diagnosis (assigned ailment) of
        this patient.
    prognosis: A human-readable string of the prognosis (assigned outcome) by
        the doctor for this patient.
    prescribed: A human-readable string of the medication prescribed during
        this visit.
    followup_date: A date for followup for this patient or None.

    Representation Invariants
    =========================
    - not followup_date or date < followup_date

    Sample Usage
    ============
    >>> visit = HospitalVisit(\
                datetime.date(2017, 10, 23),\
                99722708,\
                44123123,\
                "Dengue Fever",\
                "very poor",\
                "Sucralfate",\
                datetime.date(2017, 11, 30)\
    )
    >>> visit.doctor_id
    99722708
    >>> visit.patient_id
    44123123
    """

    date: datetime.date
    doctor_id: int
    patient_id: int
    diagnosis: str
    prognosis: str
    prescribed: str
    followup_date: datetime.date

    def __init__(self, date: datetime.date, doctor_id: int, patient_id: int,
                 diagnosis: str, prognosis: str, prescribed: str,
                 followup: datetime.date) -> None:
        """Initialize this HospitalVisit.
        """
        self.date = date
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.prognosis = prognosis
        self.prescribed = prescribed
        self.followup_date = followup

    def __repr__(self) -> str:
        """Return a human-readable representation of this object.
        Do not modify this! This is not to be used to reconstruct the object.
        """
        return "{}, {}, {}".format(self.date, self.doctor_id, self.patient_id)

    def __eq__(self, other: HospitalVisit) -> bool:
        """Return True if this HospitalVisit is equal to <other>.
        Hospital visits are equal when their
            date, doctor_id, and patient_id
        attributes are equal.

        Each of these triplets is unique as it is presumed Doctors cannot
        see the same patient twice in one day.
        """
        return (self.date, self.doctor_id, self.patient_id) == \
               (other.date, other.doctor_id, other.patient_id)


class Doctor:
    """An object for storing employment data for a medical doctor.

    Public Attributes
    =================
    name: The name of this doctor in the form 'Firstname Lastname'
    id: A unique integer identification number.
    salary: How much this doctor is paid to work one day.
    schedule: A dictionary object mapping as keys the month abbreviations
        'Jan', ..., 'Dec' to a list of datetime objects representing the days
        when this doctor works in each corresponding month.

    Sample Usage
    ============

    >>> bob = Doctor("Bob Loot", 98765432, 1079.80)
    >>> bob.schedule['Jan'].append(datetime.date(2017, 1, 23))
    >>> bob.schedule['Jan'].append(datetime.date(2017, 1, 24))
    >>> sorted(bob.schedule['Jan'])
    [datetime.date(2017, 1, 23), datetime.date(2017, 1, 24)]
    >>> bob.schedule['Feb']
    []
    """

    name: str
    id: int
    salary: float
    schedule: Dict[str, List[datetime.date]]

    def __init__(self, name: str, id_num: int, salary: float) -> None:
        """ Initialize this Doctor with name <name>, identification number
        <id_num>, and salary <salary>.
        """
        self.name = name
        self.id = id_num
        self.salary = salary
        self.schedule = {month_abbrev: [] for month_abbrev in MONTH_ABBREV}

    def __repr__(self) -> str:
        """ Return a human-readable representation of this object.
        Do not modify this! This is not to be used to reconstruct the object.
        """
        return "Did: {}".format(self.id)

    def __eq__(self, other: Doctor) -> bool:
        """ Return True if this Doctor is equal to <other>.
        Two doctors are equal when their (unique) ids are equal.
        """
        return self.id == other.id

    def __lt__(self, other: Doctor) -> bool:
        """ Return True if this Doctor is ordered earlier than <other>.
        Ordering is given by Doctor.id
        """
        return self.id < other.id


class Patient:
    """An object for storing medical history for a patient.

    Public Attributes
    =================
    name: The name of this patient in the form 'Firstname Lastname'
    id: A unique identification number.
    history: A list of HospitalVisit entries when this patient visited the
        hospital.

    Sample Usage
    ============
    >>> carol = Patient("Carol Loot", 44021721)
    >>> carol.id
    44021721
    """

    name: str
    id: int
    history: List[HospitalVisit]

    def __init__(self, name: str, id_num: int) -> None:
        """ Initialize this Patient with name <name> and identification number
        <id_num>.
        """
        self.name = name
        self.id = id_num
        self.history = []

    def __repr__(self) -> str:
        """ Return a human-readable representation of this object.
        Do not modify this! This is not to be used to reconstruct the object.
        """
        return "Pid: {}".format(self.id)

    def __eq__(self, other: Patient) -> bool:
        """ Return True if this Patient is equal to <other>.
        Two patients are equal when their (unique) ids are equal.
        """
        return self.id == other.id

    def __lt__(self, other: Patient) -> bool:
        """ Return True if this Patient is ordered earlier than <other>.
        Ordering is given by Patient.id
        """
        return self.id < other.id

    def is_prescribed(self, medication: str) -> bool:
        """
        Return True only when this Patient has been prescribed <medication>
        during a hospital visit.

        >>> carol = Patient("Carol Loot", 44021721)
        >>> visit = HospitalVisit(\
            datetime.date(2017, 10, 23),\
            99722708,\
            44123123,\
            "Dengue Fever",\
            "very poor",\
            "Sucralfate",\
            datetime.date(2017, 11, 30)\
        )
        >>> carol.history.append(visit)
        >>> carol.is_prescribed("Sucralfate")
        True
        >>> carol.is_prescribed("Lithium")
        False
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/janonly/")
        >>> hosp.patients[0].is_prescribed("Propofol")
        False
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/year97/")
        >>> hosp.patients[3].is_prescribed("Propofol")
        True
        """
        for visits in self.history:
            if visits.prescribed == medication:
                return True
        return False

    def followups(self, month: str) -> List[datetime.date]:
        """ Return a list of days (i.e. datetime objects) when patient
        has followups during the month <month>.
        The <month> is represented using the abbreviations: {'Jan',...,'Dec'}.

        No particular list order is required.

        >>> carol = Patient("Carol Loot", 44021721)
        >>> visit = HospitalVisit(\
            datetime.date(2017, 10, 23),\
            99722708,\
            44021721,\
            "Dengue Fever",\
            "very poor",\
            "Sucralfate",\
            datetime.date(2017, 11, 30)\
        )
        >>> carol.history.append(visit)
        >>> carol.followups('Nov')
        [datetime.date(2017, 11, 30)]
        >>> carol.followups('Aug')
        []
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/janonly/")
        >>> sorted(hosp.patients[0].followups('Feb'))
        [datetime.date(2017, 2, 2)]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/year97/")
        >>> sorted(hosp.patients[1].followups('Sep'))
        [datetime.date(1997, 9, 2), datetime.date(1997, 9, 20)]
        """
        int_month = 0
        for i in range(len(MONTH_ABBREV)):
            if MONTH_ABBREV[i] == month:
                int_month = i + 1

        followups = []
        for visit in self.history:
            if not visit.followup_date is None and \
                    visit.followup_date.month == int_month:
                followups.append(visit.followup_date)
        return followups

    def prescribed_after(self, date: datetime.date) -> List[str]:
        """Return the list of medications (strings) prescribed after (inclusive)
        <date>.

        This list may include duplicates if a medication is prescribed during
        multiple visits.  No particular list order is required.

        >>> carol = Patient("Carol Loot", 44021721)
        >>> visit = HospitalVisit(\
            datetime.date(2017, 10, 23),\
            99722708,\
            44021721,\
            "Dengue Fever",\
            "very poor",\
            "Sucralfate",\
            datetime.date(2017, 11, 30)\
        )
        >>> carol.history.append(visit)
        >>> carol.prescribed_after(datetime.date(2017, 10, 22),)
        ['Sucralfate']
        >>> carol.prescribed_after(datetime.date(2017, 12, 1))
        []
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/janonly/")
        >>> sorted(hosp.patients[1].prescribed_after(datetime.date(1900,1,1)))\
            #doctest: +NORMALIZE_WHITESPACE
        ['Docusate Sodium', 'Hydrocortisone Na Succ.',
         'Lansoprazole Oral Suspension',
         'Lansoprazole Oral Suspension', 'Lidocaine']
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/year97/")
        >>> sorted(hosp.patients[0].prescribed_after(datetime.date(1900,1,1))) \
            #doctest: +NORMALIZE_WHITESPACE
        ['Acetaminophen', 'Docusate Sodium', 'Hydrochlorothiazide',
         'Ipratropium Bromide MDI', 'Lansoprazole Oral Suspension',
         'Levofloxacin', 'Lidocaine', 'Morphine Sulfate', 'Neostigmine',
         'Neutra-Phos', 'Spironolactone', 'sodium bicarb', 'sodium bicarb',
         'sodium bicarb']
        """
        final = []
        for visit in self.history:
            if date < visit.date:
                final.append(visit.prescribed)
        return final

    def missed_followups(self) -> Tuple[int, int]:
        """ Return the number of missed and kept followups for this Patient.

        Note: The return statement looks like:  return missed, kept

        >>> carol = Patient("Carol Loot", 44021721)
        >>> visits = []
        >>> visits.append(HospitalVisit(\
                datetime.date(2017, 10, 23),\
                99722708,\
                44021721,\
                "Dengue Fever",\
                "very poor",\
                "Sucralfate",\
                datetime.date(2017, 11, 30)\
            ))
        >>> visits.append(HospitalVisit(\
                datetime.date(2017, 11, 30),\
                99722708,\
                44021721,\
                "Dengue Fever",\
                "very poor",\
                "Sucralfate",\
                datetime.date(2017, 12, 2)\
            ))
        >>> carol.history.extend(visits)
        >>> carol.missed_followups()
        (1, 1)
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/janonly/")
        >>> hosp.patients[3].missed_followups()
        (4, 3)
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/year97/")
        >>> hosp.patients[66].missed_followups()
        (12, 1)
        """
        follow_ups = []
        for visit in self.history:
            if visit.followup_date is not None:
                follow_ups.append(visit.followup_date)
        kept = 0
        not_kept = 0
        for follow_up in follow_ups:
            temp = 0
            for visit in self.history:
                if visit.date == follow_up:
                    temp += 1
            if temp == 1:
                kept += 1
            else:
                not_kept += 1
        return not_kept, kept


class Hospital:
    """ An object for modelling the daily operation of a hospital with doctors
    and patients.

    Public Attributes
    =================
    address: A human readable hospital's address.
    doctors: Doctors working at this hospital.
    patients: Patients who have visited this hospital.
    attendance: A daily record of doctors who showed up for work.
    admissions: A daily record of hospital visits to the hospital.
    load_schedules: Updates doctors schedules from a file.
    load_admissions: Update admissions from a file.
    load_attendance: Updates attendance from a file.
    load_doctors: Update self.attendance from a file.
    load_patients: Update self.patients from a file.

    Sample Usage
    ============
    >>> hosp = Hospital('123 Fake St.')
    >>> hosp.address
    '123 Fake St.'
    """

    address: str
    doctors: List[Doctor]
    patients: List[Patient]
    attendance: Dict[datetime.date, List[str]]
    admissions: Dict[datetime.date, List[HospitalVisit]]

    def __init__(self, address: str) -> None:
        """ Create a new Hospital with the given parameters."""
        self.address = address

        self.doctors = []
        self.patients = []

        self.attendance = {}
        self.admissions = defaultdict(lambda: [])

    def __repr__(self) -> str:
        """ Return a human-readable representation of this object.
        Do not modify this! This is not to be used to reconstruct the object.
        """
        return "Hospital on "+self.address

    def load_doctors(self, file_name: str) -> None:
        """
        Update this Hospital's doctors attribute to include the doctors from the
        file <file_name>.

        <file_name> is a csv with lines that look like:
            99064054,Brian Hazlett,1070.33
            id-number,First-name Last-name,salary-per-day

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_doctors("data/year97/doctors.csv")
        """
        return loaddata.load_doctors(self, file_name)

    def load_patients(self, file_name: str) -> None:
        """
        Update this Hospital's patients attribute to include the patients from
        the file <file_name>.

        <file_name> is a csv where each line has the following format:
            id-number,First-name Last-name,salary-per-day
        For instance:
            99064054,Brian Hazlett,1070.33

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_patients("data/year97/patients.csv")
        """
        return loaddata.load_patients(self, file_name)

    def load_schedules(self, file_name: str) -> None:
        """
        Update the schedules for all the doctors from this Hospital, using the
        dates specified in the file <file_name>.

        The content of <file_name> has the following format:
            Firstname Lastname
            MM/DD/YYYY

        That is, <first name> <last name> followed by a NON-EMPTY sequence of
        dates in the form MM/DD/YYYY, followed by an empty line after each
        doctor's schedule dates.

        For instance:
            Alice Liddle
            01/22/2017
            03/19/2017

            Mikhail Varshavski
            01/23/2017
            04/03/2018

        Names and schedules that do not correspond to doctors from self.doctors
        are ignored. Otherwise, those doctors' schedule attributes are updated.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_doctors("data/year97/doctors.csv")
        >>> hosp.load_schedules("data/year97/schedule.dat")
        """
        docs = []
        for doctor in self.doctors:
            docs.append(doctor.name)
            for month in MONTH_ABBREV:
                doctor.schedule[month] = []
        file = open(file_name, 'r')
        status = False
        curr_doc = ''
        for line in file:
            if status is False and line[0:-1] in docs:
                curr_doc = line[0:-1]
                status = True
            elif status is True and not line == '\n':
                location = docs.index(curr_doc)
                self.doctors[location].schedule[
                    MONTH_ABBREV[int(line[0:2]) - 1]] \
                    += [datetime.date(int(line[6:]),
                                      int(line[0:2]), int(line[3:5]))]
            else:
                status = False

    def load_attendance(self, file_name: str) -> None:
        """
        Update the attendance records for this Hospital from <file_name>, a csv
        file.

        Lines of <file_name> have the following format:
            DD/MM/YYYY,firstname lastname,firstname lastname,...
        For example:
            01/08/2019,Alice Liddle,Bob Loot
            02/08/2019,Carol Bitter
        which indicates that on 01/08/2019, Dr. Alice Liddle and Dr. Bob Loot
        showed up for work, and on 02/08/2019 only Dr. Carol Bitter was working
        at the hospital on that day.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_doctors("data/year97/doctors.csv")
        >>> hosp.load_attendance("data/year97/attendance.dat")
        """
        loaddata.load_attendance(self, file_name)

    def load_admissions(self, file_name: str) -> None:
        """
        Update this Hospital and patient visits with dates from <file_name>, a
        csv with lines
         visit date, doctor id, patient id, diagnosis, prognosis, drug, followup
        where intake and followup are dates in the form MM/DD/YYYY.

        NOTE: This also updates the patients' visit history.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_doctors("data/year97/doctors.csv")
        >>> hosp.load_patients("data/year97/patients.csv")
        >>> hosp.load_admissions("data/year97/admissions.csv")
        """
        loaddata.load_admissions(self, file_name)

    def admit_patient(self, patient: Patient) -> None:
        """
        Add the <patient> to this Hospital's list of patients.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> carol = Patient("Carol Loot", 44021721)
        >>> hosp.admit_patient(carol)
        >>> sorted(hosp.patients)
        [Pid: 44021721]
        """
        self.patients.append(patient)

    def hire_doctor(self, doctor: Doctor) -> None:
        """
        Add the <doctor> to this Hospital's list of doctors.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> bob = Doctor("Bob Loot", 99021721, 1.0)
        >>> hosp.hire_doctor(bob)
        >>> hosp.doctors
        [Did: 99021721]
        """
        self.doctors.append(doctor)

    def projected_expenses(self) -> float:
        """
        Return the total expenses projected based on doctor schedules
        (not actual attendance!) and their daily pay.
        Namely:
        (number of days when the doctor is scheduled to work) * (daily salary)

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> round(hosp.projected_expenses(), 2)
        46381.67
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> round(hosp.projected_expenses(), 2)
        1368941.26
        """
        total = 0
        for doctor in self.doctors:
            for month in MONTH_ABBREV:
                total += doctor.salary * len(doctor.schedule[month])
        return total

    def actual_expenses(self) -> float:
        """
        Return the total cost of paying doctors for all the shifts they worked.
        That is to say, the cost of paying doctors according to the attendance
        rather than their schedules.

        Namely: return (number of days the doctor attended) * (daily salary)

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> round(hosp.actual_expenses(), 2)
        48502.41
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> round(hosp.actual_expenses(), 2)
        1349201.46
        """
        total = 0
        for day in self.attendance:
            for doctor in self.attendance[day]:
                for docs in self.doctors:
                    if docs.name == doctor:
                        total += docs.salary
        return total

    def reminders(self, date: datetime.date, delta: int) -> List[Patient]:
        """
        Return a list of patients that have follow-up days scheduled within
        <delta>-days of <date>.

        For instance: Wednesday and Thursday are within 2-days from Tuesday.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> sorted(hosp.reminders(datetime.date(2017,1,1), 2))
        [Pid: 44524416]
        >>> hosp.reminders(datetime.date(2018,11,1), 300)
        []
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> sorted(hosp.reminders(datetime.date(1997,10,17), 3)) \
            #doctest: +NORMALIZE_WHITESPACE
        [Pid: 44045550, Pid: 44070721, Pid: 44139185, Pid: 44172567,
         Pid: 44222838, Pid: 44248993, Pid: 44269262, Pid: 44358472,
         Pid: 44366714, Pid: 44964920]
        """
        follow_ups = []
        new_time = date + datetime.timedelta(delta)
        for patient in self.patients:
            for visit in patient.history:
                if visit.followup_date is not None and \
                        date <= visit.followup_date <= new_time:
                    follow_ups.append(patient)
        return follow_ups

    def patients_seen(self, doctor: Doctor, start_date: datetime.date,
                      end_date: datetime.date) -> int:
        """
        Return the NUMBER of unique patients who visited <doctor> during
        <start_date> to <end_date> (inclusive).

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> d1 = datetime.date(2017, 1, 1)
        >>> d2 = datetime.date(2017, 1, 31)
        >>> bob = hosp.doctors[0]
        >>> hosp.patients_seen(bob, d1, d2)
        8
        >>> alice = hosp.doctors[-1]
        >>> hosp.patients_seen(alice, d1, d2)
        7
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> d1 = datetime.date(1997, 1, 1)
        >>> d2 = datetime.date(1997, 2, 1)
        >>> bob = hosp.doctors[2]
        >>> hosp.patients_seen(bob, d1, d2)
        8
        """
        total = 0
        temp_list = []
        for patient in self.patients:
            for visit in patient.history:
                if visit.doctor_id == doctor.id \
                        and start_date <= visit.date <= end_date \
                        and patient not in temp_list:
                    total += 1
                    temp_list.append(patient)
        return total

    def busiest_doctors(self, start_date: datetime.date,
                        end_date: datetime.date) -> List[Doctor]:
        """
        Return the list of doctors (in any order) who have ATTENDED TO the most
        UNIQUE patients during <start_date> to <end_date> inclusive.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> d1 = datetime.date(2017, 1, 1)
        >>> d2 = datetime.date(2017, 1, 3)
        >>> sorted(hosp.busiest_doctors(d1, d2))
        [Did: 99591940]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> d1 = datetime.date(1997, 1, 1)
        >>> d2 = datetime.date(1997, 2, 1)
        >>> sorted(hosp.busiest_doctors(d1, d2))
        [Did: 99298240, Did: 99817905]
        """
        # overly complicated code
        doc_nums = {}
        # Adding doctors to the dictionary
        for doctor in self.doctors:
            doc_nums[doctor.id] = 0
        # checking the visits
        for people in self.patients:
            for visit in people.history:
                for doctor in self.doctors:
                    if visit.doctor_id == doctor.id and \
                            start_date <= visit.date <= end_date:
                        doc_nums[doctor.id] += 1
        highest = []
        high = 0
        for doctor in self.doctors:
            for ids in doc_nums:
                if ids == doctor.id and doc_nums[ids] == high:
                    highest.append(doctor)
                elif ids == doctor.id and doc_nums[ids] > high:
                    high = doc_nums[ids]
                    highest = [doctor]
        return highest

    def coverage(self, bob: Doctor, alice: Doctor) -> List[datetime.date]:
        """
        Return the dates where Dr <bob> covered for Dr <alice>.

        Definition (Covered):
        <bob> COVERED FOR <alice> on day X if and only if
           1/  <bob> was not scheduled to work on day X, and
           2/  <bob> is on the attendance roll for day X, and
           3/  <alice> was sick on day X.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> bob = hosp.doctors[0]
        >>> alice = hosp.doctors[9]
        >>> sorted(hosp.coverage(bob, alice))
        [datetime.date(2017, 1, 16)]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> bob = hosp.doctors[1]
        >>> alice = hosp.doctors[3]
        >>> sorted(hosp.coverage(bob, alice)) #doctest: +NORMALIZE_WHITESPACE
        [datetime.date(1997, 12, 19), datetime.date(1997, 12, 25)]
        """
        final = []
        for day in self.attendance:
            for month in alice.schedule:
                if day in alice.schedule[month] and \
                        bob.name in self.attendance[day] and alice.name\
                        not in self.attendance[day]:
                    final.append(day)
        return final

    def sick_days(self, doctor: Doctor) -> List[datetime.date]:
        """
        Return the days <doctor> was sick.

        Definition (Sick):
        <doctor> is SICK on a day X when
           1/  <doctor> is scheduled to work on day X, and
           2/  <doctor> is NOT on attendance roll.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> alice = hosp.doctors[0]
        >>> hosp.sick_days(alice)
        [datetime.date(2017, 1, 19)]
        >>> bob = hosp.doctors[1]
        >>> sorted(hosp.sick_days(bob))
        [datetime.date(2017, 1, 27)]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> bob = hosp.doctors[1]
        >>> sorted(hosp.sick_days(bob)) #doctest: +NORMALIZE_WHITESPACE
        [datetime.date(1997, 2, 21), datetime.date(1997, 2, 28),
         datetime.date(1997, 5, 1), datetime.date(1997, 8, 20),
         datetime.date(1997, 9, 2), datetime.date(1997, 10, 13)]
        """
        final = []
        for months in doctor.schedule:
            for day in doctor.schedule[months]:
                for assigned in self.attendance:
                    if day == assigned and doctor.name not \
                            in self.attendance[assigned]:
                        final.append(day)
        return final

    def attended_to(self, patient: Patient) -> List[Doctor]:
        """
        Return a list of the unique doctors who have attended to <patient>.

        Definition (Attended):
        Supposing
           1/  visit is from <patient>.history, and
           2/  Dr Bob's ID number is visit.doctor_id
        then Dr Bob has ATTENDED TO <patient>.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> pat = hosp.patients[2]
        >>> sorted(hosp.attended_to(pat)) #doctest: +NORMALIZE_WHITESPACE
        [Did: 99155138, Did: 99292599, Did: 99354970, Did: 99591940,
         Did: 99670080, Did: 99868960]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> pat = hosp.patients[0]
        >>> sorted(hosp.attended_to(pat)) #doctest: +NORMALIZE_WHITESPACE
        [Did: 99043690, Did: 99145586, Did: 99261152, Did: 99298240,
         Did: 99577919, Did: 99630377, Did: 99817905, Did: 99991977]
        """
        final = []
        for visit in patient.history:
            if visit.doctor_id not in final:
                final.append(visit.doctor_id)
        srsly_final = []
        for doctor in self.doctors:
            if doctor.id in final:
                srsly_final.append(doctor)
        return srsly_final

    def prescribed_rate(self, doctor: Doctor, medication: str) -> float:
        """
        Return the prescription rate for <doctor> given <medication>.

        Definition (Prescription Rate):
        For visits = [all hospital visits with visit.doctor_id == <doctor>.id]
        PRESCRIPTION RATE for <doctor> is:
           number of visits where <medication> was prescribed
           ----------------------------------------------------- * 100
           number of visits where ANY medication was prescribed

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> round(hosp.prescribed_rate(hosp.doctors[3], 'Meperidine'), 2)
        12.5
        >>> hosp.prescribed_rate(hosp.doctors[3], 'Lithium')
        0.0
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> round(hosp.prescribed_rate(hosp.doctors[1], 'Amiodarone HCl'), 2)
        2.47
        """
        medi_yes = 0
        medi_any = 0
        for patients in self.patients:
            for visit in patients.history:
                if visit.doctor_id == doctor.id and \
                        visit.prescribed == medication:
                    medi_any += 1
                    medi_yes += 1
                elif visit.doctor_id == doctor.id and \
                        visit.prescribed is not None:
                    medi_any += 1
        return (medi_yes / medi_any) * 100


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': [
            'loaddata.load_doctors',
            'loaddata.load_patients',
            'loaddata.load_admissions',
            'loaddata.load_attendance',
            'loaddata.read_hospital',
            'load_schedules'
            ],
        'allowed-import-modules': [
            'doctest',
            'python_ta',
            'datetime',
            'typing',
            'collections',
            'loaddata',
            '__future__'
        ],
        'max-attributes': 15,
        'max-nested-blocks': 4,
        'max-args': 8,
    })
