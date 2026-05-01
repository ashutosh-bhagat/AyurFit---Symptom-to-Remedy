import pandas as pd
import copy

print("Loading dataset...")
# Load your current 14-group dataset
df = pd.read_csv('../final_ayurfit_updated.csv')
original_count = len(df)

# --- THE SYMPTOM THESAURUS ---
# Format: "exact_term_in_your_csv": ["layman_phrase_1", "layman_phrase_2", "ayurvedic_term"]
# You can add as many lines to this dictionary as you want!
symptom_thesaurus = {
    "acidity": ["heartburn", "chest feels like fire", "sour burps", "burning from spicy food", "amlapitta"],
    "cough": ["hacking cough", "green phlegm", "dry throat", "khasi", "kasa"],
    "headache": ["pounding head", "head pounding", "migraine", "shirashula", "head throbbing"],
    "joint pain": ["knees hurt", "aching joints", "stiff joints", "sandhishula"],
    "indigestion": ["upset stomach", "tummy ache", "bloating", "ajirna"],
    "fever": ["high temp", "burning up", "chills", "jvara"],
    "constipation": ["cannot pass stool", "hard bowels", "vibandha"],
    "stress": ["feeling overwhelmed", "mental pressure", "tension", "manasika udvega"],
    "skin rash": ["itchy skin", "red patches", "hives", "twak roga"],
    "fatigue": ["always tired", "no energy", "exhaustion", "klama", "winded easily"],
    "swelling": ["super puffy", "puffy ankles", "shotha"]
}

# List to hold all our newly generated rows
augmented_rows = []

print("Running NLP Synonym Augmentation...")

# Iterate through every single row in the dataset
for index, row in df.iterrows():
    # Make sure we are dealing with a string and make it lowercase
    current_symptom = str(row['Symptoms']).lower().strip()
    
    # Keep the original row so we don't lose the clinical term
    augmented_rows.append(row)
    
    # Check if the current symptom exactly matches or contains a key from our thesaurus
    for clinical_term, synonyms in symptom_thesaurus.items():
        if clinical_term in current_symptom:
            
            # If a match is found, generate a brand new row for EVERY synonym
            for synonym in synonyms:
                # Deep copy ensures we safely duplicate the row without overwriting memory
                new_row = copy.deepcopy(row)
                
                # Swap out the clinical word for the messy, colloquial synonym
                new_row['Symptoms'] = current_symptom.replace(clinical_term, synonym)
                
                # Add the new row to our massive list
                augmented_rows.append(new_row)

# Convert the massive list of rows back into a Pandas DataFrame
final_combined_df = pd.DataFrame(augmented_rows)

# Drop any accidental duplicates that might have been created
final_combined_df.drop_duplicates(inplace=True)

# Save the newly expanded dataset
output_file = 'ayurfit_nlp_augmented.csv'
final_combined_df.to_csv(output_file, index=False)

print("\n--- AUGMENTATION COMPLETE ---")
print(f"Original Row Count: {original_count}")
print(f"Total Row Count Now: {len(final_combined_df)}")
print(f"Saved to: {output_file}")