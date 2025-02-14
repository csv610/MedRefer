import openai
import os
import random
import re

class MedReferral:
    """
    A class for determining the appropriate medical specialists based on a given question using OpenAI GPT model.
    """
    medical_specialists = frozenset(
        [
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
            "Occupational Medicine Specialist"
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
        ]
    )
    
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def get_specialist_recommendation(self, question):
        """
        Determines the appropriate medical specialists for a given question.
        """
        prompt = f"""
        You are a medical assistant. Based on the given medical question, recommend the most suitable specialist doctors.
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
        Specialists:
        """

        try:
            response = openai.chat.completions.create(
                model="gpt-4o", 
                messages=[{"role": "system", "content": "You are a helpful medical assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=100
            )

            # Extract the content of the response
            full_response = response.choices[0].message.content.strip()

            # Use regex to extract only the specialist names
            match = re.search(r"Specialists?:\s*(.*)", full_response)
            if match:
                specialists = match.group(1)
            else:
                specialists = "Unknown Specialists (Please verify with a healthcare professional.)"

            # Ensure specialists are in the predefined list and return only valid specialists
            recommended_specialists = [s.strip() for s in specialists.split(",")]
            valid_specialists = [s for s in recommended_specialists if s in self.medical_specialists]

            if valid_specialists:
                return ", ".join(valid_specialists)
            else:
                return f"{specialists} (Note: Please verify with a healthcare professional.)"

        except Exception as e:
            return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    med_referral = MedReferral()
    while True:
        medical_question = input("Enter your medical question: ")
        specialists = med_referral.get_specialist_recommendation(medical_question)
        print(f"Recommended Specialists: {specialists}")

