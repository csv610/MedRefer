import litellm
import os
import re
import logging

logger = logging.getLogger(__name__)


_EMERGENCY_KEYWORDS = [
    "crushing chest pain", "heart attack", "stroke", "massive bleeding",
    "unconscious", "not breathing", "severe allergic reaction", "anaphylaxis",
    "severe burn", "gunshot", "stab wound", "severe head injury",
    "suicidal", "overdose", "poisoning", "drowning",
    "major trauma", "car accident", "spinal injury",
    "cannot breathe", "choking", "severe chest pain",
]


_MAX_INPUT_LENGTH = 2000


class MedReferral:
    """
    A class for determining the appropriate medical specialists based on a
    given question using LLMs via LiteLLM.
    """

    medical_specialists = frozenset([
        "Allergist",
        "Anesthesiologist",
        "Cardiologist",
        "Cardiothoracic Surgeon",
        "Colorectal Surgeon",
        "Child and Adolescent Psychiatrist",
        "Dermatologist",
        "Endocrinologist",
        "Forensic Psychiatrist",
        "Gastroenterologist",
        "General Surgeon",
        "Geriatrician",
        "Geriatric Psychiatrist",
        "Gynecologist",
        "Hematologist",
        "Infectious Disease Specialist",
        "Internal Medicine Doctor (Internist)",
        "Immunologist",
        "Maternal-Fetal Medicine Specialist",
        "Nephrologist",
        "Neurologist",
        "Neurosurgeon",
        "Neonatologist",
        "Nuclear Medicine Specialist",
        "Obstetrician",
        "Occupational Medicine Specialist",
        "Oncologist",
        "Orthopedic Surgeon",
        "Ophthalmologist",
        "Otolaryngologist (ENT Specialist)",
        "Pediatrician",
        "Pathologist",
        "Pulmonologist",
        "Pediatric Surgeon",
        "Plastic Surgeon",
        "Physical Medicine & Rehabilitation (PM&R) Specialist",
        "Pain Management Specialist",
        "Psychiatrist",
        "Rheumatologist",
        "Radiologist",
        "Sports Medicine Doctor",
        "Sleep Medicine Specialist",
        "Trauma Surgeon",
        "Transplant Surgeon",
        "Urologist",
    ])

    _specialist_lookup = {s.lower(): s for s in medical_specialists}

    def __init__(self, model=None):
        self.model = model or os.getenv("MEDREFER_MODEL", "ollama/gemma4")
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            litellm.api_key = api_key

    def _contains_emergency_keywords(self, question):
        question_lower = question.lower()
        for keyword in _EMERGENCY_KEYWORDS:
            if keyword in question_lower:
                return True
        return False

    def _validate_input(self, question):
        if not isinstance(question, str):
            raise ValueError("Question must be a string.")
        if not question.strip():
            raise ValueError("Question cannot be empty.")
        if len(question) > _MAX_INPUT_LENGTH:
            raise ValueError(f"Question exceeds maximum length of {_MAX_INPUT_LENGTH} characters.")

    def _match_specialist(self, name):
        return self._specialist_lookup.get(name.strip().lower())

    def get_specialist_recommendation(self, question):
        self._validate_input(question)

        if self._contains_emergency_keywords(question):
            logger.warning("Emergency keywords detected in question: %s", question[:120])
            return ("EMERGENCY: Please call emergency services (911) immediately. "
                    "Do not wait for a specialist appointment.")

        prompt = f"""You are a medical assistant. Based on the given medical question, recommend the most suitable specialist doctors.
Some symptoms may require consultation with multiple specialists.

Example format:
- Question: "I have chest pain and shortness of breath."
  Specialists: Cardiologist, Pulmonologist

- Question: "I have severe joint pain and swelling."
  Specialists: Rheumatologist, Orthopedic Surgeon

- Question: "I have blurry vision and headaches."
  Specialists: Ophthalmologist, Neurologist

Now, analyze the following question and recommend the best specialists:

Question: "{question}"
Specialists:"""

        try:
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful medical assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=100
            )

            full_response = response.choices[0].message.content.strip()
            match = re.search(r"Specialists?:\s*(.*)", full_response)
            if match:
                raw_specialists = match.group(1)
            else:
                raw_specialists = ""

            recommended = [s.strip() for s in raw_specialists.split(",")]
            valid = []
            for s in recommended:
                matched = self._match_specialist(s)
                if matched:
                    valid.append(matched)

            if valid:
                result = ", ".join(valid)
                logger.info("Question: %s -> Specialists: %s", question[:120], result)
                return f"{result} (Please verify with a healthcare professional.)"
            elif raw_specialists:
                logger.warning("No valid specialists found in response: %s", raw_specialists)
                return f"{raw_specialists} (Note: Could not verify these specialists. Please consult a healthcare professional.)"
            else:
                logger.warning("No specialist line found in LLM response: %s", full_response[:200])
                return ("Unable to determine specialists. "
                        "Please verify with a healthcare professional.")

        except Exception as e:
            logger.error("API error: %s", str(e))
            return f"Error: {str(e)}"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    med_referral = MedReferral()
    print("Enter your medical question (or type 'exit' / 'quit' to quit):")
    while True:
        try:
            medical_question = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if medical_question.lower() in ("exit", "quit"):
            break
        if not medical_question.strip():
            continue
        specialists = med_referral.get_specialist_recommendation(medical_question)
        print(f"Recommended Specialists: {specialists}")
