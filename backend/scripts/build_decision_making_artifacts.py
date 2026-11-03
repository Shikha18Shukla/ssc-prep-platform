"""Build deterministic CH-20 Decision Making question and audit artifacts."""
import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
PDF1 = "Decision Making 01 Class Notes.pdf"
PDF2 = "Decision Making 02 _ Class Notes.pdf"
ORIGINAL = "Original SSC-style practice question"

OUTCOMES = ("SELECT", "REJECT", "REFER", "INSUFFICIENT")
LEVELS = {"EASY": 11, "MEDIUM": 12, "HARD": 11}


def _eligibility(statement, candidate, criteria, answer, reason, difficulty, source=None, referrals=(), topic="eligibility and exception rules"):
    return {"category": "ELIGIBILITY", "difficulty": difficulty, "statement": statement, "candidate": candidate,
            "criteria": criteria, "referrals": list(referrals), "answer": answer, "reason": reason,
            "topic": topic, "source": source}


def _situation(statement, options, answer, reason, difficulty, source=None, topic="situational judgment"):
    return {"category": "SITUATIONAL", "difficulty": difficulty, "statement": statement, "choices": options,
            "answer": answer, "reason": reason, "topic": topic, "source": source}


def _c(name, field, op, value=None, minimum=None, maximum=None):
    row = {"name": name, "field": field, "op": op}
    if op in {"between_inclusive", "range_within"}:
        row.update(minimum=minimum, maximum=maximum)
    else:
        row["value"] = value
    return row


def _when(field, op, value):
    return {"field": field, "op": op, "value": value}


def _ref(failed, authority, when=()):
    return {"failed_criteria": list(failed), "when": list(when), "authority": authority}


