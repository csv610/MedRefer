import pytest
from unittest.mock import Mock, patch
from medrefer import MedReferral


SPECIALIST_CASES = [
    ("Allergist", "persistent sneezing, itchy eyes, and rash when exposed to pollen"),
    ("Anesthesiologist", "need anesthesia management for hip replacement surgery"),
    ("Cardiologist", "chest pain, shortness of breath, and irregular heartbeat"),
    ("Cardiothoracic Surgeon", "need open heart surgery to repair a damaged heart valve"),
    ("Colorectal Surgeon", "rectal bleeding and persistent constipation requiring surgery"),
    ("Child and Adolescent Psychiatrist", "my 12-year-old has severe anxiety and behavioral issues"),
    ("Dermatologist", "severe acne, eczema, and skin growths that need evaluation"),
    ("Endocrinologist", "diabetes, thyroid problems, and hormonal imbalances"),
    ("Forensic Psychiatrist", "need psychiatric evaluation for legal proceedings"),
    ("Gastroenterologist", "chronic diarrhea, abdominal pain, and acid reflux"),
    ("General Surgeon", "need emergency appendix removal surgery"),
    ("Geriatrician", "my 82-year-old mother needs comprehensive healthcare management"),
    ("Geriatric Psychiatrist", "my 75-year-old father has dementia and severe depression"),
    ("Gynecologist", "irregular periods, pelvic pain, and need cervical screening"),
    ("Hematologist", "anemia, easy bruising, and bleeding disorders"),
    ("Infectious Disease Specialist", "recurrent infections, fever, and suspect tuberculosis"),
    ("Internal Medicine Doctor (Internist)", "need comprehensive care for multiple chronic conditions"),
    ("Immunologist", "recurrent infections and suspect immune system deficiency"),
    ("Maternal-Fetal Medicine Specialist", "pregnant with complications and need high-risk care"),
    ("Nephrologist", "chronic kidney disease, high blood pressure, and protein in urine"),
    ("Neurologist", "migraines, seizures, and numbness in my limbs"),
    ("Neurosurgeon", "brain tumor requiring surgical intervention"),
    ("Neonatologist", "newborn has breathing problems and needs intensive care"),
    ("Nuclear Medicine Specialist", "need nuclear medicine imaging for thyroid assessment"),
    ("Obstetrician", "pregnant and need prenatal care and delivery planning"),
    ("Occupational Medicine Specialist", "work-related injury and need occupational health evaluation"),
    ("Oncologist", "diagnosed with cancer and need treatment planning"),
    ("Orthopedic Surgeon", "torn ACL and need knee surgery"),
    ("Ophthalmologist", "blurry vision, eye pain, and suspect glaucoma"),
    ("Otolaryngologist (ENT Specialist)", "chronic sinusitis, hearing loss, and throat problems"),
    ("Pediatrician", "my 5-year-old has recurring ear infections and developmental concerns"),
    ("Pathologist", "need pathology analysis of my biopsy samples"),
    ("Pulmonologist", "asthma, shortness of breath, and chronic cough"),
    ("Pediatric Surgeon", "my child needs surgical correction of a birth defect"),
    ("Plastic Surgeon", "burn scars and want reconstructive surgery"),
    ("Physical Medicine & Rehabilitation (PM&R) Specialist", "spinal cord injury and need rehabilitation therapy"),
    ("Pain Management Specialist", "chronic pain from fibromyalgia that doesn't respond"),
    ("Psychiatrist", "severe depression, anxiety, and need psychiatric medication"),
    ("Rheumatologist", "rheumatoid arthritis, joint pain, and swelling"),
    ("Radiologist", "need imaging interpretation for CT and MRI scans"),
    ("Sports Medicine Doctor", "sports-related injury to my shoulder"),
    ("Sleep Medicine Specialist", "severe sleep apnea and insomnia"),
    ("Trauma Surgeon", "multiple injuries from a motor vehicle accident"),
    ("Transplant Surgeon", "end-stage kidney disease and need a kidney transplant"),
    ("Urologist", "urinary incontinence, prostate problems, and erectile dysfunction"),
]


class TestAllSpecialists:
    @pytest.mark.parametrize("specialist, question", SPECIALIST_CASES)
    @patch("litellm.completion")
    def test_recommends_specialist(self, mock_completion, specialist, question):
        mock_completion.return_value = _mock_response(f"Specialists: {specialist}")
        result = MedReferral().get_specialist_recommendation(question)
        assert specialist in result


def _mock_response(content: str):
    mr = Mock()
    mr.choices = [Mock()]
    mr.choices[0].message.content = content
    return mr
