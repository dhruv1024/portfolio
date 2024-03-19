import argparse
import numpy as np
from scipy.optimize import minimize_scalar

def calculate_attractiveness(age, wealth, beauty, gender='man', divorced=False, porn_factor=0):
    # Age factor
    age_factor = 1 - 0.02 * max(0, age - 20)
    
    # Wealth factor
    if gender == 'man':
        wealth_factor = two_sided_exponential_weight(wealth, a=5)
    else:
        wealth_factor = two_sided_exponential_weight(wealth, a=5) if not divorced else two_sided_exponential_weight(wealth + 0.1, a=5)
    
    # Beauty factor
    beauty_factor = two_sided_exponential_weight(beauty, a=5) if gender == 'woman' else 0
    
    # Divorce factor
    divorce_factor = 0.5 if divorced else 0
    
    # Porn factor
    porn_factor = two_sided_exponential_weight(porn_factor, a=5) if gender == 'woman' else 0
    
    attractiveness = age_factor + wealth_factor + beauty_factor - divorce_factor - porn_factor
    
    return max(0, attractiveness)  # Ensure attractiveness is within a reasonable range

def two_sided_exponential_weight(x, a=5):
    if x >= 0.5:
        return np.exp(2 * a * (x - 0.5)) / (1 + np.exp(2 * a * (x - 0.5)))
    else:
        return -np.exp(-2 * a * x) / (1 + np.exp(-2 * a * x))

def logistic_function(x):
    return 1 / (1 + np.exp(-x))

def calculate_probability(age, attractiveness, desperation_factor, available_years, age_weight=1, attr_weight=1, desp_weight=1):
    base_probability = 0.4
    weighted_attractiveness = two_sided_exponential_weight(attractiveness, a=5) * attr_weight
    weighted_desperation = two_sided_exponential_weight(desperation_factor, a=5) * desp_weight
    diminishing_age_factor = logistic_function(age - 30)  # Adjusted logistic function for age impact
    
    # Adjust available years for marriage based on age
    adjusted_available_years = max(0, available_years - (age - 20))
    
    raw_probability = base_probability * (weighted_attractiveness + weighted_desperation + diminishing_age_factor * age_weight) * adjusted_available_years / 30
    
    # Ensure the probability is within the [0, 1] range
    probability = max(0, min(1, raw_probability))
    
    return probability

def likelihood(age, *args):
    attractiveness, wealth, beauty, gender, divorced, porn_factor, age_weight, attr_weight, desp_weight, available_years = args
    
    attractiveness = calculate_attractiveness(
        age=age,
        wealth=wealth,
        beauty=beauty,
        gender=gender,
        divorced=divorced,
        porn_factor=porn_factor
    )
    
    probability = calculate_probability(
        age=age,
        attractiveness=attractiveness,
        desperation_factor=logistic_function(age - 30),
        available_years=available_years,
        age_weight=age_weight,
        attr_weight=attr_weight,
        desp_weight=desp_weight
    )
    
    return -probability  # Negative because we are minimizing

def most_likely_age(attractiveness, wealth, beauty, gender='man', divorced=False, porn_factor=0, age_weight=1, attr_weight=1, desp_weight=1):
    available_years = 30  # Maximum number of years available for marriage
    result = minimize_scalar(likelihood, bounds=(20, 50), args=(attractiveness, wealth, beauty, gender, divorced, porn_factor, age_weight, attr_weight, desp_weight, available_years), method='bounded')
    
    return result.x, -result.fun

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the likelihood of getting married based on specified factors.")
    parser.add_argument("--age", type=int, required=True, help="Age of the person")
    parser.add_argument("--wealth", type=float, required=True, help="Wealth factor (normalized between 0 and 1)")
    parser.add_argument("--beauty", type=float, help="Beauty factor (only for women, normalized between 0 and 1)")
    parser.add_argument("--gender", choices=["man", "woman"], default="man", help="Gender of the person")
    parser.add_argument("--divorced", action="store_true", help="Specify if the person is divorced")
    parser.add_argument("--porn_factor", type=float, default=0, help="Porn factor (only for women, normalized between 0 and 1)")
    parser.add_argument("--age_weight", type=float, default=1, help="Weight for age impact on probability")
    parser.add_argument("--attr_weight", type=float, default=1, help="Weight for attractiveness impact on probability")
    parser.add_argument("--desp_weight", type=float, default=1, help="Weight for desperation impact on probability")

    args = parser.parse_args()

    attractiveness = calculate_attractiveness(
        age=args.age,
        wealth=args.wealth,
        beauty=args.beauty,
        gender=args.gender,
        divorced=args.divorced,
        porn_factor=args.porn_factor
    )

    likely_age, probability = most_likely_age(
        attractiveness=attractiveness,
        wealth=args.wealth,
        beauty=args.beauty,
        gender=args.gender,
        divorced=args.divorced,
        porn_factor=args.porn_factor,
        age_weight=args.age_weight,
        attr_weight=args.attr_weight,
        desp_weight=args.desp_weight
    )

    print(f"For a {args.gender}, the likely age to get married is {likely_age:.2f} with a probability of {probability * 100:.2f}%.")