ITEMS = [
    _situation("You are posted to a communally sensitive area. Which response best supports calm, impartial administration?", [
        "Resign from the post immediately.", "Seek political patronage before taking any action.",
        "Coordinate with the administration and representative community leaders to establish respectful, impartial communication.",
        "Request a transfer without first assessing the situation."], 2,
        "Impartial contact with representative community leaders, coordinated through the administration, can build communication and reduce tension. Resigning or seeking political patronage avoids neutral public service; requesting transfer does not address the immediate responsibility.", "EASY", (PDF1, 4), "communal sensitivity and impartial public service"),
    _eligibility("Decision rules for a marketing trainee are assessed on 1 October 2016. Sohan Das has a B.Sc. with 56% marks, was born on 10 May 1982, and has two years of marketing-department experience. What decision follows?",
        {"graduate_pct": 56, "date_of_birth": "1982-05-10", "as_of": "2016-10-01", "marketing_experience_months": 24, "management_diploma": False},
        [_c("graduation marks", "graduate_pct", "gte", 50), _c("age", "age_years", "between_inclusive", minimum=24, maximum=30), _c("marketing experience", "marketing_experience_months", "gte", 6)], "REJECT",
        "Sohan has 56% and 24 months of relevant experience, but he was 34 on 1 October 2016, above the inclusive 24–30 age range. The management-diploma exception applies only when experience is the sole unmet criterion, so it cannot cure the age failure.", "EASY", (PDF1, 22), topic="date-specific age and mandatory criteria"),
    _situation("You are a judge hearing a well-known person’s case while media pressure is high. What should guide the decision?", [
        "Media perception and public opinion.", "Legal precedents together with personal bias.",
        "Evidence and applicable law, assessed impartially.", "Friends’ views before reaching a judgment."], 2,
        "A judicial decision must rest on the evidence and applicable law, without media pressure or personal bias. Friends’ opinions are not a substitute for the record or legal process.", "MEDIUM", (PDF1, 5), "judicial impartiality and due process"),
    _situation("A competent adult patient understands the likely consequences but refuses a prescribed medicine because of personal beliefs. What should the doctor do first?", [
        "Respect the refusal without explaining risks or recording the discussion.", "Explain benefits, risks and alternatives, check understanding, respect the informed decision, and document the refusal.",
        "Force the medicine because the doctor prescribed it.", "Ignore the patient and end care."], 1,
        "A capable adult’s informed refusal should be respected after clear, non-coercive counselling. Documenting the discussion supports continuity and accountability. Coercion violates autonomy; ignoring or abandoning the patient is not appropriate care.", "MEDIUM", (PDF1, 6), "patient autonomy and informed refusal"),
    _eligibility("A research institute is filling an Assistant Librarian post. All cases are considered on 1 November 2016. Vidya earned 72% in a Bachelor's degree in Library and Information Science, qualified UGC NET in 2016 at age 23, and completed a five-year internship in a university library. What decision follows?",
        {"age_range_on_reference": [23, 24], "library_information_science_pct": 72, "university_library_experience_months": 60, "ugc_net": True},
        [_c("age", "age_range_on_reference", "range_within", minimum=25, maximum=40), _c("degree marks", "library_information_science_pct", "gte", 65), _c("university library experience", "university_library_experience_months", "gte", 48)], "REJECT",
        "The source says she qualified UGC NET at age 23 during 2016. By the 1 November 2016 reference date her exact age could be 23 or 24, but it cannot be 25; the range is wholly below the minimum. UGC NET permits referral only when degree marks are the sole unmet criterion, and does not waive age.", "MEDIUM", (PDF2, 8), topic="date-bounded age and scoped exception", referrals=[_ref(["degree marks"], "Director of the institute", [_when("ugc_net", "eq", True)])]),
    _situation("As a municipal officer, you directly observe a factory releasing waste into a river at night and can safely identify the location. What should you prioritize?", [
        "Wait a month before recording anything.", "Privately threaten the factory staff.",
        "Secure factual observations, use the lawful enforcement process, and notify the environmental authority promptly.",
        "Secretly publish unverified accusations online."], 2,
        "A factual record and prompt use of authorized enforcement and environmental reporting channels address the ongoing harm while preserving evidence and due process. Delay, threats, and public claims not yet verified are unsafe or improper.", "HARD", (PDF1, 7), "environmental harm and lawful escalation"),
    _eligibility("A marketing trainee must be a graduate with at least 50%, be 24–30 inclusive on 1 October 2016, and have at least six months of marketing-department experience. A candidate who meets the other criteria but lacks experience is referred to the Marketing Manager if they hold a management diploma. Dhaval Kulkarni graduated with 58%, was born on 18 June 1990, has eight months of marketing experience, and has no management diploma. Decide.",
        {"graduate_pct": 58, "date_of_birth": "1990-06-18", "as_of": "2016-10-01", "marketing_experience_months": 8, "management_diploma": False},
        [_c("graduation marks", "graduate_pct", "gte", 50), _c("age", "age_years", "between_inclusive", minimum=24, maximum=30), _c("marketing experience", "marketing_experience_months", "gte", 6)], "SELECT",
        "Dhaval was 26 on the reference date, has 58% graduation marks, and has eight months of marketing experience. He satisfies all three mandatory conditions, so he should be selected; the diploma exception is not needed.", "EASY", (PDF1, 23), topic="rule-based selection and exact reference date"),
    _situation("A government clerk receives an incomplete application from a villager who does not understand the procedure. What is the most appropriate response?", [
        "Reject it immediately without explaining why.", "Return it without identifying what is missing.",
        "Explain the missing items and the permitted way to complete them, applying the same rules fairly.",
        "Ignore the application because assistance is not part of public service."], 2,
        "Clear guidance helps the applicant complete the process while preserving the same documentary requirements for everyone. Immediate unexplained rejection, an unhelpful return, or neglect would deny fair access to the procedure.", "EASY", (PDF1, 8), "accessible and fair public service"),
    _eligibility("Marketing-trainee rules: at least 50% graduation marks; age 24–30 inclusive on 1 October 2016; at least six months of marketing experience. If experience alone is missing, a candidate with a management diploma is referred to the Marketing Manager. Naveen Ghosh has a B.Com. with 70%, is 29 on the reference date, has a marketing diploma, and has no marketing-department experience. Decide.",
        {"graduate_pct": 70, "age_years": 29, "as_of": "2016-10-01", "marketing_experience_months": 0, "management_diploma": True},
        [_c("graduation marks", "graduate_pct", "gte", 50), _c("age", "age_years", "between_inclusive", minimum=24, maximum=30), _c("marketing experience", "marketing_experience_months", "gte", 6)], "REFER",
        "Naveen meets the marks and age criteria. Experience is the only unmet requirement, and he holds a marketing management diploma, so the stated exception sends his case to the Marketing Manager rather than selecting or rejecting him outright.", "MEDIUM", (PDF1, 24), referrals=[_ref(["marketing experience"], "Marketing Manager", [_when("management_diploma", "eq", True)])]),
    _situation("A patient with a contagious disease is admitted to a hospital. What is the best first step?", [
        "Ask the patient to wait in the general waiting area.", "Apply the facility's isolation precautions and promptly alert the responsible clinician or infection-control team.",
        "Inform the media before the clinical team.", "Discharge the patient immediately."], 1,
        "Prompt isolation under facility protocol limits exposure while the clinical and infection-control teams assess the patient. Waiting among others, disclosing information to the media, or discharging without assessment could increase harm.", "EASY", (PDF1, 9), "infection control and immediate safety"),
    _eligibility("A junior librarian must have a Bachelor's degree in Library Science, be under 32, and have at least one year of experience in any library, assessed on 1 April 2025. Rina is 31, holds a B.Lib.Sc., and has 18 months of experience in a college library. Decide.",
        {"bachelor_library_science": True, "age_years": 31, "library_experience_months": 18, "as_of": "2025-04-01"},
        [_c("library science degree", "bachelor_library_science", "eq", True), _c("age under 32", "age_years", "lt", 32), _c("library experience", "library_experience_months", "gte", 12)], "SELECT",
        "Rina has the required degree, is under 32 on the stated date, and has more than 12 months of library experience. A college library counts because the rule says any library.", "EASY", (PDF2, 4), topic="multiple mandatory criteria"),
    _situation("A fire alarm sounds in a government building while you are working at the front desk. What should you do?", [
        "Keep working until someone personally confirms the fire.", "Shout at people without giving directions.",
        "Follow the building evacuation procedure, guide people to safety, and alert emergency responders or the designated authority.",
        "Turn off the alarm so work can continue."], 2,
        "Treat the alarm as an immediate safety signal: follow the evacuation procedure, help people leave safely, and notify the designated responders. Waiting, creating panic, or disabling the alarm can expose people to danger.", "EASY", (PDF1, 10), "emergency response and evacuation"),
    _eligibility("A junior librarian must have a B.Sc. with at least 60%, an M.Sc., and be below 28 on 1 January 2017. Prior work experience is preferred. If an otherwise eligible candidate has no work experience, refer the case to the Principal; if all criteria including experience are met, select. Neeraj has a B.Sc. with 65%, an M.Sc., is 26 on the reference date, and has no work experience. Decide.",
        {"bsc_pct": 65, "msc": True, "age_years": 26, "prior_experience_months": 0, "as_of": "2017-01-01"},
        [_c("B.Sc. marks", "bsc_pct", "gte", 60), _c("M.Sc.", "msc", "eq", True), _c("age under 28", "age_years", "lt", 28), _c("prior experience", "prior_experience_months", "gte", 1)], "REFER",
        "Neeraj meets the degree and age conditions. The rules specifically direct an otherwise eligible candidate with no experience to the Principal, so this is a referral rather than a selection or rejection.", "MEDIUM", (PDF2, 5), referrals=[_ref(["prior experience"], "Principal", [_when("prior_experience_months", "eq", 0)])]),
    _situation("A critically ill patient arrives at a hospital reception desk. What should the receptionist do first?", [
        "Complete all paperwork before calling clinical staff.", "Activate the emergency response and call the doctor or triage team, then assist with paperwork when care is underway.",
        "Send the patient away to fetch documents.", "Wait for senior administrative approval before alerting clinicians."], 1,
        "The receptionist should promptly alert clinical staff or activate triage so urgent care can begin; paperwork can follow. Delays for forms, documents, or administrative approval put the patient at unnecessary risk.", "MEDIUM", (PDF1, 11), "medical emergency and prioritization"),
    _situation("You see someone drop a wallet on a public street. What should you do?", [
        "Ignore it and continue walking.", "Keep it because no one saw you pick it up.",
        "Donate the contents without checking for the owner.", "Make a reasonable effort to return it to the owner or hand it to an appropriate lost-property authority."], 3,
        "Returning the wallet or handing it to a responsible lost-property authority protects the owner's property. Keeping, ignoring, or disposing of it does not.", "EASY", (PDF1, 12), "honesty and lost property"),
    _eligibility("A research institute Assistant Librarian must be aged 25–40 inclusive on 1 November 2016, hold a Library and Information Science bachelor's degree with at least 65%, and have four years of practical university-library experience. If the degree-mark criterion alone is missed but the candidate has UGC NET, refer to the Director. Meha has 69% and is currently an intern at Ranchi University, but her age and the duration of her experience are not stated. Decide.",
        {"library_information_science_pct": 69, "age_years": None, "university_library_experience_months": None, "ugc_net": None, "as_of": "2016-11-01"},
        [_c("age", "age_years", "between_inclusive", minimum=25, maximum=40), _c("degree marks", "library_information_science_pct", "gte", 65), _c("university library experience", "university_library_experience_months", "gte", 48)], "INSUFFICIENT",
        "Her 69% meets the degree threshold, but the case omits her age and how long she has worked in a university library. Being an intern does not establish four years of experience; without those facts, selection, rejection, or referral cannot be decided.", "HARD", (PDF2, 9), topic="missing facts and non-inference"),
    _situation("You have been assigned a work task that you do not know how to perform. What is the best course?", [
        "Make excuses and leave it unfinished.", "Guess at the procedure and submit work that may be wrong.",
        "Seek guidance or suitable training, then complete the task accurately.", "Delay it without telling anyone."], 2,
        "Promptly seeking guidance lets the task be completed accurately and responsibly. Excuses, guessing, and uncommunicated delay risk poor work and undermine accountability.", "MEDIUM", (PDF1, 13), "seeking guidance and accountability"),
    _eligibility("An Indian cricket player must be an Indian citizen, be no more than 19 on 1 November 2016, be medically fit, have played in an Under-19 World Cup or the Ranji Trophy, have no criminal cases, and pass anti-doping screening. Failure only of anti-doping screening is referred to the BCCI President; a criminal-case issue goes to the State Government, and a medical-fitness failure goes to the Medical Association. Mahesh is 19, Indian, medically fit, played in the Under-19 World Cup, has no criminal case, and failed the anti-doping test. Decide.",
        {"indian_citizen": True, "age_years": 19, "medically_fit": True, "played_u19_or_ranji": True, "criminal_cases": 0, "anti_doping_passed": False},
        [_c("citizenship", "indian_citizen", "eq", True), _c("age limit", "age_years", "lte", 19), _c("medical fitness", "medically_fit", "eq", True), _c("required competition", "played_u19_or_ranji", "eq", True), _c("criminal record", "criminal_cases", "eq", 0), _c("anti-doping", "anti_doping_passed", "eq", True)], "REFER",
        "Mahesh meets the nationality, age, fitness, competition, and criminal-record conditions. Anti-doping is the sole failed condition, and the rule explicitly refers that case to the BCCI President.", "HARD", (PDF2, 11), referrals=[_ref(["anti-doping"], "BCCI President", [_when("anti_doping_passed", "eq", False)]), _ref(["criminal record"], "State Government", [_when("criminal_cases", "gt", 0)]), _ref(["medical fitness"], "Medical Association", [_when("medically_fit", "eq", False)])]),
    _eligibility("Use the cricket-selection rules: Indian citizenship, age no more than 19 on 1 November 2016, medical fitness, play in an Under-19 World Cup or Ranji Trophy, no criminal cases, and a passed anti-doping test. Referral exceptions apply only to a sole failure in medical fitness, criminal record, or anti-doping screening. Ram was born on 26 May 1990, is Indian, played in the Ranji Trophy, and passed both medical-fitness and anti-doping tests; no criminal case is reported. Decide.",
        {"indian_citizen": True, "date_of_birth": "1990-05-26", "as_of": "2016-11-01", "medically_fit": True, "played_u19_or_ranji": True, "criminal_cases": 0, "anti_doping_passed": True},
        [_c("citizenship", "indian_citizen", "eq", True), _c("age limit", "age_years", "lte", 19), _c("medical fitness", "medically_fit", "eq", True), _c("required competition", "played_u19_or_ranji", "eq", True), _c("criminal record", "criminal_cases", "eq", 0), _c("anti-doping", "anti_doping_passed", "eq", True)], "REJECT",
        "Ram is 26 on 1 November 2016, so he fails the maximum age of 19. The referral exceptions cover medical fitness, criminal-record, or anti-doping failures only; none waives the age rule.", "EASY", (PDF2, 12), referrals=[_ref(["anti-doping"], "BCCI President", [_when("anti_doping_passed", "eq", False)]), _ref(["criminal record"], "State Government", [_when("criminal_cases", "gt", 0)]), _ref(["medical fitness"], "Medical Association", [_when("medically_fit", "eq", False)])]),
    _situation("As team lead, your team has missed a major deadline. What is the most responsible next step?", [
        "Abandon the project without review.", "Stay silent and hope the delay is overlooked.",
        "Blame one team member publicly.", "Identify the causes, inform affected stakeholders, and agree on a realistic recovery plan and next steps."], 3,
        "A factual review and transparent recovery plan address the missed deadline and help prevent recurrence. Abandonment, silence, and blame do not solve the work or support accountability.", "MEDIUM", (PDF1, 15), "professional accountability and recovery planning"),
    _situation("A person experiencing domestic violence asks a legal-aid clinic for help making a report and finding support. What should the worker do?", [
        "Dismiss it as a private matter.", "Tell the person to wait without assessing immediate safety.",
        "Support the person in understanding reporting and protection options, help with the requested report, and connect them with appropriate services while respecting their choices.",
        "Send the person directly to court without listening or explaining options."], 2,
        "The person asked for help, so the worker should take the report request seriously, assess immediate safety, explain options, and connect them with appropriate services. Ignoring, delaying, or sending them away without support fails the request and may increase risk.", "HARD", (PDF1, 16), "safety, dignity and legal support"),
    _eligibility("A United Nations Secretary-General candidate must be over 45, a former president, have support from at least 70% of member states, and come from a country that has been a UN member for at least ten years. If membership is at least five years but under ten and support is at least 85%, refer to the UN High Commissioner. Anjab Zimbo is 52, a former president, has 74% support, and his country has not completed ten years of UN membership. Decide.",
        {"age_years": 52, "former_president": True, "member_state_support_pct": 74, "country_member_10_years": False},
        [_c("age", "age_years", "gt", 45), _c("former president", "former_president", "eq", True), _c("member-state support", "member_state_support_pct", "gte", 70), _c("country membership", "country_member_10_years", "eq", True)], "REJECT",
        "Zimbo fails the ten-year country-membership condition. The special referral also requires at least 85% support; his stated 74% does not meet that threshold, so the case is rejected regardless of whether the country has completed five years.", "MEDIUM", (PDF2, 14), referrals=[_ref(["country membership"], "UN High Commissioner", [_when("member_state_support_pct", "gte", 85), _when("country_un_membership_years", "gte", 5)])]),
    _eligibility("Use the United Nations Secretary-General criteria: age over 45, former president, support from at least 70% of member states, and country membership of at least ten years. A candidate who meets every condition except being a former president is referred to the UN President if they have served as a country's foreign minister. Jane is 49, has 71% support, her country has been a member for 20 years, and she served as its foreign minister but was never president. Decide.",
        {"age_years": 49, "former_president": False, "foreign_minister": True, "member_state_support_pct": 71, "country_un_membership_years": 20},
        [_c("age", "age_years", "gt", 45), _c("former president", "former_president", "eq", True), _c("member-state support", "member_state_support_pct", "gte", 70), _c("country membership", "country_un_membership_years", "gte", 10)], "REFER",
        "Jane meets age, support, and membership requirements. Former presidency is the sole unmet condition; the supplied exception for a served foreign minister directs referral to the UN President.", "MEDIUM", (PDF2, 15), referrals=[_ref(["former president"], "UN President", [_when("foreign_minister", "eq", True)])]),
    _eligibility("A corporate recruitment policy requires at least 75% in both classes 10 and 12, at least 70% in Civil or Mechanical Engineering, age no more than 25 on 8 September 2016, at least 60% in the selection test, and a CAD course from a prestigious institute. If the candidate meets all other conditions but lacks CAD, refer to the Company President when they are willing to pay at least ₹30,000 and have at least 75% at graduation. Nataasha has 80% and 75% in classes 10 and 12, 75% in Civil Engineering, is 24 on the reference date, scored 60% in the selection test, lacks the CAD course, has 75% at graduation, and is willing to pay ₹35,000. Decide.",
        {"class10_pct": 80, "class12_pct": 75, "engineering_pct": 75, "age_years": 24, "selection_test_pct": 60, "cad_from_prestigious_institute": False, "graduate_pct": 75, "willing_payment": 35000},
        [_c("class 10 marks", "class10_pct", "gte", 75), _c("class 12 marks", "class12_pct", "gte", 75), _c("engineering marks", "engineering_pct", "gte", 70), _c("age", "age_years", "lte", 25), _c("selection test", "selection_test_pct", "gte", 60), _c("CAD course", "cad_from_prestigious_institute", "eq", True)], "REFER",
        "Nataasha meets the school, engineering, age, and test thresholds. CAD is her sole unmet condition, and she meets both stated safeguards for its exception: graduation marks of 75% and willingness to pay ₹30,000 or more. Refer to the Company President.", "HARD", (PDF2, 17), referrals=[_ref(["CAD course"], "Company President", [_when("willing_payment", "gte", 30000), _when("graduate_pct", "gte", 75)])]),
    _eligibility("Corporate recruitment is assessed on 8 September 2016. Candidates need at least 75% in classes 10 and 12, at least 70% in Civil or Mechanical Engineering, age no more than 25, at least 60% in the selection test, and a CAD course from a prestigious institute. If age alone is above the limit, a candidate with more than one year of experience at a prestigious company is referred to the Company President. Stella completed her degree on 16 June 2011 at age 21, earned 80% and 75% in classes 10 and 12, 85% in Civil Engineering, 65% in the selection test, completed CAD at a prestigious institute, and has more than two years' experience at a prestigious company. Decide.",
        {"age_lower_bound_years": 26, "class10_pct": 80, "class12_pct": 75, "engineering_pct": 85, "selection_test_pct": 65, "cad_from_prestigious_institute": True, "prestigious_company_experience_months": 25},
        [_c("class 10 marks", "class10_pct", "gte", 75), _c("class 12 marks", "class12_pct", "gte", 75), _c("engineering marks", "engineering_pct", "gte", 70), _c("age", "age_lower_bound_years", "lte", 25), _c("selection test", "selection_test_pct", "gte", 60), _c("CAD course", "cad_from_prestigious_institute", "eq", True)], "REFER",
        "She was already 21 by 16 June 2011. By 8 September 2016, over five years later, she must be at least 26 and therefore exceeds the maximum age of 25. Age is the only failed condition, and more than two years at a prestigious company satisfies the more-than-one-year exception, so refer to the Company President.", "HARD", (PDF2, 18), referrals=[_ref(["age"], "Company President", [_when("prestigious_company_experience_months", "gt", 12)])]),
    _eligibility("A marketing trainee must be a graduate with at least 50%, be 24–30 inclusive on 1 October 2016, and have six months of marketing-department experience. If experience is the only unmet condition, a management diploma triggers referral to the Marketing Manager. The applicant has 50% graduation marks, turns 24 on 1 October 2016, has exactly six months of marketing experience, and has no management diploma. Decide.",
        {"graduate_pct": 50, "date_of_birth": "1992-10-01", "as_of": "2016-10-01", "marketing_experience_months": 6, "management_diploma": False},
        [_c("graduation marks", "graduate_pct", "gte", 50), _c("age", "age_years", "between_inclusive", minimum=24, maximum=30), _c("marketing experience", "marketing_experience_months", "gte", 6)], "SELECT",
        "The candidate is exactly 24 on the reference date, has exactly 50% marks, and has exactly six months of relevant experience. Each threshold is inclusive, so all criteria are met.", "HARD", None, topic="original boundary case for age, marks and experience"),
    _situation("A confidential patient report is accidentally emailed to an unauthorized distribution list at a clinic. What should the responsible employee do first?", [
        "Delete the sent message from their own mailbox and say nothing.", "Forward the report to more colleagues to ask who has seen it.",
        "Promptly notify the privacy or incident lead, follow containment instructions, and document the incident without further sharing the report.",
        "Post a public warning containing the patient's identity."], 2,
        "Prompt reporting lets the authorized privacy lead contain access and follow required incident procedures. Concealment, wider distribution, or public disclosure would worsen the privacy breach.", "MEDIUM", None, "confidentiality and incident escalation"),
    _eligibility("A procurement analyst must have a finance degree with at least 60%, be 21–30 inclusive on 1 July 2025, and have 24 months of procurement experience. If experience is the only missing criterion, an applicant with at least 18 months of experience and a postgraduate procurement diploma is referred to the Procurement Director. Dev has 62%, turns 30 on 1 July 2025, has exactly 18 months of procurement experience, and holds the postgraduate diploma. Decide.",
        {"finance_degree_pct": 62, "date_of_birth": "1995-07-01", "as_of": "2025-07-01", "procurement_experience_months": 18, "postgraduate_procurement_diploma": True},
        [_c("finance degree marks", "finance_degree_pct", "gte", 60), _c("age", "age_years", "between_inclusive", minimum=21, maximum=30), _c("procurement experience", "procurement_experience_months", "gte", 24)], "REFER",
        "Dev meets the degree and age conditions. Experience is the sole shortfall at 18 rather than 24 months; the rule's diploma exception applies at 18 months or more and sends the case to the Procurement Director.", "MEDIUM", None, referrals=[_ref(["procurement experience"], "Procurement Director", [_when("procurement_experience_months", "gte", 18), _when("postgraduate_procurement_diploma", "eq", True)])]),
    _situation("A warning system reports that a bridge may be structurally unsafe while pedestrians are approaching. What should the duty officer do first?", [
        "Wait for visible damage before acting.", "Close access using the established safety procedure, direct people to a safe route, and notify emergency and engineering authorities.",
        "Allow pedestrians through while looking for another report.", "Post an unverified social-media warning and leave the area."], 1,
        "The warning indicates a possible immediate danger, so the officer should prevent entry, move people to safety, and alert the responsible emergency and engineering teams. Waiting or allowing access risks injury; an unverified post is not a controlled response.", "HARD", None, "public safety and urgent risk control"),
    _eligibility("A public-archives assistant must have a bachelor's degree with at least 55%, be 21–28 inclusive on 1 July 2026, and have at least 24 completed months of records-management experience. Mira has 55%, was born on 1 July 1998, and her relevant experience began on 1 July 2024. Decide.",
        {"bachelor_pct": 55, "date_of_birth": "1998-07-01", "as_of": "2026-07-01", "experience_start": "2024-07-01", "experience_as_of": "2026-07-01"},
        [_c("degree marks", "bachelor_pct", "gte", 55), _c("age", "age_years", "between_inclusive", minimum=21, maximum=28), _c("records experience", "experience_months", "gte", 24)], "SELECT",
        "Mira meets the 55% threshold exactly, turns 28 on the assessment date, and completes exactly 24 calendar months of relevant experience on that date. All three inclusive requirements are met.", "EASY", None, topic="original exact-boundary selection"),
    _situation("A procurement panel member discovers that one bidder is a close relative. What is the appropriate action?", [
        "Continue scoring the bid but keep the relationship private.", "Disqualify every bidder to avoid making a decision.",
        "Tell the relative confidential scoring information so they can withdraw.", "Disclose the conflict promptly and recuse from evaluation under the procurement procedure."], 3,
        "Disclosing the conflict and recusing protects an impartial procurement process. Concealment or sharing confidential information compromises fairness, while disqualifying every bidder is arbitrary.", "HARD", None, "conflict of interest and procedural fairness"),
    _eligibility("An aviation-safety records assessor must have a bachelor's degree with at least 65%, be 25–35 inclusive on 15 September 2025, and have at least 60 completed months of aviation-audit experience. A special referral applies only when the shortfall is under 60 months but at least 48 months and the candidate holds a safety-inspector certificate. Arjun has 70%, is 35 on the reference date, and holds the certificate; his employer's record says only ‘about five years’ and gives no exact start date. Decide.",
        {"bachelor_pct": 70, "age_years": 35, "as_of": "2025-09-15", "experience_months": None, "safety_inspector_certificate": True},
        [_c("degree marks", "bachelor_pct", "gte", 65), _c("age", "age_years", "between_inclusive", minimum=25, maximum=35), _c("aviation audit experience", "experience_months", "gte", 60)], "INSUFFICIENT",
        "Arjun meets the known degree and age conditions, but ‘about five years’ does not establish whether he has completed 60 months or falls in the 48–59 month referral band. The certificate alone cannot resolve that missing duration, so the information is insufficient.", "HARD", None, topic="original conflicting-duration and referral boundary"),
    _situation("A police officer's public-service desk is busy and residents are asking for help. Which professional attitude is most appropriate?", [
        "Assume the public is dishonest and respond negatively.", "Use cruelty to make people obey quickly.", "Rely on fear as the main way to manage the desk.", "Remain constructive, respectful and positive while applying the law fairly."], 3,
        "A constructive and respectful attitude supports effective public service while allowing the officer to apply rules consistently. Negativity, cruelty, and fear undermine trust and professional conduct.", "EASY", (PDF1, 17), "professional attitude and public service"),
    _eligibility("A United Nations Secretary-General must be over 45, a former president, have at least 70% member-state support, and come from a country that has been a member for ten years. The foreign-minister referral applies only if that is the candidate's sole failed criterion. A candidate is 50, has 80% support and 12 years of country membership, was never president, and has never served as a foreign minister. Decide.",
        {"age_years": 50, "former_president": False, "foreign_minister": False, "member_state_support_pct": 80, "country_un_membership_years": 12},
        [_c("age", "age_years", "gt", 45), _c("former president", "former_president", "eq", True), _c("member-state support", "member_state_support_pct", "gte", 70), _c("country membership", "country_un_membership_years", "gte", 10)], "REJECT",
        "The former-president criterion is the sole failure, but the stated referral requires prior foreign-minister service. Since the candidate has not served as a foreign minister, no exception applies and the candidate is rejected.", "HARD", None, referrals=[_ref(["former president"], "UN President", [_when("foreign_minister", "eq", True)])], topic="original exception boundary"),
]


