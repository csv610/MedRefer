import litellm
import pytest
from unittest.mock import Mock, patch
from medrefer import MedReferral


class TestMedReferralInit:
    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    def test_init_sets_litellm_api_key(self):
        with patch("litellm.api_key", ""):
            MedReferral()
            assert litellm.api_key == "test-key-123"

    def test_medical_specialists_contains_expected(self):
        expected = {
            "Cardiologist", "Neurologist", "Dermatologist",
            "Psychiatrist", "Oncologist", "Ophthalmologist",
            "Urologist", "Endocrinologist", "Gastroenterologist",
        }
        assert expected.issubset(MedReferral.medical_specialists)

    def test_medical_specialists_is_frozenset(self):
        assert isinstance(MedReferral.medical_specialists, frozenset)

    def test_medical_specialists_count(self):
        assert len(MedReferral.medical_specialists) == 45


class TestGetSpecialistRecommendation:
    @patch("litellm.completion")
    def test_returns_valid_specialists(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Cardiologist, Pulmonologist")
        result = MedReferral().get_specialist_recommendation("chest pain")
        assert result == "Cardiologist, Pulmonologist"

    @patch("litellm.completion")
    def test_filters_invalid_specialists(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Cardiologist, Quack, Neurologist")
        result = MedReferral().get_specialist_recommendation("headache")
        assert result == "Cardiologist, Neurologist"

    @patch("litellm.completion")
    def test_no_valid_specialists_returns_disclaimer(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Quack, Witch Doctor")
        result = MedReferral().get_specialist_recommendation("weird symptoms")
        assert "Please verify with a healthcare professional." in result

    @patch("litellm.completion")
    def test_missing_specialists_line(self, mock_completion):
        mock_completion.return_value = _mock_response("Go see a doctor.")
        result = MedReferral().get_specialist_recommendation("sick")
        assert "Unknown Specialists" in result

    @patch("litellm.completion")
    def test_api_error(self, mock_completion):
        mock_completion.side_effect = Exception("API Connection Error")
        result = MedReferral().get_specialist_recommendation("headache")
        assert result == "Error: API Connection Error"

    @patch("litellm.completion")
    def test_strips_whitespace(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists:  Cardiologist  ,  Neurologist  ")
        result = MedReferral().get_specialist_recommendation("symptoms")
        assert result == "Cardiologist, Neurologist"

    @patch("litellm.completion")
    def test_single_specialist(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Dermatologist")
        result = MedReferral().get_specialist_recommendation("skin rash")
        assert result == "Dermatologist"

    @patch("litellm.completion")
    def test_multiple_specialists(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Rheumatologist, Orthopedic Surgeon, Internal Medicine Doctor (Internist)")
        result = MedReferral().get_specialist_recommendation("joint pain")
        assert result == "Rheumatologist, Orthopedic Surgeon, Internal Medicine Doctor (Internist)"

    @patch("litellm.completion")
    def test_case_sensitivity(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: cardiologist, NEUROLOGIST, Dermatologist")
        result = MedReferral().get_specialist_recommendation("symptoms")
        assert result == "Dermatologist"

    @patch("litellm.completion")
    def test_specialist_with_parentheses(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Otolaryngologist (ENT Specialist), Physical Medicine & Rehabilitation (PM&R) Specialist")
        result = MedReferral().get_specialist_recommendation("ear and throat issues")
        assert "Otolaryngologist (ENT Specialist)" in result
        assert "Physical Medicine & Rehabilitation (PM&R) Specialist" in result

    @patch("litellm.completion")
    def test_calls_litellm_with_correct_params(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Cardiologist")
        question = "I have chest pain"
        MedReferral().get_specialist_recommendation(question)

        mock_completion.assert_called_once()
        kwargs = mock_completion.call_args.kwargs
        assert kwargs["model"] == "ollama/gemma4"
        assert kwargs["max_tokens"] == 100
        assert len(kwargs["messages"]) == 2
        assert kwargs["messages"][0]["role"] == "system"
        assert kwargs["messages"][1]["role"] == "user"
        assert question in kwargs["messages"][1]["content"]

    @patch("litellm.completion")
    def test_empty_question(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: General Surgeon")
        result = MedReferral().get_specialist_recommendation("")
        assert result == "General Surgeon"

    @patch("litellm.completion")
    def test_very_long_question(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Neurologist")
        result = MedReferral().get_specialist_recommendation("I have " + "symptoms " * 100)
        assert result == "Neurologist"

    @patch("litellm.completion")
    def test_specialist_singular_label(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialist: Dermatologist")
        result = MedReferral().get_specialist_recommendation("skin issue")
        assert result == "Dermatologist"

    @patch("litellm.completion")
    def test_all_invalid_returns_raw_specialists_with_disclaimer(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: FakeDoc, NotADoc")
        result = MedReferral().get_specialist_recommendation("mystery illness")
        assert "FakeDoc, NotADoc" in result
        assert "Please verify with a healthcare professional." in result

    @patch("litellm.completion")
    def test_mixed_validity_keeps_only_valid(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Cardiologist, Witch Doctor, Pulmonologist")
        result = MedReferral().get_specialist_recommendation("chest pain")
        assert "Cardiologist" in result
        assert "Pulmonologist" in result
        assert "Witch Doctor" not in result


class TestMedReferralIntegration:
    @patch("litellm.completion")
    def test_cardiac_workflow(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Cardiologist, Pulmonologist")
        result = MedReferral().get_specialist_recommendation("chest pain and shortness of breath")
        assert result == "Cardiologist, Pulmonologist"

    @patch("litellm.completion")
    def test_dermatology_workflow(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Dermatologist")
        result = MedReferral().get_specialist_recommendation("rash on my skin")
        assert result == "Dermatologist"

    @patch("litellm.completion")
    def test_psychiatry_workflow_filters_invalid(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Psychiatrist, Psychologist")
        result = MedReferral().get_specialist_recommendation("depression")
        assert result == "Psychiatrist"


def _mock_response(content: str):
    mr = Mock()
    mr.choices = [Mock()]
    mr.choices[0].message.content = content
    return mr
