import pytest
from unittest.mock import Mock, patch
import logging
from medrefer import MedReferral


@pytest.fixture(autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


class TestMedReferralInit:
    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    def test_init_sets_litellm_api_key(self):
        import litellm
        with patch("litellm.api_key", ""):
            MedReferral()
            assert litellm.api_key == "test-key-123"

    @patch.dict("os.environ", {"MEDREFER_MODEL": "custom-model"})
    def test_init_uses_env_model(self):
        r = MedReferral()
        assert r.model == "custom-model"

    def test_init_default_model(self):
        r = MedReferral()
        assert r.model == "ollama/gemma4"

    def test_init_explicit_model(self):
        r = MedReferral(model="gpt-4o")
        assert r.model == "gpt-4o"

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


class TestInputValidation:
    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            MedReferral().get_specialist_recommendation("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            MedReferral().get_specialist_recommendation("   ")

    def test_non_string_raises(self):
        with pytest.raises(ValueError, match="must be a string"):
            MedReferral().get_specialist_recommendation(123)

    def test_excessive_length_raises(self):
        long_input = "x" * 2001
        with pytest.raises(ValueError, match="exceeds maximum length"):
            MedReferral().get_specialist_recommendation(long_input)


class TestEmergencyDetection:
    def test_heart_attack_triggers_emergency(self):
        result = MedReferral().get_specialist_recommendation("I think I'm having a heart attack")
        assert "EMERGENCY" in result
        assert "911" in result

    def test_stroke_keyword_triggers_emergency(self):
        result = MedReferral().get_specialist_recommendation("signs of stroke")
        assert "EMERGENCY" in result

    def test_severe_burn_triggers_emergency(self):
        result = MedReferral().get_specialist_recommendation("severe burn on my arm")
        assert "EMERGENCY" in result

    def test_suicidal_triggers_emergency(self):
        result = MedReferral().get_specialist_recommendation("feeling suicidal")
        assert "EMERGENCY" in result

    def test_choking_triggers_emergency(self):
        result = MedReferral().get_specialist_recommendation("cannot breathe")
        assert "EMERGENCY" in result

    def test_non_emergency_does_not_trigger(self):
        result = MedReferral().get_specialist_recommendation("I have a mild headache")
        assert "EMERGENCY" not in result


class TestGetSpecialistRecommendation:
    @patch("litellm.completion")
    def test_returns_valid_specialists_with_disclaimer(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Cardiologist, Pulmonologist")
        result = MedReferral().get_specialist_recommendation("chest pain")
        assert "Cardiologist" in result
        assert "Pulmonologist" in result
        assert "Please verify with a healthcare professional." in result

    @patch("litellm.completion")
    def test_filters_invalid_specialists(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Cardiologist, Quack, Neurologist")
        result = MedReferral().get_specialist_recommendation("headache")
        assert "Cardiologist" in result
        assert "Neurologist" in result
        assert "Quack" not in result

    @patch("litellm.completion")
    def test_no_valid_specialists_returns_disclaimer(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Quack, Witch Doctor")
        result = MedReferral().get_specialist_recommendation("weird symptoms")
        assert "Quack" in result
        assert "Witch Doctor" in result
        assert "Please consult a healthcare professional" in result

    @patch("litellm.completion")
    def test_missing_specialists_line(self, mock_completion):
        mock_completion.return_value = _mock_response("Go see a doctor.")
        result = MedReferral().get_specialist_recommendation("sick")
        assert "Unable to determine" in result

    @patch("litellm.completion")
    def test_api_error(self, mock_completion):
        mock_completion.side_effect = Exception("API Connection Error")
        result = MedReferral().get_specialist_recommendation("headache")
        assert result == "Error: API Connection Error"

    @patch("litellm.completion")
    def test_strips_whitespace(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists:  Cardiologist  ,  Neurologist  ")
        result = MedReferral().get_specialist_recommendation("symptoms")
        assert "Cardiologist" in result
        assert "Neurologist" in result

    @patch("litellm.completion")
    def test_single_specialist(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Dermatologist")
        result = MedReferral().get_specialist_recommendation("skin rash")
        assert "Dermatologist" in result

    @patch("litellm.completion")
    def test_multiple_specialists(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Rheumatologist, Orthopedic Surgeon, Internal Medicine Doctor (Internist)")
        result = MedReferral().get_specialist_recommendation("joint pain")
        assert "Rheumatologist" in result
        assert "Orthopedic Surgeon" in result
        assert "Internal Medicine Doctor (Internist)" in result

    @patch("litellm.completion")
    def test_case_insensitive_matching(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: cardiologist, NEUROLOGIST, Dermatologist")
        result = MedReferral().get_specialist_recommendation("symptoms")
        assert "Cardiologist" in result
        assert "Neurologist" in result
        assert "Dermatologist" in result

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
        referral = MedReferral(model="test-model")
        referral.get_specialist_recommendation(question)

        mock_completion.assert_called_once()
        kwargs = mock_completion.call_args.kwargs
        assert kwargs["model"] == "test-model"
        assert kwargs["max_tokens"] == 100
        assert len(kwargs["messages"]) == 2
        assert kwargs["messages"][0]["role"] == "system"
        assert kwargs["messages"][1]["role"] == "user"
        assert question in kwargs["messages"][1]["content"]

    @patch("litellm.completion")
    def test_specialist_singular_label(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialist: Dermatologist")
        result = MedReferral().get_specialist_recommendation("skin issue")
        assert "Dermatologist" in result

    @patch("litellm.completion")
    def test_all_invalid_returns_raw_specialists_with_disclaimer(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: FakeDoc, NotADoc")
        result = MedReferral().get_specialist_recommendation("mystery illness")
        assert "FakeDoc, NotADoc" in result
        assert "Please consult a healthcare professional" in result

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
        assert "Cardiologist" in result
        assert "Pulmonologist" in result

    @patch("litellm.completion")
    def test_dermatology_workflow(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Dermatologist")
        result = MedReferral().get_specialist_recommendation("rash on my skin")
        assert "Dermatologist" in result

    @patch("litellm.completion")
    def test_psychiatry_workflow_filters_invalid(self, mock_completion):
        mock_completion.return_value = _mock_response("Specialists: Psychiatrist, Psychologist")
        result = MedReferral().get_specialist_recommendation("depression")
        assert "Psychiatrist" in result
        assert "Psychologist" not in result


def _mock_response(content: str):
    mr = Mock()
    mr.choices = [Mock()]
    mr.choices[0].message.content = content
    return mr