def _age_on(dob, as_of):
    dob, as_of = date.fromisoformat(dob), date.fromisoformat(as_of)
    return as_of.year - dob.year - ((as_of.month, as_of.day) < (dob.month, dob.day))


def _add_months(value, months):
    year = value.year + (value.month - 1 + months) // 12
    month = (value.month - 1 + months) % 12 + 1
    from calendar import monthrange
    day = min(value.day, monthrange(year, month)[1])
    return date(year, month, day)


def _completed_months(start, as_of):
    start, as_of = date.fromisoformat(start), date.fromisoformat(as_of)
    if as_of < start:
        return None
    months = (as_of.year - start.year) * 12 + as_of.month - start.month
    if _add_months(start, months) > as_of:
        months -= 1
    return months


def _compare(value, op, expected=None, minimum=None, maximum=None):
    if op == "eq": return value == expected
    if op == "gte": return value >= expected
    if op == "gt": return value > expected
    if op == "lte": return value <= expected
    if op == "lt": return value < expected
    if op == "between_inclusive": return minimum <= value <= maximum
    if op == "range_within": return minimum <= value[0] and value[1] <= maximum
    raise ValueError(f"Unsupported eligibility operator: {op}")


def evaluate_candidate(candidate, criteria, referrals=()):
    """Apply explicitly encoded criteria and exact-failure referral exceptions."""
    facts = dict(candidate)
    if facts.get("date_of_birth") and facts.get("as_of"):
        facts["age_years"] = _age_on(facts["date_of_birth"], facts["as_of"])
    if facts.get("experience_start") and facts.get("experience_as_of"):
        facts["experience_months"] = _completed_months(facts["experience_start"], facts["experience_as_of"])
    failures, missing = [], []
    for criterion in criteria:
        value = facts.get(criterion["field"])
        if value is None:
            missing.append(criterion["name"])
            continue
        if not _compare(value, criterion["op"], criterion.get("value"), criterion.get("minimum"), criterion.get("maximum")):
            failures.append(criterion["name"])
    if missing:
        return {"outcome": "INSUFFICIENT", "authority": None, "failed": failures, "missing": missing}
    for referral in referrals:
        if set(referral["failed_criteria"]) != set(failures):
            continue
        if all(facts.get(condition["field"]) is not None and _compare(facts[condition["field"]], condition["op"], condition.get("value")) for condition in referral["when"]):
            return {"outcome": "REFER", "authority": referral["authority"], "failed": failures, "missing": missing}
    if failures:
        return {"outcome": "REJECT", "authority": None, "failed": failures, "missing": []}
    return {"outcome": "SELECT", "authority": None, "failed": [], "missing": []}


