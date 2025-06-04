import pickle
import pandas as pd
import numpy as np

class Models():
    def __init__(self):
        with open("models.pkl", "rb") as f:
            self.models = pickle.load(f)
            
        with open("scaled.pkl", "rb") as f:
            self.scaled = pickle.load(f)
            
    def preprocess(self, input_data: dict):
        categories = {
            'person_gender': ['male', 'female'],
            'person_education': ['Doctorate', 'Master', 'Bachelor', 'Associate', 'High School'],
            'person_home_ownership': ['RENT', 'OTHER', 'MORTGAGE', 'OWN'],
            'loan_intent': ['MEDICAL', 'EDUCATION', 'DEBTCONSOLIDATION', 'HOMEIMPROVEMENT', 'VENTURE', 'PERSONAL'],
        }

        final_columns = [
            'person_age', 'person_income', 'person_emp_exp', 'loan_amnt',
            'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length',
            'credit_score', 'previous_loan_defaults_on_file',
            'person_gender_female', 'person_gender_male',
            'person_education_Associate', 'person_education_Bachelor',
            'person_education_Doctorate', 'person_education_High School',
            'person_education_Master', 'person_home_ownership_MORTGAGE',
            'person_home_ownership_OTHER', 'person_home_ownership_OWN',
            'person_home_ownership_RENT', 'loan_intent_DEBTCONSOLIDATION',
            'loan_intent_EDUCATION', 'loan_intent_HOMEIMPROVEMENT',
            'loan_intent_MEDICAL', 'loan_intent_PERSONAL', 'loan_intent_VENTURE'
        ]

        final = {}

        for col in ['person_age', 'person_income', 'person_emp_exp', 'loan_amnt',
                    'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length',
                    'credit_score']:
            final[col] = [float(input_data[col])]

        final['previous_loan_defaults_on_file'] = [int((input_data['previous_loan_defaults_on_file'] == 'Yes'))]

        for cat in categories:
            for t in categories[cat]:
                final[f'{cat}_{t}'] = [int((input_data[cat] == t))]


        final_df = pd.DataFrame(columns=final_columns)
        for c in final:
            final_df[c] = final[c]  
            
        return final_df
    
    def scaling(self, df: pd.DataFrame):
        scaled_df = pd.DataFrame(columns=df.columns)
        for col in df.columns:
            scaled_df[col] = (df[col] - self.scaled[col]["mean"]) / self.scaled[col]["std"]
        
        return np.array(scaled_df)
            

    def predict(self, sample, name):
        df = self.preprocess(sample)
        if name in ["Naive Bayes", "KNN", "SVM"]:
            df = self.scaling(df)
        return self.models[name].predict(df)
    
    
if __name__ == "__main__":
    models = Models()

    # Исходные данные
    input_data = {
        'person_age': 23.0,
        'person_gender': 'female',
        'person_education': 'Master',
        'person_income': 77693.0,
        'person_emp_exp': 0,
        'person_home_ownership': 'RENT',
        'loan_amnt': 3500.0,
        'loan_intent': 'EDUCATION',
        'loan_int_rate': 9.63,
        'loan_percent_income': 0.05,
        'cb_person_cred_hist_length': 3.0,
        'credit_score': 679,
        'previous_loan_defaults_on_file': 'Yes'
    }

    kek = models.predict(input_data, "KNN")
    print(kek)

