"""
Comprehensive test coverage for all 42 medical specialists.
Each specialist has a test case with a relevant medical question that should trigger its recommendation.
"""

import pytest
from unittest.mock import Mock, patch
from medrefer import MedReferral


class TestAllSpecialists:
    """Test cases for all 42 medical specialists."""

    @patch('litellm.completion')
    def test_allergist(self, mock_completion):
        """Test recommendation for Allergist - allergies and hypersensitivity."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Allergist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have persistent sneezing, itchy eyes, and rash when exposed to pollen"
        )
        assert "Allergist" in result

    @patch('litellm.completion')
    def test_anesthesiologist(self, mock_completion):
        """Test recommendation for Anesthesiologist - surgical anesthesia management."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Anesthesiologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I need anesthesia management for my upcoming hip replacement surgery"
        )
        assert "Anesthesiologist" in result

    @patch('litellm.completion')
    def test_cardiologist(self, mock_completion):
        """Test recommendation for Cardiologist - heart and cardiovascular diseases."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Cardiologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have chest pain, shortness of breath, and irregular heartbeat"
        )
        assert "Cardiologist" in result

    @patch('litellm.completion')
    def test_cardiothoracic_surgeon(self, mock_completion):
        """Test recommendation for Cardiothoracic Surgeon - heart and chest surgery."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Cardiothoracic Surgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I need open heart surgery to repair a damaged heart valve"
        )
        assert "Cardiothoracic Surgeon" in result

    @patch('litellm.completion')
    def test_colorectal_surgeon(self, mock_completion):
        """Test recommendation for Colorectal Surgeon - colon and rectum surgery."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Colorectal Surgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have rectal bleeding and persistent constipation requiring surgical evaluation"
        )
        assert "Colorectal Surgeon" in result

    @patch('litellm.completion')
    def test_child_and_adolescent_psychiatrist(self, mock_completion):
        """Test recommendation for Child and Adolescent Psychiatrist."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Child and Adolescent Psychiatrist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "My 12-year-old daughter has severe anxiety and behavioral issues affecting school"
        )
        assert "Child and Adolescent Psychiatrist" in result

    @patch('litellm.completion')
    def test_dermatologist(self, mock_completion):
        """Test recommendation for Dermatologist - skin conditions."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Dermatologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have severe acne, eczema, and skin growths that need evaluation"
        )
        assert "Dermatologist" in result

    @patch('litellm.completion')
    def test_endocrinologist(self, mock_completion):
        """Test recommendation for Endocrinologist - hormones and metabolism."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Endocrinologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have diabetes, thyroid problems, and hormonal imbalances"
        )
        assert "Endocrinologist" in result

    @patch('litellm.completion')
    def test_forensic_psychiatrist(self, mock_completion):
        """Test recommendation for Forensic Psychiatrist - psychiatric evaluation for legal cases."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Forensic Psychiatrist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I need psychiatric evaluation for legal proceedings"
        )
        assert "Forensic Psychiatrist" in result

    @patch('litellm.completion')
    def test_gastroenterologist(self, mock_completion):
        """Test recommendation for Gastroenterologist - digestive system."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Gastroenterologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have chronic diarrhea, abdominal pain, and acid reflux"
        )
        assert "Gastroenterologist" in result

    @patch('litellm.completion')
    def test_general_surgeon(self, mock_completion):
        """Test recommendation for General Surgeon - general surgical procedures."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: General Surgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I need emergency appendix removal surgery"
        )
        assert "General Surgeon" in result

    @patch('litellm.completion')
    def test_geriatrician(self, mock_completion):
        """Test recommendation for Geriatrician - elderly patient care."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Geriatrician"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "My 82-year-old mother needs comprehensive healthcare management for multiple chronic conditions"
        )
        assert "Geriatrician" in result

    @patch('litellm.completion')
    def test_geriatric_psychiatrist(self, mock_completion):
        """Test recommendation for Geriatric Psychiatrist - elderly mental health."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Geriatric Psychiatrist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "My 75-year-old father has dementia and severe depression"
        )
        assert "Geriatric Psychiatrist" in result

    @patch('litellm.completion')
    def test_gynecologist(self, mock_completion):
        """Test recommendation for Gynecologist - women's reproductive health."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Gynecologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have irregular periods, pelvic pain, and need cervical screening"
        )
        assert "Gynecologist" in result

    @patch('litellm.completion')
    def test_hematologist(self, mock_completion):
        """Test recommendation for Hematologist - blood disorders."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Hematologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have anemia, easy bruising, and bleeding disorders"
        )
        assert "Hematologist" in result

    @patch('litellm.completion')
    def test_infectious_disease_specialist(self, mock_completion):
        """Test recommendation for Infectious Disease Specialist."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Infectious Disease Specialist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have recurrent infections, fever, and suspect tuberculosis"
        )
        assert "Infectious Disease Specialist" in result

    @patch('litellm.completion')
    def test_internal_medicine_doctor(self, mock_completion):
        """Test recommendation for Internal Medicine Doctor (Internist)."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Internal Medicine Doctor (Internist)"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I need comprehensive care for multiple chronic conditions"
        )
        assert "Internal Medicine Doctor (Internist)" in result

    @patch('litellm.completion')
    def test_immunologist(self, mock_completion):
        """Test recommendation for Immunologist - immune system disorders."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Immunologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have recurrent infections and suspect immune system deficiency"
        )
        assert "Immunologist" in result

    @patch('litellm.completion')
    def test_maternal_fetal_medicine_specialist(self, mock_completion):
        """Test recommendation for Maternal-Fetal Medicine Specialist."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Maternal-Fetal Medicine Specialist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I am pregnant with complications and need high-risk pregnancy care"
        )
        assert "Maternal-Fetal Medicine Specialist" in result

    @patch('litellm.completion')
    def test_nephrologist(self, mock_completion):
        """Test recommendation for Nephrologist - kidney disease."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Nephrologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have chronic kidney disease, high blood pressure, and protein in urine"
        )
        assert "Nephrologist" in result

    @patch('litellm.completion')
    def test_neurologist(self, mock_completion):
        """Test recommendation for Neurologist - nervous system diseases."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Neurologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have migraines, seizures, and numbness in my limbs"
        )
        assert "Neurologist" in result

    @patch('litellm.completion')
    def test_neurosurgeon(self, mock_completion):
        """Test recommendation for Neurosurgeon - brain and spine surgery."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Neurosurgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have a brain tumor requiring surgical intervention"
        )
        assert "Neurosurgeon" in result

    @patch('litellm.completion')
    def test_neonatologist(self, mock_completion):
        """Test recommendation for Neonatologist - newborn care."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Neonatologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "My newborn has breathing problems and needs intensive care"
        )
        assert "Neonatologist" in result

    @patch('litellm.completion')
    def test_nuclear_medicine_specialist(self, mock_completion):
        """Test recommendation for Nuclear Medicine Specialist."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Nuclear Medicine Specialist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I need nuclear medicine imaging for thyroid and cardiac assessment"
        )
        assert "Nuclear Medicine Specialist" in result

    @patch('litellm.completion')
    def test_obstetrician(self, mock_completion):
        """Test recommendation for Obstetrician - pregnancy and delivery."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Obstetrician"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I am pregnant and need prenatal care and delivery planning"
        )
        assert "Obstetrician" in result

    @patch('litellm.completion')
    def test_occupational_medicine_specialist(self, mock_completion):
        """Test recommendation for Occupational Medicine Specialist."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Occupational Medicine Specialist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have work-related injury and need occupational health evaluation"
        )
        assert "Occupational Medicine Specialist" in result

    @patch('litellm.completion')
    def test_oncologist(self, mock_completion):
        """Test recommendation for Oncologist - cancer treatment."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Oncologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have been diagnosed with cancer and need treatment planning"
        )
        assert "Oncologist" in result

    @patch('litellm.completion')
    def test_orthopedic_surgeon(self, mock_completion):
        """Test recommendation for Orthopedic Surgeon - bone and joint surgery."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Orthopedic Surgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have a torn ACL and need knee surgery"
        )
        assert "Orthopedic Surgeon" in result

    @patch('litellm.completion')
    def test_ophthalmologist(self, mock_completion):
        """Test recommendation for Ophthalmologist - eye diseases."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Ophthalmologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have blurry vision, eye pain, and suspect glaucoma"
        )
        assert "Ophthalmologist" in result

    @patch('litellm.completion')
    def test_otolaryngologist(self, mock_completion):
        """Test recommendation for Otolaryngologist (ENT Specialist)."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Otolaryngologist (ENT Specialist)"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have chronic sinusitis, hearing loss, and throat problems"
        )
        assert "Otolaryngologist (ENT Specialist)" in result

    @patch('litellm.completion')
    def test_pediatrician(self, mock_completion):
        """Test recommendation for Pediatrician - child health care."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Pediatrician"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "My 5-year-old has recurring ear infections and developmental concerns"
        )
        assert "Pediatrician" in result

    @patch('litellm.completion')
    def test_pathologist(self, mock_completion):
        """Test recommendation for Pathologist - tissue and disease analysis."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Pathologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I need pathology analysis of my biopsy samples"
        )
        assert "Pathologist" in result

    @patch('litellm.completion')
    def test_pulmonologist(self, mock_completion):
        """Test recommendation for Pulmonologist - lung and respiratory diseases."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Pulmonologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have asthma, shortness of breath, and chronic cough"
        )
        assert "Pulmonologist" in result

    @patch('litellm.completion')
    def test_pediatric_surgeon(self, mock_completion):
        """Test recommendation for Pediatric Surgeon - child surgery."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Pediatric Surgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "My child needs surgical correction of a birth defect"
        )
        assert "Pediatric Surgeon" in result

    @patch('litellm.completion')
    def test_plastic_surgeon(self, mock_completion):
        """Test recommendation for Plastic Surgeon - reconstructive and cosmetic surgery."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Plastic Surgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have burn scars and want reconstructive surgery"
        )
        assert "Plastic Surgeon" in result

    @patch('litellm.completion')
    def test_physical_medicine_rehabilitation_specialist(self, mock_completion):
        """Test recommendation for Physical Medicine & Rehabilitation (PM&R) Specialist."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Physical Medicine & Rehabilitation (PM&R) Specialist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have spinal cord injury and need rehabilitation therapy"
        )
        assert "Physical Medicine & Rehabilitation (PM&R) Specialist" in result

    @patch('litellm.completion')
    def test_pain_management_specialist(self, mock_completion):
        """Test recommendation for Pain Management Specialist."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Pain Management Specialist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have chronic pain from fibromyalgia that doesn't respond to medications"
        )
        assert "Pain Management Specialist" in result

    @patch('litellm.completion')
    def test_psychiatrist(self, mock_completion):
        """Test recommendation for Psychiatrist - mental health."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Psychiatrist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have severe depression, anxiety, and need psychiatric medication"
        )
        assert "Psychiatrist" in result

    @patch('litellm.completion')
    def test_rheumatologist(self, mock_completion):
        """Test recommendation for Rheumatologist - arthritis and autoimmune diseases."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Rheumatologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have rheumatoid arthritis, joint pain, and swelling"
        )
        assert "Rheumatologist" in result

    @patch('litellm.completion')
    def test_radiologist(self, mock_completion):
        """Test recommendation for Radiologist - medical imaging."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Radiologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I need imaging interpretation for my CT and MRI scans"
        )
        assert "Radiologist" in result

    @patch('litellm.completion')
    def test_sports_medicine_doctor(self, mock_completion):
        """Test recommendation for Sports Medicine Doctor."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Sports Medicine Doctor"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have a sports-related injury to my shoulder"
        )
        assert "Sports Medicine Doctor" in result

    @patch('litellm.completion')
    def test_sleep_medicine_specialist(self, mock_completion):
        """Test recommendation for Sleep Medicine Specialist."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Sleep Medicine Specialist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have severe sleep apnea and insomnia"
        )
        assert "Sleep Medicine Specialist" in result

    @patch('litellm.completion')
    def test_trauma_surgeon(self, mock_completion):
        """Test recommendation for Trauma Surgeon - acute traumatic injuries."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Trauma Surgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have multiple injuries from a motor vehicle accident"
        )
        assert "Trauma Surgeon" in result

    @patch('litellm.completion')
    def test_transplant_surgeon(self, mock_completion):
        """Test recommendation for Transplant Surgeon - organ transplantation."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Transplant Surgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have end-stage kidney disease and need a kidney transplant"
        )
        assert "Transplant Surgeon" in result

    @patch('litellm.completion')
    def test_urologist(self, mock_completion):
        """Test recommendation for Urologist - urinary and reproductive system."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Urologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation(
            "I have urinary incontinence, prostate problems, and erectile dysfunction"
        )
        assert "Urologist" in result