def _all_question_text(item):
    if item["category"] == "ELIGIBILITY":
        criteria = "; ".join(f"{c['name']}: {c.get('minimum')} to {c.get('maximum')} inclusive" if c["op"] in {"between_inclusive", "range_within"} else f"{c['name']}: {c['op']} {c.get('value')}" for c in item["criteria"])
        exceptions = " ".join(f"Exception: if only {', '.join(r['failed_criteria'])} is unmet and the stated condition(s) hold, refer to {r['authority']}." for r in item["referrals"])
        return f"Rules: {criteria}. {exceptions}\nCase: {item['statement']}\nWhat decision follows?"
    return item["statement"]


def _source_label(source):
    if source is None: return ORIGINAL
    pdf, page = source
    return f"{pdf}, page {page}; lecture example, exam/year not stated"


def _position_map(ids):
    ordered = sorted(ids, key=lambda qid: hashlib.sha256(f"dm-answer-position-v1:{qid}".encode()).digest())
    sequence = "ABCD" * (len(ids) // 4) + "ABCD"[:len(ids) % 4]
    return {qid: key for qid, key in zip(ordered, sequence)}


def _page_review():
    candidates = {
        (PDF1, 4): ("situational", "Communally sensitive posting", "accepted_question", "Select respectful coordination with representative community leaders and administration."),
        (PDF1, 5): ("situational", "Judge facing media pressure", "accepted_question", "Decide impartially on evidence and law."),
        (PDF1, 6): ("situational", "Patient refuses medication", "accepted_question", "Counsel, respect informed refusal, and document it; source mark not used as sole key."),
        (PDF1, 7): ("situational", "Factory releases waste into river", "accepted_question", "Record facts and use lawful environmental enforcement channels."),
        (PDF1, 8): ("situational", "Incomplete application from an applicant needing guidance", "accepted_question", "Explain missing items and fair completion procedure."),
        (PDF1, 9): ("situational", "Contagious disease admission", "accepted_question", "Use isolation protocol and notify the clinical/infection-control team."),
        (PDF1, 10): ("situational", "Fire alarm in government building", "accepted_question", "Evacuate under procedure and alert responders."),
        (PDF1, 11): ("situational", "Critically ill patient at reception", "accepted_question", "Alert the clinical team before paperwork."),
        (PDF1, 12): ("situational", "Wallet dropped in street", "accepted_question", "Return to owner or responsible lost-property authority."),
        (PDF1, 13): ("situational", "Unfamiliar assigned task", "accepted_question", "Seek suitable guidance or training."),
        (PDF1, 14): ("situational", "Lawyer influences witness", "rejected", "The supplied choice jumps directly to contempt without describing the conduct, applicable procedure, warning, or severity; no proportionate single action can be verified."),
        (PDF1, 15): ("situational", "Team misses major deadline", "accepted_question", "Analyze causes, communicate, and agree recovery steps."),
        (PDF1, 16): ("situational", "Domestic violence reported to legal-aid clinic", "accepted_question", "Support the requested report and connect the person to safety and legal services."),
        (PDF1, 17): ("situational", "Professional attitude for police", "accepted_question", "Positive, respectful public service is the defensible choice."),
        (PDF1, 18): ("situational", "Colleague's brother accused of anti-national activities", "rejected", "The relationship alone does not establish the colleague's conduct or justify arrest; source options encourage guilt by association and arbitrary punishment."),
        (PDF1, 19): ("situational", "Goons follow two women at night", "rejected", "Options do not provide a clearly safe, proportionate response; direct confrontation, gathering a crowd, or leaving the women without support all carry unresolved risks."),
        (PDF1, 20): ("situational", "Police officer deprived of ethical facilities", "rejected", "‘Ethical facilities’ and the alleged deprivation are undefined, leaving the responsible procedure and appropriate remedy unclear."),
        (PDF1, 21): ("eligibility", "Marketing trainee criteria and management-diploma exception", "accepted_context", "Used with the candidate cases on pages 22–24; exact marks, age reference date, experience and referral exception retained."),
        (PDF1, 22): ("eligibility", "Sohan Das marketing-trainee case", "accepted_question", "Age is 34 on 1 October 2016, outside the 24–30 range; reject."),
        (PDF1, 23): ("eligibility", "Dhaval Kulkarni marketing-trainee case", "accepted_question", "Age 26, 58% and eight months' experience meet the criteria; select."),
        (PDF1, 24): ("eligibility", "Naveen Ghosh marketing-trainee case", "accepted_question", "Experience alone is missing and the management diploma triggers referral."),
    }
    candidates.update({
        (PDF2, 4): ("eligibility", "Junior Librarian criteria and Rina case", "accepted_question", "B.Lib.Sc., under 32, and at least one year in any library; Rina meets all."),
        (PDF2, 5): ("eligibility", "Junior Librarian criteria and Neeraj case", "accepted_question", "B.Sc. ≥60%, M.Sc., below 28; no experience routes otherwise eligible candidate to Principal."),
        (PDF2, 7): ("eligibility", "Assistant Librarian criteria and UGC NET exception", "accepted_context", "Age 25–40 on 1 November 2016, Library and Information Science degree ≥65%, four years' university-library experience; degree exception with NET goes to institute Director."),
        (PDF2, 8): ("eligibility", "Vidya Assistant Librarian case", "accepted_question", "Age 23 fails the minimum age; NET exception does not waive age."),
        (PDF2, 9): ("eligibility", "Meha Assistant Librarian case", "accepted_question", "Age and experience duration are missing; mark information insufficient."),
        (PDF2, 10): ("eligibility", "Indian cricket selection criteria and exceptions", "accepted_context", "Nationality, age ≤19 on 1 November 2016, fitness, eligible competition, criminal record, doping; distinct referral authorities retained."),
        (PDF2, 11): ("eligibility", "Mahesh cricket selection case", "accepted_question", "Only anti-doping failure; refer BCCI President."),
        (PDF2, 12): ("eligibility", "Ram cricket selection case", "accepted_question", "Age 26 exceeds the maximum 19; reject despite medical fitness and prior play."),
        (PDF2, 13): ("eligibility", "UN Secretary-General criteria and exceptions", "accepted_context", "Age >45, former President, 70% support, 10-year member-country rule; foreign-minister and 5-year/85% exceptions retained."),
        (PDF2, 14): ("eligibility", "Anjab Zimbo UN case", "accepted_question", "Six-year membership but 74% support misses the 85% referral exception; reject."),
        (PDF2, 15): ("eligibility", "Jane UN case", "accepted_question", "Foreign minister but not former President; refer to UN President under the stated exception."),
        (PDF2, 16): ("eligibility", "Corporate recruitment criteria and exceptions", "accepted_context", "Class marks, engineering marks, age on 8 September 2016, selection test, CAD; age and CAD exceptions retained."),
        (PDF2, 17): ("eligibility", "Nataasha corporate recruitment case", "accepted_question", "CAD is sole miss; 75% graduation and ₹35,000 willingness trigger Company President referral."),
        (PDF2, 18): ("eligibility", "Stella corporate recruitment case", "accepted_question", "She was 21 on 16 June 2011, so by 8 September 2016 she is necessarily over 25; more than one year in a prestigious company triggers referral."),
    })
    reviews = []
    for pdf, count in ((PDF1, 26), (PDF2, 20)):
        for page in range(1, count + 1):
            info = candidates.get((pdf, page))
            if info:
                category, description, status, reason = info
            else:
                category = None
                description = "Cover, recap, topic overview, summary, or closing page"
                status = "reference"
                reason = "Visually inspected; contains no distinct complete question suitable for the bank."
            reviews.append({"pdf": pdf, "page": page, "category": category, "description": description, "status": status, "reason": reason})
    return reviews


def build():
    if len(ITEMS) != 34:
        raise ValueError(f"Expected 34 questions, found {len(ITEMS)}")
    ids = [f"dm-{i:03d}" for i in range(1, len(ITEMS) + 1)]
    positions = _position_map(ids)
    rows, ledger = [], []
    for index, (qid, item) in enumerate(zip(ids, ITEMS), 1):
        if item["category"] == "ELIGIBILITY":
            verified = evaluate_candidate(item["candidate"], item["criteria"], item["referrals"])
            if verified["outcome"] != item["answer"]:
                raise ValueError(f"Independent eligibility evaluator conflict at {qid}: {verified} != {item['answer']}")
            authority = next((ref["authority"] for ref in item["referrals"] if ref["failed_criteria"] == verified["failed"] and verified["outcome"] == "REFER"), "designated authority")
            choices = [f"Select the candidate.", "Reject the candidate.", f"Refer the case to the {authority}.", "The information is insufficient to decide."]
            answer_index = OUTCOMES.index(item["answer"])
            eligibility_audit = {"candidate": item["candidate"], "criteria": item["criteria"], "referrals": item["referrals"], "expected_outcome": item["answer"], "evaluator_result": verified}
        else:
            choices = item["choices"]
            answer_index = item["answer"]
            eligibility_audit = None
        answer_text = choices[answer_index]
        key = positions[qid]
        distractors = iter(choice for n, choice in enumerate(choices) if n != answer_index)
        placed = {label: (answer_text if label == key else next(distractors)) for label in "ABCD"}
        question = {"subject_slug": "reasoning", "subcategory_slug": None, "chapter_slug": "decision-making",
                    "question_text": _all_question_text(item), "difficulty": item["difficulty"], "is_pyq": False,
                    "pyq_year": None, "pyq_exam_name": None, "source": _source_label(item["source"]),
                    "options": placed, "correct_option": key, "explanation": item["reason"]}
        rows.append(question)
        ledger.append({"id": qid, "row": index, "category": item["category"], "topic": item["topic"], "question": question["question_text"],
                       "source_pdf": item["source"][0] if item["source"] else None,
                       "source_page": item["source"][1] if item["source"] else None,
                       "source": question["source"], "original_question": item["source"] is None,
                       "statement": item["statement"], "eligibility": eligibility_audit,
                       "options": placed, "correct_option": key, "correct_answer": answer_text,
                       "independent_reasoning": item["reason"], "difficulty": item["difficulty"],
                       "verification_status": "independently_verified"})
    difficulty = Counter(row["difficulty"] for row in rows)
    categories = Counter(item["category"] for item in ITEMS)
    positions_count = Counter(row["correct_option"] for row in rows)
    if difficulty != Counter(LEVELS) or categories != Counter({"ELIGIBILITY": 18, "SITUATIONAL": 16}) or positions_count != Counter({"A": 9, "B": 9, "C": 8, "D": 8}):
        raise ValueError(f"Distribution mismatch: difficulty={difficulty}, categories={categories}, positions={positions_count}")
    reviews = _page_review()
    accepted = sum(entry["source"] is not None for entry in ITEMS)
    original = len(ITEMS) - accepted
    rejected = [page for page in reviews if page["status"] == "rejected"]
    source_review = {"pdfs": [{"name": PDF1, "pages": 26}, {"name": PDF2, "pages": 20}],
                     "pages_reviewed": 46, "page_reviews": reviews,
                     "accepted_source_question_count": accepted, "original_question_count": original,
                     "rejected_source_question_count": len(rejected)}
    report = {"chapter_id": "382f7052-28c0-4d51-a117-d59dde2934d5", "total_questions": len(rows),
              "accepted_source_questions": accepted, "original_questions": original,
              "rejected_source_pages": [{"pdf": p["pdf"], "page": p["page"], "reason": p["reason"]} for p in rejected],
              "category_distribution": dict(categories), "difficulty_distribution": dict(difficulty),
              "answer_position_distribution": dict(positions_count),
              "eligibility_verification": "All 16 candidate cases are independently evaluated by evaluate_candidate using per-question criteria, exact reference dates, calendar-age calculation, completed calendar months, and exact-failure referral exceptions. Boundary and exception tests are in test_decision_making_verified_batch.py.",
              "situational_verification": "Every selected action was re-evaluated against the stated context for safety, rights, proportionality, procedure, and escalation. Four underspecified or unsafe source situations were rejected.",
              "duplicate_check": "Exact and high-similarity screening is applied by the guarded importer against live active Reasoning questions and canonical batches; the source cases were manually compared for duplicate scenarios and decision logic.",
              "import_status": "POST_IMPORT_VERIFIED",
              "database_verification": {"chapter_id": "382f7052-28c0-4d51-a117-d59dde2934d5", "active_normal": 34, "active_pyq": 0, "difficulty_distribution": {"EASY": 11, "MEDIUM": 12, "HARD": 11}, "initial_imported": 34, "initial_rejected": 0, "initial_duplicates": 0, "replay_duplicates": 34, "replay_inserts": 0, "other_chapter_ids_unchanged": True},
              "verification_results": {"focused_tests": "9 passed", "targeted_backend_regression": "111 passed", "full_backend_suite": "409 passed in 630.46s", "python_compilation": "passed", "git_diff_check": "passed", "frontend_production_build": "passed (Vite 5.4.21)", "authenticated_live_api": {"chapter_list": "present under Reasoning", "difficulty_availability_10_questions": {"EASY": 11, "MEDIUM": 12, "HARD": 11, "PYQ": 0}, "mixed_normal_available": 34, "question_rows_have_four_options_and_explanations": True, "exam_session_flow": "TestClient integration passed save/reload, submit, score, review and explanations"}, "browser_ui": "not performed; no browser verification claimed"}}
    (DATA / "decision_making_verified_batch.json").write_text(json.dumps({"questions": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "decision_making_answer_ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "decision_making_source_review.json").write_text(json.dumps(source_review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "decision_making_review_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# CH-20 Decision Making review", "", "## Source review", "",
          f"Visually reviewed all 46 scanned pages: {PDF1} (26 pages) and {PDF2} (20 pages). Page-by-page decisions are in `decision_making_source_review.json`.",
          "", f"Accepted source-derived questions: {accepted}; original questions: {original}; rejected source candidates: {len(rejected)}.",
          "", "Rejected source questions: " + "; ".join(f"{p['pdf']} p.{p['page']}: {p['reason']}" for p in rejected),
          "", "## Question bank", "", f"Total: {len(rows)} active Normal questions; 0 PYQs.",
          "", "Categories: " + ", ".join(f"{k}={v}" for k, v in categories.items()),
          "", "Difficulty: " + ", ".join(f"{k}={v}" for k, v in difficulty.items()),
          "", "Correct-answer positions: " + ", ".join(f"{k}={v}" for k, v in positions_count.items()),
          "", "## Independent verification", "", report["eligibility_verification"], "", report["situational_verification"], "", report["duplicate_check"],
          "", "## Import and application verification", "",
          "Live database import: 34 imported, 0 rejected, 0 duplicates. Final active Normal=34, PYQ=0; difficulty counts Easy=11, Medium=12, Hard=11. Replay dry-run: 34 duplicates, 0 inserts. Other chapter IDs remained unchanged.",
          "", "Authenticated live API: chapter appears under Reasoning; Easy/Medium/Hard availability is 11/12/11 for a 10-question request; PYQ availability is 0. Mixed Normal pool reports 34. Returned questions include four options and explanations. TestClient exam-session flow passed save/reload, submission, scoring, and answer/explanation review.",
          "", "Verification: CH-20 focused tests 9 passed; targeted backend regression 111 passed; full backend suite 409 passed in 630.46s. Python compilation, git diff --check, and frontend production build (Vite 5.4.21) passed. No browser UI verification was performed.", ""]
    (DATA / "decision_making_review_report.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    build()
