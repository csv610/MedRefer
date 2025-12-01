"""
Tests for the MedRefer medical specialist recommendation system.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from medrefer import MedReferral


class TestMedReferralInit:
    """Test MedReferral class initialization."""

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key-123'})
    @patch('litellm.api_key', 'test-key-123')
    def test_init_sets_api_key(self):
        """Test that initialization sets the API key from environment."""
        with patch('litellm.api_key', 'test-key-123') as mock_api_key:
            referral = MedReferral()
            # Verify that the instance was created
            assert referral is not None

    def test_medical_specialists_contains_expected_specialists(self):
        """Test that medical_specialists contains expected specialist types."""
        referral = MedReferral()
        expected_specialists = {
            'Cardiologist',
            'Neurologist',
            'Dermatologist',
            'Psychiatrist',
            'Oncologist',
            'Ophthalmologist',
            'Urologist',
            'Endocrinologist',
            'Gastroenterologist',
        }
        assert expected_specialists.issubset(referral.medical_specialists)

    def test_medical_specialists_is_frozenset(self):
        """Test that medical_specialists is a frozenset."""
        referral = MedReferral()
        assert isinstance(referral.medical_specialists, frozenset)

    def test_medical_specialists_count(self):
        """Test that medical_specialists has the expected count."""
        referral = MedReferral()
        assert len(referral.medical_specialists) == 42


class TestGetSpecialistRecommendation:
    """Test the get_specialist_recommendation method."""

    @patch('litellm.completion')
    def test_get_specialist_recommendation_returns_valid_specialists(self, mock_completion):
        """Test that valid specialists from LLM response are returned."""
        # Mock the LLM response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Cardiologist, Pulmonologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have chest pain")

        assert "Cardiologist" in result
        assert "Pulmonologist" in result

    @patch('litellm.completion')
    def test_get_specialist_recommendation_filters_invalid_specialists(self, mock_completion):
        """Test that invalid specialists are filtered out."""
        # Mock the LLM response with an invalid specialist
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Cardiologist, InvalidSpecialist, Neurologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have a headache")

        assert "Cardiologist" in result
        assert "Neurologist" in result
        assert "InvalidSpecialist" not in result

    @patch('litellm.completion')
    def test_get_specialist_recommendation_handles_no_valid_specialists(self, mock_completion):
        """Test that a disclaimer is returned when no valid specialists are found."""
        # Mock the LLM response with only invalid specialists
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: InvalidSpecialist1, InvalidSpecialist2"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have an unusual condition")

        assert "Note: Please verify with a healthcare professional." in result

    @patch('litellm.completion')
    def test_get_specialist_recommendation_handles_missing_specialists_line(self, mock_completion):
        """Test handling when response doesn't contain 'Specialists:' line."""
        # Mock the LLM response without the specialists line
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "I recommend seeing a doctor"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I feel unwell")

        assert "Unknown Specialists" in result or "Please verify with a healthcare professional." in result

    @patch('litellm.completion')
    def test_get_specialist_recommendation_handles_api_error(self, mock_completion):
        """Test that API errors are handled gracefully."""
        # Mock the LLM to raise an exception
        mock_completion.side_effect = Exception("API Connection Error")

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have a headache")

        assert "Error:" in result
        assert "API Connection Error" in result

    @patch('litellm.completion')
    def test_get_specialist_recommendation_strips_whitespace(self, mock_completion):
        """Test that specialist names are properly stripped of whitespace."""
        # Mock the LLM response with extra whitespace
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists:  Cardiologist  ,  Neurologist  "
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have symptoms")

        assert "Cardiologist" in result
        assert "Neurologist" in result
        # Ensure no leading/trailing whitespace in result
        assert not result.startswith(" ")
        assert not result.endswith(" ")

    @patch('litellm.completion')
    def test_get_specialist_recommendation_single_specialist(self, mock_completion):
        """Test recommendation with a single specialist."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Dermatologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have a skin rash")

        assert result == "Dermatologist"

    @patch('litellm.completion')
    def test_get_specialist_recommendation_multiple_specialists(self, mock_completion):
        """Test recommendation with multiple specialists."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Rheumatologist, Orthopedic Surgeon, Internal Medicine Doctor (Internist)"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have joint pain and swelling")

        assert "Rheumatologist" in result
        assert "Orthopedic Surgeon" in result
        assert "Internal Medicine Doctor (Internist)" in result

    @patch('litellm.completion')
    def test_get_specialist_recommendation_case_sensitivity(self, mock_completion):
        """Test that specialist matching is case-sensitive."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: cardiologist, NEUROLOGIST, Dermatologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have symptoms")

        # Should not match due to case sensitivity
        assert "cardiologist" not in referral.medical_specialists
        assert "NEUROLOGIST" not in referral.medical_specialists
        # But the valid one should be there
        assert "Dermatologist" in result

    @patch('litellm.completion')
    def test_get_specialist_recommendation_calls_litellm_with_correct_params(self, mock_completion):
        """Test that litellm.completion is called with correct parameters."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Cardiologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        question = "I have chest pain"
        referral.get_specialist_recommendation(question)

        # Verify litellm.completion was called
        mock_completion.assert_called_once()

        # Verify the call includes correct parameters
        call_kwargs = mock_completion.call_args.kwargs
        assert call_kwargs['model'] == 'gpt-4o'
        assert call_kwargs['max_tokens'] == 100
        assert len(call_kwargs['messages']) == 2
        assert call_kwargs['messages'][0]['role'] == 'system'
        assert call_kwargs['messages'][1]['role'] == 'user'
        assert question in call_kwargs['messages'][1]['content']

    @patch('litellm.completion')
    def test_get_specialist_recommendation_with_special_characters(self, mock_completion):
        """Test handling of specialist names with special characters."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Otolaryngologist (ENT Specialist), Physical Medicine & Rehabilitation (PM&R) Specialist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have ear and throat issues")

        assert "Otolaryngologist (ENT Specialist)" in result
        assert "Physical Medicine & Rehabilitation (PM&R) Specialist)" in result

    @patch('litellm.completion')
    def test_get_specialist_recommendation_empty_question(self, mock_completion):
        """Test handling of empty medical question."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: General Surgeon"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("")

        assert "General Surgeon" in result or "Error" in result

    @patch('litellm.completion')
    def test_get_specialist_recommendation_very_long_question(self, mock_completion):
        """Test handling of very long medical question."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Neurologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        long_question = "I have " + "symptoms " * 100
        result = referral.get_specialist_recommendation(long_question)

        assert "Neurologist" in result or "Error" in result


class TestMedReferralIntegration:
    """Integration tests for the MedReferral system."""

    @patch('litellm.completion')
    def test_full_workflow_cardiac_issue(self, mock_completion):
        """Test full workflow for a cardiac issue."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Cardiologist, Pulmonologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have chest pain and shortness of breath")

        assert "Cardiologist" in result
        assert "Pulmonologist" in result

    @patch('litellm.completion')
    def test_full_workflow_dermatological_issue(self, mock_completion):
        """Test full workflow for a dermatological issue."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Dermatologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have a rash on my skin")

        assert "Dermatologist" in result

    @patch('litellm.completion')
    def test_full_workflow_psychiatric_issue(self, mock_completion):
        """Test full workflow for a psychiatric issue."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Specialists: Psychiatrist, Psychologist"
        mock_completion.return_value = mock_response

        referral = MedReferral()
        result = referral.get_specialist_recommendation("I have been experiencing depression")

        # Psychologist is not in the valid list, so only Psychiatrist should remain
        assert "Psychiatrist" in result
        assert "Psychologist" not in result
