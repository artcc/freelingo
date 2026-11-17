"""Curated speaking situations; public clients localize the stable IDs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Situation:
    id: str
    category: str
    title: str
    scenario: str
    role: str
    objective: str


SITUATIONS = (
    Situation(
        "medical_appointment",
        "daily_life",
        "Booking a medical appointment",
        "The learner calls a medical practice to arrange a routine appointment.",
        "A receptionist asking the reason for the appointment and offering available times.",
        "Briefly explain the reason, clarify availability and confirm the appointment details.",
    ),
    Situation(
        "neighbour_problem",
        "daily_life",
        "A problem with a neighbour",
        "The learner speaks to a neighbour about repeated evening noise.",
        "A neighbour willing to listen but with their own routine.",
        "Explain the problem politely, hear the other perspective and agree on a compromise.",
    ),
    Situation(
        "flat_viewing",
        "daily_life",
        "Viewing a flat",
        "The learner visits a flat they might rent.",
        "An estate agent showing the flat and answering practical questions.",
        "Ask about the flat, clarify rent and conditions, and express a decision or next step.",
    ),
    Situation(
        "school_meeting",
        "daily_life",
        "A school meeting",
        "The learner attends a meeting about a child's experience at school.",
        "A teacher discussing classroom progress and a small practical concern.",
        "Ask about progress, explain a concern and agree on helpful follow-up.",
    ),
    Situation(
        "household_repair",
        "daily_life",
        "Arranging a household repair",
        "The learner arranges help for a broken household appliance.",
        "A repair professional asking what happened and when a visit is possible.",
        "Describe the fault, clarify timing and cost, and agree on an appointment.",
    ),
    Situation(
        "change_reservation",
        "travel",
        "Changing a reservation",
        "The learner needs to change the date of a travel reservation.",
        "A reservations agent checking alternatives and conditions.",
        "Explain the change, compare an alternative and confirm the new arrangement.",
    ),
    Situation(
        "hotel_problem",
        "travel",
        "A problem at the hotel",
        "The learner reports a problem with their hotel room.",
        "A receptionist offering a realistic remedy.",
        "Describe the issue, ask for a solution and confirm an acceptable arrangement.",
    ),
    Situation(
        "ask_directions",
        "travel",
        "Asking for directions",
        "The learner needs to find a destination in an unfamiliar town.",
        "A local person giving directions with simple landmarks.",
        "Ask for directions, clarify a confusing step and confirm the route.",
    ),
    Situation(
        "missed_connection",
        "travel",
        "A missed connection",
        "A delay has caused the learner to miss a connecting train or flight.",
        "A transport agent helping find the next available connection.",
        "Explain the delay, ask about alternatives and confirm the next journey.",
    ),
    Situation(
        "lost_luggage",
        "travel",
        "Lost luggage",
        "The learner's suitcase has not arrived at the destination.",
        "A baggage-desk agent collecting the description and delivery arrangements.",
        "Describe the luggage, explain the journey and agree how to receive an update.",
    ),
    Situation(
        "return_purchase",
        "shopping_services",
        "Returning a purchase",
        "The learner returns an item that is faulty or unsuitable.",
        "A shop assistant checking the issue and offering return options.",
        "Explain the reason, clarify the policy and agree on a refund or exchange.",
    ),
    Situation(
        "restaurant_order",
        "shopping_services",
        "Ordering at a restaurant",
        "The learner orders a meal and has a dietary preference.",
        "A server explaining a few menu options and checking the order.",
        "Choose a meal, clarify an ingredient or preference and confirm the order.",
    ),
    Situation(
        "phone_contract",
        "shopping_services",
        "Choosing a phone contract",
        "The learner compares mobile-phone plans.",
        "A shop adviser explaining two realistic plans and their conditions.",
        "Describe usage needs, clarify price and commitment, and choose or decline an offer.",
    ),
    Situation(
        "bank_appointment",
        "shopping_services",
        "An appointment at the bank",
        "The learner asks about opening a basic bank account using fictional details.",
        "A bank employee explaining account features without requesting real sensitive details.",
        "Explain the need, ask about fees and required documents, and agree on a next step.",
    ),
    Situation(
        "delivery_problem",
        "shopping_services",
        "A delivery problem",
        "The learner contacts customer service about a missing or damaged delivery.",
        "A customer-service representative checking the issue.",
        "Describe the order problem, request a remedy and confirm what will happen next.",
    ),
    Situation(
        "meet_someone",
        "social",
        "Meeting someone new",
        "The learner meets someone at a small social gathering.",
        "Another guest with a few ordinary interests to share.",
        "Introduce yourself, find a shared interest and bring the exchange to a natural pause.",
    ),
    Situation(
        "make_plans",
        "social",
        "Making plans",
        "The learner and a friend arrange something to do together.",
        "A friend with a preference and a scheduling constraint.",
        "Suggest an activity, negotiate availability and confirm a time and place.",
    ),
    Situation(
        "decline_invitation",
        "social",
        "Declining an invitation",
        "The learner cannot accept a friend's invitation.",
        "A friend inviting the learner to an event.",
        "Decline politely, explain as much as you wish and optionally suggest an alternative.",
    ),
    Situation(
        "resolve_misunderstanding",
        "social",
        "Resolving a misunderstanding",
        "A friend has misunderstood a message about shared plans.",
        "A friend who has a different interpretation and is open to clarification.",
        "Explain the intended meaning, acknowledge the misunderstanding and agree what to do.",
    ),
    Situation(
        "host_visitors",
        "social",
        "Hosting visitors",
        "The learner welcomes visitors and helps them settle in.",
        "A visiting friend asking about arrangements and local activities.",
        "Welcome the visitor, explain practical arrangements and agree on a simple plan.",
    ),
    Situation(
        "introduce_yourself",
        "work",
        "Introducing yourself at work",
        "The learner meets a colleague on their first day.",
        "A welcoming colleague explaining their own role.",
        "Introduce your role, ask about the team and establish a useful first connection.",
    ),
    Situation(
        "explain_task",
        "work",
        "Explaining a task",
        "The learner explains an ordinary work task to a colleague.",
        "A colleague who needs to understand the task and its main steps.",
        "Explain the purpose and steps, clarify a detail and check shared understanding.",
    ),
    Situation(
        "clarify_instructions",
        "work",
        "Clarifying instructions",
        "The learner receives work instructions with one ambiguous detail.",
        "A manager assigning a realistic task and clarifying it when asked.",
        "Identify the ambiguity, ask a focused question and confirm the expected result.",
    ),
    Situation(
        "negotiate_deadline",
        "work",
        "Negotiating a deadline",
        "The learner needs more time for a task while the project manager needs a timely result.",
        "A project manager discussing priorities and possible adjustments.",
        "Explain the constraint, propose a realistic alternative and agree on a deadline.",
    ),
    Situation(
        "share_proposal",
        "work",
        "Sharing a proposal",
        "The learner suggests a small improvement to a team routine.",
        "A colleague interested in the proposal but with one practical concern.",
        "Present the idea and benefit, respond to the concern and agree on a next step.",
    ),
)

SITUATIONS_BY_ID = {situation.id: situation for situation in SITUATIONS}
SITUATION_CONTEXT_PREFIX = "<situation>\n"
