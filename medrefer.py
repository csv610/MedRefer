import openai
import os
import random
import re

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your API key is set as an environment variable

# List of Medical Specialist Doctors
medical_specialists = [
    # Medical Specialties
    "Internal Medicine Doctor (Internist)",
    "Cardiologist",
    "Endocrinologist",
    "Gastroenterologist",
    "Hematologist",
    "Nephrologist",
    "Neurologist",
    "Oncologist",
    "Pulmonologist",
    "Rheumatologist",
    "Infectious Disease Specialist",
    "Geriatrician",

    # Surgical Specialties
    "General Surgeon",
    "Cardiothoracic Surgeon",
    "Neurosurgeon",
    "Orthopedic Surgeon",
    "Plastic Surgeon",
    "Ophthalmologist",
    "Otolaryngologist (ENT Specialist)",
    "Urologist",
    "Colorectal Surgeon",
    "Pediatric Surgeon",
    "Trauma Surgeon",
    "Transplant Surgeon",

    # Women’s and Children’s Health
    "Obstetrician",
    "Gynecologist",
    "Pediatrician",
    "Neonatologist",
    "Maternal-Fetal Medicine Specialist",

    # Diagnostic and Laboratory Specialties
    "Pathologist",
    "Radiologist",
    "Nuclear Medicine Specialist",

    # Mental Health Specialties
    "Psychiatrist",
    "Child and Adolescent Psychiatrist",
    "Forensic Psychiatrist",
    "Geriatric Psychiatrist",

    # Allied and Holistic Specialties
    "Dermatologist",
    "Allergist",
    "Immunologist",
    "Anesthesiologist",
    "Sports Medicine Doctor",
    "Physical Medicine & Rehabilitation (PM&R) Specialist",
    "Pain Management Specialist",
    "Sleep Medicine Specialist",
    "Occupational Medicine Specialist"
]

def get_specialist_recommendation(question):
    """
    Function to determine the appropriate medical specialists for a given question using OpenAI GPT model.
    This version supports multiple specialist recommendations.
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
        valid_specialists = [s for s in recommended_specialists if s in medical_specialists]

        if valid_specialists:
            return ", ".join(valid_specialists)
        else:
            return f"{specialists} (Note: Please verify with a healthcare professional.)"

    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    while(1):
         medical_question = input("Enter your medical question: ")
         specialists = get_specialist_recommendation(medical_question)
         print(f"Recommended Specialists: {specialists}")
